import keyboard
import time
import threading
from src.vision.vision_engine import VisionEngine
from src.input.human_controller import HumanController
from src.wait.smart_wait import SmartWait
from src.core.engine import WorkflowContext, WorkflowEngine
from src.core.actions import WaitAndClickTemplateAction, YOLOInteractAction

class AutomationBot:
    def __init__(self):
        self.vision = VisionEngine(yolo_model_path="models/best.pt") 
        self.controller = HumanController()
        self.waiter = SmartWait(self.vision)
        self.print = print 
        
        # Initialize context and engine
        self.context = WorkflowContext(self.vision, self.controller, self.waiter, self.log_wrapper)
        self.engine = WorkflowEngine(self.context)
        self.context.is_running = False

    def log_wrapper(self, message):
        self.print(message)

    def setup_hotkeys(self):
        keyboard.add_hotkey('F9', self.start_bot)
        keyboard.add_hotkey('F10', self.stop_bot) # Maps to pause in engine
        keyboard.add_hotkey('esc', self.exit_bot)

    def start_bot(self):
        if not self.context.is_running:
            self.print("[System] Starting workflow...")
            self.context.is_running = True
            self.context.is_paused = False
            
            # DEFINE THE WORKFLOW DYNAMICALLY (Instead of hardcoded loops)
            workflow =[
                WaitAndClickTemplateAction('templates/start_button.png', timeout=60),
                YOLOInteractAction('enemy_character', timeout=30)
            ]
            self.engine.load_workflow(workflow)
            
            # Run engine in background to not block hotkeys
            threading.Thread(target=self.engine.execute, daemon=True).start()
        elif self.context.is_paused:
            self.print("[System] Resuming workflow...")
            self.context.is_paused = False

    def stop_bot(self):
        self.print("[System] Pausing workflow...")
        self.context.is_paused = True

    def exit_bot(self):
        self.print("[System] Shutting down...")
        self.context.is_running = False

# The rest of __main__ execution remains the same, interfacing with app_ui.py