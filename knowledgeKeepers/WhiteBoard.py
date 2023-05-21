from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create a blank white image
image = 255 * np.ones((1000, 1200, 3), dtype=np.uint8)

# Create a window to display the image
cv2.namedWindow('Whiteboard')

# Set up mouse event handlers
def mouse_handler(event, x, y, flags, param):
    global image

    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing a line
        cv2.circle(image, (x, y), 20, (0, 0, 0), -20)
        cv2.imshow('Whiteboard', image)

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # Continue drawing the line
        cv2.circle(image, (x, y), 20, (0, 0, 0), -20)
        cv2.imshow('Whiteboard', image)

    elif event == cv2.EVENT_LBUTTONUP:
        # Stop drawing the line
        cv2.circle(image, (x, y), 20, (0, 0, 0), -20)
        cv2.imshow('Whiteboard', image)
        

    elif event == cv2.EVENT_LBUTTONDBLCLK:
        # Preprocess the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Extract text from the preprocessed image using Tesseract OCR
        text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789+-/*= ')

        # Print the extracted text
        print(text)

        
        # Close the whiteboard window
        cv2.destroyAllWindows()

cv2.setMouseCallback('Whiteboard', mouse_handler)

# Display the whiteboard and wait for user input
cv2.imshow('Whiteboard', image)
cv2.waitKey(0)