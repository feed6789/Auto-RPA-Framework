import time

class SmartWait:
    """Intelligent waiting mechanisms replacing time.sleep()"""
    def __init__(self, vision_engine):
        self.vision = vision_engine

    def for_template(self, template_path, confidence=0.8, timeout=30, poll_interval=0.5):
        """Blocks until a template appears on screen."""
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            screen = self.vision.capture_screen()
            pos = self.vision.find_template(screen, template_path, confidence)
            if pos:
                return pos, screen
            time.sleep(poll_interval)
        raise TimeoutError(f"Template {template_path} not found within {timeout}s")

    def for_yolo_object(self, label, confidence=0.6, timeout=30, poll_interval=0.5):
        """Blocks until a YOLO object appears."""
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            screen = self.vision.capture_screen()
            detections = self.vision.detect_objects_yolo(screen, confidence)
            for det in detections:
                if det['label'] == label:
                    return det, screen
            time.sleep(poll_interval)
        raise TimeoutError(f"Object '{label}' not found within {timeout}s")