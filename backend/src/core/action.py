from abc import ABC, abstractmethod
import time

class Action(ABC):
    @abstractmethod
    def execute(self, context):
        pass

class WaitAndClickTemplateAction(Action):
    def __init__(self, template_path, timeout=30):
        self.template_path = template_path
        self.timeout = timeout

    def execute(self, context):
        context.logger(f"Waiting for template: {self.template_path}")
        # 1. Smart Wait
        pos, screen = context.waiter.for_template(self.template_path, timeout=self.timeout)
        context.logger(f"Found at {pos}. Clicking...")
        # 2. Human click
        context.controller.move_to(pos[0], pos[1])
        context.controller.click()
        return True

class YOLOInteractAction(Action):
    def __init__(self, target_label, timeout=30):
        self.target_label = target_label
        self.timeout = timeout

    def execute(self, context):
        context.logger(f"Waiting for YOLO object: {self.target_label}")
        det, screen = context.waiter.for_yolo_object(self.target_label, timeout=self.timeout)
        context.logger(f"Found '{self.target_label}' at {det['center']}. Interacting...")
        context.controller.move_to(det['center'][0], det['center'][1])
        context.controller.click()
        return True