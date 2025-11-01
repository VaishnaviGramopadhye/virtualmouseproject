import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr

# Initialize
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

# Voice recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

def voice_control():
    with mic as source:
        print("🎤 Listening for voice commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=3)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("Voice Command:", command)

        # Move mouse based on voice
        if "up" in command:
            pyautogui.moveRel(0, -50)
        elif "down" in command:
            pyautogui.moveRel(0, 50)
        elif "left" in command:
            pyautogui.moveRel(-50, 0)
        elif "right" in command:
            pyautogui.moveRel(50, 0)
        elif "click" in command:
            pyautogui.click()

    except sr.UnknownValueError:
        print("❌ Could not understand voice")
    except sr.RequestError:
        print("⚠️ Speech Recognition service error")


while True:
    ret, frame = cap.read()

    if not ret:  
        print("📷 Webcam not detected. Switching to Voice Control...")
        voice_control()
        continue

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  # Index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:  # Thumb
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Hand Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit with 'q'
        break

cap.release()
cv2.destroyAllWindows()
