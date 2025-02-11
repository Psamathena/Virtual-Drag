import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
prev_time = 0
is_dragging = False
drag_start_pos = None

# Set up mouse control parameters
smoothening = 5
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

# Adjust these values based on your camera setup
frame_reduction = 100
cam_width = 640
cam_height = 480
cap.set(3, cam_width)
cap.set(4, cam_height)
class BlockDragDrop:
    def __init__(self):
        # Initialize blocks with their properties
        self.blocks = [
            {"rect": (100, 100, 100, 100), "color": (0, 0, 0), "dragging": False},
            {"rect": (250, 100, 100, 100), "color": (0, 0, 0), "dragging": False}, 
            {"rect": (100, 250, 100, 100), "color": (0, 0, 0), "dragging": False},
            {"rect": (250, 250, 100, 100), "color": (0, 0, 0), "dragging": False}
        ]
        self.grab_threshold = 40  # Distance threshold for grab detection

    def process_frame(self, img, hand_landmarks):
        """Process a single frame with hand landmarks"""
        img = cv2.flip(img, 1)  # Flip image horizontally
        
        # Draw the blocks
        for block in self.blocks:
            x, y, w, h = block["rect"]
            cv2.rectangle(img, (x, y), (x+w, y+h), block["color"], -1)
        
        if hand_landmarks:
            self._handle_hand_interaction(img, hand_landmarks)
            
        return img

    def _handle_hand_interaction(self, img, hand):
        """Handle hand interaction with blocks"""
        # Get index and thumb finger positions
        index_x = int(hand.landmark[8].x * cam_width)
        index_y = int(hand.landmark[8].y * cam_height)
        thumb_x = int(hand.landmark[4].x * cam_width)
        thumb_y = int(hand.landmark[4].y * cam_height)
        
        # Calculate distance between fingers
        finger_distance = ((thumb_x - index_x)**2 + (thumb_y - index_y)**2)**0.5
        
        # Visual feedback for finger positions
        cv2.circle(img, (index_x, index_y), 10, (255, 0, 0), -1)
        cv2.circle(img, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
        
        # Check for grabbing gesture
        is_grabbing = finger_distance < self.grab_threshold
        
        self._update_blocks(index_x, index_y, is_grabbing)

    def _update_blocks(self, finger_x, finger_y, is_grabbing):
        """Update block positions based on finger interaction"""
        for block in self.blocks:
            x, y, w, h = block["rect"]
            
            # Check if fingers are over the block
            if x < finger_x < x+w and y < finger_y < y+h:
                if is_grabbing:
                    block["dragging"] = True
                    # Update block position based on finger movement
                    new_x = max(0, min(cam_width - w, finger_x - w//2))
                    new_y = max(0, min(cam_height - h, finger_y - h//2))
                    block["rect"] = (new_x, new_y, w, h)
                else:
                    block["dragging"] = False

def main():
    try:
        # Initialize the block drag and drop system
        block_system = BlockDragDrop()
        prev_time = time.time()  # Initialize prev_time locally
        
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to get frame from camera")
                break
                
            # Process hand detection
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            
            # Process frame with hand landmarks if detected
            hand_landmarks = results.multi_hand_landmarks[0] if results.multi_hand_landmarks else None
            img = block_system.process_frame(img, hand_landmarks)
            
            # Display FPS
            curr_time = time.time()
            fps = 1/(curr_time-prev_time)
            prev_time = curr_time  # Update prev_time
            cv2.putText(img, f'FPS: {int(fps)}', (10, 70), 
                       cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            
            # Show the image
            cv2.imshow("Block Drag and Drop", img)
            
            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

