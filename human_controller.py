import time
import random
import numpy as np
import pytweening
from pynput.mouse import Controller as MouseController, Button

class HumanController:
    """
    Simulates human-like mouse movements and actions.
    - Moves in curved paths (Bezier curves).
    - Varies movement speed using easing functions.
    - Adds random "shivers" and micro-stutters.
    - Clicks at random offsets within a target area.
    - Uses randomized delays for all actions.
    """
    def __init__(self):
        self.mouse = MouseController()

    def _generate_bezier_curve(self, start, end, control_points_num=2):
        """
        Generates a sequence of points for a Bezier curve.
        """
        # Add some randomness to control points to make each curve unique
        pts = [np.array(start)]
        for _ in range(control_points_num):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            mid_point = (np.array(start) + np.array(end)) / 2
            pts.append(mid_point + np.array([x_offset, y_offset]))
        pts.append(np.array(end))
        pts = np.array(pts)

        # Bezier curve formula for n control points
        path = []
        num_steps = 100 # Increase for smoother curves
        for t in np.linspace(0, 1, num_steps):
            n = len(pts) - 1
            point = np.zeros(2)
            for i, p in enumerate(pts):
                bernstein_poly = (
                    np.math.comb(n, i) * (t**i) * ((1 - t)**(n - i))
                )
                point += p * bernstein_poly
            path.append(tuple(point.astype(int)))
            
        return path

    def move_to(self, target_x, target_y, duration_min=0.3, duration_max=0.8):
        """
        Moves the mouse to a target coordinate with human-like motion.
        """
        # Never click the dead center. Apply a random offset.
        target_x += random.randint(-4, 4)
        target_y += random.randint(-4, 4)

        start_pos = self.mouse.position
        path = self._generate_bezier_curve(start_pos, (target_x, target_y))

        duration = random.uniform(duration_min, duration_max)
        
        for i, (px, py) in enumerate(path):
            progress = i / len(path)
            # Use an ease-in-out function for natural acceleration and deceleration
            eased_progress = pytweening.easeInOutQuad(progress)

            # Apply a slight "shiver" to mimic unsteady hand movements
            if random.random() < 0.05: # 5% chance to shiver
                px += random.randint(-1, 1)
                py += random.randint(-1, 1)

            self.mouse.position = (px, py)
            
            # This sleep calculation creates the easing effect
            # Sleep less in the middle of the movement (faster) and more at the ends (slower)
            sleep_time = (duration / len(path)) * (1 - eased_progress * 0.9 + 0.1)
            time.sleep(sleep_time)

    def click(self, button=Button.left):
        """
        Simulates a human-like click with a random delay between press and release.
        """
        hold_time = random.uniform(0.065, 0.145) # 65ms to 145ms
        self.mouse.press(button)
        time.sleep(hold_time)
        self.mouse.release(button)