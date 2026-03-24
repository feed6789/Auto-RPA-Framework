import keyboard
import time
import threading
import random
from vision_engine import VisionEngine
from human_controller import HumanController

class AutomationBot:
    def __init__(self):
        # Initialize components
        # IMPORTANT: Provide the path to your trained YOLOv8 model here.
        self.vision = VisionEngine(yolo_model_path="models/best.pt") 
        self.controller = HumanController()
        
        # State management
        self.is_running = False
        self.is_exiting = False
        
        # Timers for micro-breaks
        self.break_timer = time.time()
        self.break_duration = 0
        self.next_break_interval = random.uniform(300, 600) # Break every 5-10 minutes
        self.print = print 

    def setup_hotkeys(self):
        """Sets up global hotkeys for controlling the bot."""
        keyboard.add_hotkey('F9', self.start_bot)
        keyboard.add_hotkey('F10', self.stop_bot)
        keyboard.add_hotkey('esc', self.exit_bot)
        self.print("[System] Hotkeys registered: F9=Start | F10=Pause | ESC=Exit")

    def start_bot(self):
        if not self.is_running:
            self.print("[Bot] Starting...")
            self.is_running = True
            self.break_timer = time.time()
            self.next_break_interval = random.uniform(300, 600)

    def stop_bot(self):
        if self.is_running:
            self.print("[Bot] Paused.")
            self.is_running = False

    def exit_bot(self):
        self.print("[System] Exit command received. Shutting down...")
        self.stop_bot()
        self.is_exiting = True

    def take_micro_break(self):
        """Simulates a human taking a short break."""
        self.break_duration = random.uniform(15, 45) # Break for 15-45 seconds
        self.print(f"[Bot] Taking a micro-break for {self.break_duration:.1f} seconds.")
        time.sleep(self.break_duration)
        self.break_timer = time.time() # Reset timer after break
        self.next_break_interval = random.uniform(300, 600) # Schedule next break
        self.print("[Bot] Resuming activity.")

    def main_loop(self):
        """The core logic loop of the bot, runs continuously in a separate thread."""
        self.print("[System] Main loop started. Use the UI or F9 to begin.")
        
        while not self.is_exiting:
            if not self.is_running:
                time.sleep(0.1) # Idle efficiently when paused
                continue

            # --- Micro-break Logic ---
            if time.time() - self.break_timer > self.next_break_interval:
                self.take_micro_break()
                continue

            # --- Main Automation Logic ---
            try:
                # 1. Capture the screen
                screen = self.vision.capture_screen()

                # 2. Example: Find a static UI button with template matching
                button_pos = self.vision.find_template(screen, 'templates/start_button.png', confidence=0.85)
                if button_pos:
                    self.print(f"[Action] Found UI button at {button_pos}. Clicking it.")
                    self.controller.move_to(button_pos[0], button_pos[1])
                    self.controller.click()
                    time.sleep(random.uniform(1.0, 2.5)) # Wait after action
                    continue

                # 3. Example: Use YOLO to find dynamic objects (e.g., enemies)
                detected_enemies = self.vision.detect_objects_yolo(screen)
                if detected_enemies:
                    # Target the first detected enemy
                    target = detected_enemies[0]
                    self.print(f"[Action] YOLO detected '{target['label']}' at {target['center']}.")
                    self.controller.move_to(target['center'][0], target['center'][1])
                    self.controller.click()
                    time.sleep(random.uniform(0.5, 1.2))
                    continue
                
                # 4. Example: Use OCR to read HP from a specific region
                hp_region = screen[800:850, 100:250] # Example coordinates [y1:y2, x1:x2]
                text_results = self.vision.read_text_ocr(hp_region)
                for text in text_results:
                    if '%' in text or '/' in text:
                        self.print(f"[OCR] Detected HP: {text}")
                        # Add logic here, e.g., if HP is low, use a potion.

                # #detected objects 
                # detected_objects = self.vision.detect_objects_yolo(screen)
                # if detected_objects:
                #     # Your logic here, e.g., target the first object
                #     target = detected_objects[0]
                #     self.print(f"Detected a '{target['label']}' at {target['center']}")
                #     self.controller.move_to(target['center'][0], target['center'][1])
                
                # If no actions are taken, wait a bit to avoid maxing out CPU
                time.sleep(0.1)
                
            except Exception as e:
                self.print(f"[Error] An exception occurred in the main loop: {e}")
                self.stop_bot()
                time.sleep(5) # Wait before trying again


if __name__ == "__main__":
    bot = AutomationBot()
    bot.setup_hotkeys()

    # Run the bot's main loop in a background thread to keep the main thread
    # free for handling hotkey events.
    bot_thread = threading.Thread(target=bot.main_loop, daemon=True)
    bot_thread.start()

    # Keep the main script alive to listen for the exit command
    while not bot.is_exiting:
        time.sleep(1)

    print("[System] Shutdown sequence complete.")