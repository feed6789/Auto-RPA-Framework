import cv2
import numpy as np
import mss
from ultralytics import YOLO
from paddleocr import PaddleOCR
import os
import logging
logging.getLogger("ppocr").setLevel(logging.ERROR)

# Suppress PaddleOCR logging unless it's an error
os.environ['PP_OCR_LOG_LEVEL'] = '3'

class VisionEngine:
    """
    Handles all visual processing tasks:
    - High-speed screen capture via MSS.
    - Static object finding via OpenCV Template Matching.
    - Dynamic object detection via YOLOv8.
    - Text reading via PaddleOCR.
    """
    def __init__(self, yolo_model_path=None):
        self.sct = mss.mss()
        self.yolo_model = None
        self.ocr_reader = None

        if yolo_model_path:
            try:
                self.yolo_model = YOLO(yolo_model_path)
                print(f"[Vision] YOLO model loaded successfully from {yolo_model_path}")
            except Exception as e:
                print(f"[Vision Error] Failed to load YOLO model: {e}")
        
        try:
            # Initialize OCR for English. Add other languages like 'ch' if needed.
            # This will download models on first run.
            self.ocr_reader = PaddleOCR(use_angle_cls=True, lang='en')
            print("[Vision] PaddleOCR engine initialized.")
        except Exception as e:
            print(f"[Vision Error] Failed to initialize PaddleOCR: {e}")


    def capture_screen(self, region=None):
        """
        Captures the screen. If a region (x, y, w, h) is provided, captures that area.
        Otherwise, captures the primary monitor.
        """
        if region:
            monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
        else:
            # monitors[1] is typically the primary display
            monitor = self.sct.monitors[1]

        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        # Convert from BGRA to BGR for OpenCV compatibility
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def find_template(self, screen_img, template_path, confidence=0.8):
        """
        Finds a static image (template) within a larger image (screen).
        Returns the center coordinates (x, y) if found, otherwise None.
        """
        if not os.path.exists(template_path):
            print(f"[Vision Error] Template path does not exist: {template_path}")
            return None
            
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        h, w = template.shape[:2]

        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        return None

    def detect_objects_yolo(self, screen_img, confidence=0.6):
        """
        Performs object detection using the loaded YOLOv8 model.
        Returns a list of detections, each with {'box': (x1, y1, x2, y2), 'center': (cx, cy), 'label': name}.
        """
        if not self.yolo_model:
            print("[Vision Error] YOLO model is not loaded.")
            return []

        results = self.yolo_model.predict(source=screen_img, conf=confidence, verbose=False)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                label = self.yolo_model.names[int(box.cls)]
                detections.append({
                    'box': (x1, y1, x2, y2),
                    'center': (center_x, center_y),
                    'label': label
                })
        return detections

    def read_text_ocr(self, screen_img):
        """
        Performs OCR on a given image region.
        Returns a list of found text strings.
        """
        if not self.ocr_reader:
            print("[Vision Error] OCR reader is not initialized.")
            return []
            
        result = self.ocr_reader.ocr(screen_img, cls=True)
        texts = [line[1][0] for line in result[0]] if result and result[0] else []
        return texts