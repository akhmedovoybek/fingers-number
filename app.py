import cv2
from utils import Finger_counter
from AppOpener import open
import speech_recognition as sr

def demostration():
    r = sr.Recognizer()
    # Creating instances
    finger_counter = Finger_counter()
    cap = cv2.VideoCapture(0)

    # looping through the video frame by frame
    name_index = 0
    while (cap.isOpened()):

        # reading the captured images
        ret , frame = cap.read() # reading Frame 
        
        # checking if the frame is empty
        if not ret: break

        # Find out the finger count which is upen the hand
        drawn_image, finger_count = finger_counter.count_fingers(frame)


        # displaying the results
        cv2.imshow("Finger Counter", drawn_image) # showing Video 

        # taking the keyboard key
        k = cv2.waitKey(1)

        # exit condition
        if  k == ord("q"): 
            break

        # saving the images
        if k == ord("s"):
            cv2.imwrite(f"hand_counted_{name_index}.jpg", drawn_image)
            name_index += 1
        # with sr.Microphone() as source:
        #     audio_data = r.listen(source)
        #     try:
        #         text = r.recognize_google(audio_data)
        #         print("Speech: "+text)
        #     except sr.UnknownValueError:
        #         print("Google Speech Recognition could not understand the audio")
        #     except sr.RequestError as e:
        #         print("Could not request results from Google Speech Recognition service; {0}".format(e))
    # re-allocating the sources
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    demostration()