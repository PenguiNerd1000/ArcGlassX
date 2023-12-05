import pytesseract
import easyocr
from spellchecker import SpellChecker
import pyttsx3
import cv2
import matplotlib.pyplot as plt

spell = SpellChecker()

engine = pyttsx3.init()

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rayz1\AppData\Local\Tesseract-OCR\tesseract.exe'


def recognize_handwritten(image):
    text = pytesseract.image_to_string(image)
    return text

def recognize_printed(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    words = text.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_text = ' '.join(corrected_words)
    return corrected_text

def is_handwritten(image):


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)


    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    is_handwritten = False
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        print(aspect_ratio)
        if aspect_ratio < 1:
            return True
        else:
            return False



videocapture = cv2.VideoCapture(0)


while True:

    _, frame = videocapture.read()

   
    if is_handwritten(frame):
        text = recognize_handwritten(frame)
        print("Handwritten")
    else:
        text = recognize_printed(frame)
        print("printed")

    text = correct_spelling(text)
        #speak
    if text:
        engine.say(text)
        engine.runAndWait()

    #show frame
        #show frame
    cv2.imshow('Video', frame)

    #stop when input q is inputted
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



videocapture.release()