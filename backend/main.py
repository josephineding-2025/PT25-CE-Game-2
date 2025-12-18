import cv2
import mediapipe as mp
import math
import time
import random

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

class MotionGame:
    def __init__(self):
        self.stage = 1
        self.current_pose_index = 0
        self.time_limit = 10  # Starts at 10s for Stage 1
        self.timer_start = None
        self.total_score = 0
        self.game_over = False
        self.start_game_time = time.time()
        
        # Define poses
        self.pose_definitions = [
            {"name": "1. The Awakening", "check_func": self.check_pose_awakening},
            {"name": "2. The Archer", "check_func": self.check_pose_archer},
            {"name": "3. The Iron Sumo", "check_func": self.check_pose_iron_sumo},
            {"name": "4. Disco Diagonal", "check_func": self.check_pose_disco_diagonal},
            {"name": "5. The Golden Rooster", "check_func": self.check_pose_golden_rooster},
            {"name": "6. The Shell Defence", "check_func": self.check_pose_shell_defence},
            {"name": "7. Ninja Ground Tap", "check_func": self.check_pose_ninja_ground_tap},
            {"name": "8. Supernova X", "check_func": self.check_pose_supernova_x},
        ]
        
        self.current_pose = self.pose_definitions[0]
        self.shuffle_order = [] 

    def reset_game(self):
        """Resets the game state to start over."""
        self.stage = 1
        self.current_pose_index = 0
        self.time_limit = 10
        self.timer_start = None
        self.total_score = 0
        self.game_over = False
        self.current_pose = self.pose_definitions[0]
        self.start_game_time = time.time()
 

    def calculate_distance(self, p1, p2):
        """Calculates the Euclidean distance between two landmarks."""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def calculate_angle(self, a, b, c):
        """Calculates the angle at b given points a, b, c."""
        ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
        return abs(ang) if abs(ang) <= 180 else 360 - abs(ang)

    # --- POSE CHECKS ---

    def check_pose_awakening(self, landmarks):
        """1. The Awakening: Arms raised overhead, creating a circle 'O' shape."""
        score = 0
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        
        # Wrists above Nose
        if lw.y < nose.y and rw.y < nose.y: score += 4
        # Wrists close together
        if self.calculate_distance(lw, rw) < 0.2: score += 4
        # Arms visible
        if lw.visibility > 0.5 and rw.visibility > 0.5: score += 2
        
        return score

    def check_pose_archer(self, landmarks):
        """2. The Archer: Standing sideways, one arm straight, one bent (drawing bow)."""
        score = 0
        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        le = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        re = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        
        # Calculate Elbow Angles
        left_angle = self.calculate_angle(ls, le, lw)
        right_angle = self.calculate_angle(rs, re, rw)
        
        # Check for one straight arm (>150 deg) and one bent arm (<90 deg)
        # Case A: Left Straight, Right Bent
        if left_angle > 150 and right_angle < 90: score += 6
        # Case B: Right Straight, Left Bent
        elif right_angle > 150 and left_angle < 90: score += 6
            
        # Check arm height (should be roughly shoulder level)
        if abs(lw.y - ls.y) < 0.2 or abs(rw.y - rs.y) < 0.2: score += 2
        # Feet should be somewhat apart (standing stance) - basic check
        if ls.visibility > 0.5: score += 2 # Visibility bonus
        
        return score

    def check_pose_iron_sumo(self, landmarks):
        """3. The Iron Sumo: Wide squat, arms hanging down holding dumbbell."""
        score = 0
        lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        rk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Legs wide (Ankles wider than Shoulders/Hips)
        hip_width = abs(lh.x - rh.x)
        ankle_width = abs(la.x - ra.x)
        if ankle_width > hip_width * 1.5: score += 3
        
        # Squat depth (Hips close to Knee Y level)
        if abs(lh.y - lk.y) < 0.3: score += 2
        
        # Arms straight down (Wrists below Hips)
        if lw.y > lh.y and rw.y > rh.y: score += 3
        # Wrists close together (holding dumbbell)
        if self.calculate_distance(lw, rw) < 0.15: score += 2
        
        return score

    def check_pose_disco_diagonal(self, landmarks):
        """4. Disco Diagonal: One arm high, one hand on hip (akimbo)."""
        score = 0
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Case A: Left High, Right Akimbo
        l_high = lw.y < nose.y
        r_akimbo = abs(rw.y - rh.y) < 0.2 # Wrist near hip
        
        # Case B: Right High, Left Akimbo
        r_high = rw.y < nose.y
        l_akimbo = abs(lw.y - lh.y) < 0.2
        
        if (l_high and r_akimbo) or (r_high and l_akimbo):
            score += 8
        elif l_high or r_high:
            score += 4 # Partial points for high arm
            
        if nose.visibility > 0.5: score += 2
        
        return score

    def check_pose_golden_rooster(self, landmarks):
        """5. The Golden Rooster: One leg balance, arms T-pose, hands down."""
        score = 0
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        l_index = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value]
        r_index = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value]

        # One leg raised (Significant Y difference between ankles)
        if abs(la.y - ra.y) > 0.15: score += 3
        
        # Arms Horizontal (Wrists near Shoulder Y)
        if abs(lw.y - ls.y) < 0.15 and abs(rw.y - rs.y) < 0.15: score += 3
        
        # Hands pointing down (Index finger below Wrist Y)
        # Note: Y increases downwards in screen coordinates
        if l_index.y > lw.y and r_index.y > rw.y: score += 4
        
        return score

    def check_pose_shell_defence(self, landmarks):
        """6. The Shell Defence: Crouching tight ball."""
        score = 0
        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        rk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        
        # Compactness: distance between shoulders and knees is small
        dist_l = self.calculate_distance(ls, lk)
        dist_r = self.calculate_distance(rs, rk)
        
        if dist_l < 0.3 and dist_r < 0.3: score += 8
        elif dist_l < 0.4 and dist_r < 0.4: score += 4
            
        if ls.visibility > 0.5: score += 2
        return score

    def check_pose_ninja_ground_tap(self, landmarks):
        """7. Ninja Ground Tap: Side lunge, one hand floor, one hand up."""
        score = 0
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]

        # Check vertical spread of hands (High/Low)
        # One wrist below knee (Low), One wrist above nose (High)
        
        l_low = lw.y > la.y - 0.1 # Near ankle level
        l_high = lw.y < nose.y
        r_low = rw.y > ra.y - 0.1
        r_high = rw.y < nose.y
        
        if (l_low and r_high) or (r_low and l_high): score += 6
        
        # Wide stance check (Ankles apart)
        if abs(la.x - ra.x) > 0.4: score += 4
        
        return score

    def check_pose_supernova_x(self, landmarks):
        """8. Supernova X: Body extended in X shape."""
        score = 0
        lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        
        # Arms V-shape Up: Wrists wider than Shoulders AND Wrists above Shoulders
        arms_wide = abs(lw.x - rw.x) > abs(ls.x - rs.x) * 1.5
        arms_up = lw.y < ls.y and rw.y < rs.y
        if arms_wide and arms_up: score += 5
        
        # Legs V-shape Down: Ankles wider than Hips
        legs_wide = abs(la.x - ra.x) > abs(lh.x - rh.x) * 1.5
        if legs_wide: score += 5
        
        return score

    def next_level(self):
        """Transitions to the next pose or stage."""
        if self.stage == 1:
            self.current_pose_index += 1
            if self.current_pose_index >= len(self.pose_definitions):
                # Transition to Stage 2
                self.stage = 2
                self.time_limit = 3
                self.start_stage_2()
            else:
                # Decrease time limit by 1s until it hits 3s
                self.time_limit = max(3, 10 - self.current_pose_index)
                self.current_pose = self.pose_definitions[self.current_pose_index]
        elif self.stage == 2:
            self.pick_random_pose()

        self.timer_start = time.time()

    def start_stage_2(self):
        """Initialize Stage 2 Shuffle Mode."""
        print("Entering Stage 2: Shuffle Challenge!")
        self.pick_random_pose()

    def pick_random_pose(self):
        """Picks a random pose for Stage 2."""
        self.current_pose = random.choice(self.pose_definitions)

    def update(self, landmarks):
        """Main game logic update per frame."""
        if self.game_over:
            return "GAME OVER", (0, 0, 255)

        if self.timer_start is None:
            self.timer_start = time.time()

        elapsed_time = time.time() - self.timer_start
        mod_time_limit = self.time_limit
        
        time_remaining = self.time_limit - elapsed_time

        if time_remaining <= 0:
            self.game_over = True
            return "TIME'S UP! GAME OVER", (0, 0, 255)

        # Check pose score
        score = self.current_pose["check_func"](landmarks)
        PASS_THRESHOLD = 6
        
        status_text = f"Time: {time_remaining:.1f}s | Score: {score}/10"
        color = (0, 165, 255) # Orange

        if score >= PASS_THRESHOLD:
            # Success!
            self.total_score += score
            status_text = f"MATCH! +{score} pts"
            color = (0, 255, 0) # Green
            print(f"Passed {self.current_pose['name']}! Score: {score}")
            self.next_level()
        
        return status_text, color

def main():
    cap = cv2.VideoCapture(0)
    game = MotionGame()

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting webcam... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        # Default status
        status_text = f"Stage {game.stage}: {game.current_pose['name']}"
        score_color = (255, 255, 255)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            if not game.game_over:
                logic_text, score_color = game.update(results.pose_landmarks.landmark)
                status_text += f" | {logic_text}"
            else:
                status_text = f"GAME OVER! Score: {game.total_score} | Press 'r' to Retry"
                score_color = (0, 0, 255)

        # Draw UI
        cv2.putText(frame, status_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, score_color, 2, cv2.LINE_AA)
        
        # Draw Total Score separate
        cv2.putText(frame, f"Total: {game.total_score}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 215, 0), 2, cv2.LINE_AA)

        cv2.imshow('Motion Detection Game', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and game.game_over:
            game.reset_game()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
