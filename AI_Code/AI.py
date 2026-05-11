import cv2
import mediapipe as mp
import time
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture
cap = cv2.VideoCapture(0)
# Set the width and height of the video capture
cap.set(3, 1280)
cap.set(4, 720)

def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def get_finger_values(hand_landmarks):
    landmarks = hand_landmarks.landmark

    wrist = landmarks[mp_hands.HandLandmark.WRIST]
    middle_mcp = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    # Scale helps ignore hand moving closer/farther from camera
    hand_scale = distance(wrist, middle_mcp) #converts "landmark" to "float" as well

    finger_tips = {
        "thumb": landmarks[mp_hands.HandLandmark.THUMB_TIP],
        "index": landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
        "middle": landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
        "ring": landmarks[mp_hands.HandLandmark.RING_FINGER_TIP],
        "pinky": landmarks[mp_hands.HandLandmark.PINKY_TIP],
    }

    values = {}

    for finger, tip in finger_tips.items():
        values[finger] = distance(tip, wrist) / hand_scale

    return values




def countdown():
    start_time = time.time()
    checkC = 0
    while True:
        success, img = cap.read()

        while not success and checkC < 5:
                        time.sleep(1)  # Wait for a moment before retrying
                        print("Failed to capture video. Retrying...")
                        success, img = cap.read()
                        checkC += 1
        if not success:
            print("Failed to capture video after multiple attempts. Exiting.")
            return False
       
        elapsed_time = time.time() - start_time
        remaining_time = 5 - int(elapsed_time)
        if remaining_time <= 0:
            break
        img = cv2.flip(img, 1)
        cv2.putText(img, "Starting in: " + str(remaining_time), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Display the countdown timer on the image
        cv2.putText(img, "Please put your hand in the starting position", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2) # Display an instruction message on the image
        

        cv2.putText(img, "Initializing hand tracking... please put hand in perfered starting position", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2) # Display an initialization message on the image
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return True
        
        
        


def main():


    
    # Use MediaPipe Hands to process the video feed
    with mp_hands.Hands(

        max_num_hands=1,
        
        # Set the minimum detection confidence and tracking confidence to 0.7 for better performance
        min_detection_confidence=0.7, 
        
        min_tracking_confidence=0.7

        ) as hands:
            countdown() # Start the countdown before processing the video feed
            
            success, img = cap.read() # Read a frame from the video feed
            img = cv2.flip(img, 1)  # Flip the image horizontally for a
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert the image to RGB format for MediaPipe
            results = hands.process(rgb_img) # Process the image and find hands
            Starting_position = get_finger_values(results.multi_hand_landmarks[0]) if results.multi_hand_landmarks else None

            while True:
                success, img = cap.read() # Read a frame from the video feed
                img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect
                
                #get image dimensions (used for later calculations)
                h, w, _ = img.shape

                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert the image to RGB format for MediaPipe

                results = hands.process(rgb_img) # Process the image and find hands

                # print (Starting_position) # Print the initial finger values to the console for debugging purposes
                if results.multi_hand_landmarks: # If hands are detected
                    position = get_finger_values(results.multi_hand_landmarks[0]) # Get the current finger values (not used in this code but can be used for further processing)

                    for hand_landmarks in results.multi_hand_landmarks: # For each hand detected
                        mp_drawing.draw_landmarks(img, 
                                                  hand_landmarks, 
                                                  mp_hands.HAND_CONNECTIONS
                                                  ) # Draw the hand landmarks on the image
                        finger_tips = {
                            "thumb": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                            "index": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                            "middle": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                            "ring": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                            "pinky": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                        }
                        for name, landmark in finger_tips.items():
                            x = int(landmark.x * w) # Convert the normalized landmark coordinates to pixel coordinates
                            y = int(landmark.y * h)
                            cv2.putText(img, 
                                        name + ": " + str(x) + ", " + str(y), (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1) # Label the fingertip with its coordinates on the image
                            cv2.circle(img, (x, y), 5, (0, 255, 0), cv2.FILLED) # Draw a circle at the fingertip position
                        
                #show the image
                cv2.imshow("Image", img)
                #print ("distence of pointer from original position: " + str(Starting_position["index"] - position["index"])) # Print the distance of the index fingertip from its original position to the console for debugging purposes

                #break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    


if __name__ == "__main__":
    main()