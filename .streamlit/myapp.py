import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from ultralytics import YOLO
import cv2
import numpy as np

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Real-time Object Detection", page_icon="🎥")

st.title("🎥 Real-Time Object Detection with YOLOv8")
st.write("This app detects objects from your **system camera (webcam)** using YOLOv8.")

# -------------------------------
# Sidebar Settings
# -------------------------------
st.sidebar.header("Settings")

model_choice = st.sidebar.selectbox(
    "Choose YOLO Model",
    ["yolov8n.pt (nano)", "yolov8s.pt (small)", "yolov8m.pt (medium)"]
)

conf_thres = st.sidebar.slider("Confidence Threshold", 0.2, 0.90, 0.45)

model_map = {
    "yolov8n.pt (nano)": "yolov8n.pt",
    "yolov8s.pt (small)": "yolov8s.pt",
    "yolov8m.pt (medium)": "yolov8m.pt",
}

# -------------------------------
# Load YOLO Model Only Once
# -------------------------------
@st.cache_resource
def load_model(model_name):
    return YOLO(model_name)

model = load_model(model_map[model_choice])

# -------------------------------
# Video Transformer
# -------------------------------
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.model = model
        self.conf = conf_thres

    def transform(self, frame):
        # Convert frame to numpy array (BGR)
        img = frame.to_ndarray(format="bgr24")

        # Run YOLO safely
        try:
            results = self.model.predict(img, conf=self.conf, verbose=False)
        except Exception as e:
            print("YOLO Error:", e)
            return img

        r = results[0]

        # If detection is corrupted, return original frame
        if r.boxes is None or len(r.boxes) == 0:
            return img

        # Clean predictions
        new_boxes = []
        for box in r.boxes:
            try:
                xyxy = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # Skip invalid / hallucinated results
                if cls not in model.model.names:
                    continue
                if conf < self.conf:
                    continue
                if xyxy[0] < 0 or xyxy[1] < 0:
                    continue

                new_boxes.append(box)
            except:
                continue

        # If nothing valid, return frame
        if len(new_boxes) == 0:
            return img

        # Replace dangerous YOLO list with filtered list
        r.boxes = type(r.boxes)(new_boxes)

        # Draw boxes safely
        annotated = r.plot()

        return annotated


# -------------------------------
# Start Webcam Stream
# -------------------------------
webrtc_streamer(
    key="object-detection",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)
