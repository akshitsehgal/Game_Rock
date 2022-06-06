import streamlit as st
import cv2 as cv
import mediapipe as mp
import random

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def get_hand_marks(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range(5,20,4)]):
        return "Rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[9].y>landmarks[12].y and landmarks[5].y>landmarks[8].y:
          return "Scissors"
    else:
        return "Paper"

clock = 0

p1_move = p2_move = None
game_text = ""
success = True
NPC_list = ['Scissors','Paper','Rock']



st.title("Rock Paper Scissors")
run = st.checkbox("Play")
frame_window = st.image([])
vid = cv.VideoCapture(0,cv.CAP_DSHOW)

while run:

    vid.set(cv.CAP_PROP_FRAME_WIDTH, 1080)
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    
    with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
        ret, frame = vid.read()
        if not ret or frame is None: break
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(frame)


        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         mp_drawing.draw_landmarks(frame,
        #                                 hand_landmarks,
        #                                 mp_hands.HAND_CONNECTIONS,
        #                                 mp_drawing_styles.get_default_hand_landmarks_style(),
        #                                 mp_drawing_styles.get_default_hand_connections_style())
        frame = cv.flip(frame,1)

        if 0 <= clock<2:
            success = True
            game_text = "Ready?"
        elif clock < 3: game_text = "3..."
        elif clock < 4: game_text = "2..."
        elif clock < 5: game_text = "1..."
        elif clock < 7: game_text = "GO!"
        elif clock == 7:
            hls = results.multi_hand_landmarks
            if hls:
                p1_move = get_hand_marks(hls[0])
                p2_move = random.choice(NPC_list)
            else:
                success = False
        elif clock < 10:
            if success:
                game_text = f"Player 1 showed {p1_move}. Computer showed {p2_move}."
                if p1_move == "Paper" and p2_move=="Rock":
                    game_text = f"{game_text} Player 1 wins"
                elif p1_move == "Rock" and p2_move=="Scissors":
                    game_text = f"{game_text} Player 1 wins" 
                elif p1_move == "Scissors" and p2_move=="Paper":
                    game_text = f"{game_text} Player 1 wins"
                elif p1_move == p2_move:
                    game_text = f"{game_text} Game Tied"
                else:
                    game_text = f"{game_text} Computer wins"

            else:
                game_text = 'Didn\'t play properly!'

        cv.putText(frame, f'Clock: {clock}',(50,50),cv.FONT_HERSHEY_PLAIN, 2,(0,255,255), 2, cv.LINE_AA)
        cv.putText(frame, game_text,(50,80),cv.FONT_HERSHEY_PLAIN, 2,(0,255,255), 2, cv.LINE_AA)
        clock = (clock + 1) % 10
        if p2_move:
            icon = cv.imread(f"{p2_move}.png")
            icon = cv.resize(icon, (400, 400))
            frame[100:500, 100:500] = icon
        frame_window.image(frame)    

else:
    vid.release()
    cv.destroyAllWindows
    st.write("Stopped")