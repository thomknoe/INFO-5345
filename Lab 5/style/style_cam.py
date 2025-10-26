import argparse
import cv2
import numpy as np
import time
import math
from tflite_runtime.interpreter import Interpreter

# ---------- Utils ----------
def divisible_by_4(x):
    return int(math.ceil(x / 4.0) * 4)

def load_interpreter(path, threads=4):
    it = Interpreter(model_path=path, num_threads=threads)
    it.allocate_tensors()
    return it

def preprocess_style(style_bgr):
    # style_predict_quantized_256 expects 256x256 RGB float32 in [0,1]
    rgb = cv2.cvtColor(style_bgr, cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, (256, 256), interpolation=cv2.INTER_AREA)
    rgb = rgb.astype(np.float32) / 255.0
    return np.expand_dims(rgb, 0)

def preprocess_content_first(frame_bgr, target_w=320):
    # Determine fixed (H,W) for the session, multiples of 4
    h0, w0 = frame_bgr.shape[:2]
    scale = target_w / float(w0)
    W = divisible_by_4(int(w0 * scale))
    H = divisible_by_4(int(h0 * scale))
    # Produce first tensor
    bgr = cv2.resize(frame_bgr, (W, H), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return np.expand_dims(rgb, 0), (H, W)

def preprocess_content_fixed(frame_bgr, H, W):
    # Always resize to the fixed HxW decided at startup
    bgr = cv2.resize(frame_bgr, (W, H), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return np.expand_dims(rgb, 0)

def postprocess_bgr(rgb_tensor):
    # rgb_tensor: [1, H, W, 3] float32 in [0,1]
    img = np.clip(rgb_tensor[0] * 255.0, 0, 255).astype(np.uint8)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def run_style_predict(predict_it, style_in):
    in_idx = predict_it.get_input_details()[0]['index']
    out_idx = predict_it.get_output_details()[0]['index']
    predict_it.set_tensor(in_idx, style_in)
    predict_it.invoke()
    return predict_it.get_tensor(out_idx)   # [1,100] float32

def identify_transform_inputs(transform_it):
    """
    Robustly determine which input is content [1,H,W,3] and which is style [1,100].
    Handles cases where shape or shape_signature are None or both 4D at first.
    """
    ids = transform_it.get_input_details()
    id_content = None
    id_style = None

    # First try actual shapes
    for d in ids:
        shp = d.get("shape", None)
        if shp is not None and len(shp) == 4:
            id_content = d["index"]
        elif shp is not None and len(shp) == 2:
            id_style = d["index"]

    # Fallback to shape_signature if needed
    if id_content is None or id_style is None:
        for d in ids:
            sig = d.get("shape_signature", None)
            if sig is not None and len(sig) == 4 and id_content is None:
                id_content = d["index"]
            elif sig is not None and len(sig) == 2 and id_style is None:
                id_style = d["index"]

    if id_content is None or id_style is None:
        # Final fallback: pick largest-rank as content, smallest as style
        ranks = [(d["index"], len(d.get("shape", [])) or 0) for d in ids]
        ranks.sort(key=lambda x: x[1], reverse=True)
        if ranks:
            id_content = ranks[0][0]
        if len(ranks) > 1:
            id_style = ranks[-1][0]

    if id_content is None or id_style is None:
        raise RuntimeError("Could not identify content/style input tensors from transform model.")

    return id_content, id_style

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", type=int, default=0, help="Webcam index")
    ap.add_argument("--style", type=str, required=True, help="Path to style image (jpg/png)")
    ap.add_argument("--threads", type=int, default=4, help="TFLite CPU threads")
    ap.add_argument("--alpha", type=float, default=1.0, help="Blend strength 0..1 (stylized vs original)")
    ap.add_argument("--mirror", action="store_true", help="Mirror (selfie) view")
    ap.add_argument("--width", type=int, default=320, help="Fixed content width")
    args = ap.parse_args()

    # Load models
    predict_it  = load_interpreter("style_predict.tflite",  args.threads)
    transform_it = load_interpreter("style_transform.tflite", args.threads)

    # Load & encode style once
    style_bgr = cv2.imread(args.style)
    if style_bgr is None:
        raise FileNotFoundError(f"Could not read style image: {args.style}")
    style_in = preprocess_style(style_bgr)
    style_bottleneck = run_style_predict(predict_it, style_in)

    # Camera
    cap = cv2.VideoCapture(args.cam)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.cam}")

    print("Press 'r' to reload style image, 'q' to quit.")

    # Grab first frame to fix (H,W)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Could not read first frame from camera.")
    if args.mirror:
        frame = cv2.flip(frame, 1)

    content_input, (H, W) = preprocess_content_first(frame, target_w=args.width)

    # Identify input indices for transform model
    id_content, id_style = identify_transform_inputs(transform_it)

    # Resize content input tensor ONCE and re-allocate
    transform_it.resize_tensor_input(id_content, content_input.shape, strict=False)
    transform_it.allocate_tensors()

    # Output tensor index
    out_idx = transform_it.get_output_details()[0]['index']

    # Main loop
    last = time.time()
    frames = 0
    fps_txt = None

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if args.mirror:
            frame = cv2.flip(frame, 1)

        # Preprocess to the fixed HxW each frame
        content_input = preprocess_content_fixed(frame, H, W)

        # Run transform
        transform_it.set_tensor(id_content, content_input)
        transform_it.set_tensor(id_style, style_bottleneck)
        transform_it.invoke()
        stylized = transform_it.get_tensor(out_idx)   # [1,H,W,3] float32
        out_bgr = postprocess_bgr(stylized)

        # Optional blend with original
        if args.alpha < 1.0:
            base = cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)
            out_bgr = cv2.addWeighted(out_bgr, args.alpha, base, 1.0 - args.alpha, 0)

        # FPS meter
        frames += 1
        now = time.time()
        if now - last >= 1.0:
            fps_txt = f"~{frames / (now - last):.1f} FPS | {W}x{H} | alpha={args.alpha}"
            last = now
            frames = 0

        if fps_txt:
            cv2.putText(out_bgr, fps_txt, (8, 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(out_bgr, fps_txt, (8, 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow("Arbitrary Style Transfer (TFLite, quantized)", out_bgr)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('r'):
            # Allow hot-reloading the style image on disk
            style_bgr = cv2.imread(args.style)
            if style_bgr is not None:
                style_in = preprocess_style(style_bgr)
                style_bottleneck = run_style_predict(predict_it, style_in)
                print("Style reloaded.")
            else:
                print("Failed to reload style (file missing).")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
