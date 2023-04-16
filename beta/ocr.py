import cv2
import pytesseract

def read_text_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilate = cv2.dilate(thresh, kernel, iterations=3)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        roi = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
        if text.strip() in [None, " ", '']:
            continue
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        print(text)
    cv2.imshow('OCR', frame)
