import cv2
import pickle
import cvzone
import numpy as np
import streamlit as st
from PIL import Image
import time
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Spacer",
    page_icon="🚖"
)

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):
    spaceCounter = 0
    vl=[]
    for i,pos in enumerate(posList):
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            vl.append('E' + str(i+1))  # Prefix each slot number with 'E'
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(i+1), (x, y + height - 3), scale=1,
                            thickness=2, offset=0, colorR=color)

    return vl, img, spaceCounter

st.title("Space Sence")

# Create placeholders
image_placeholder = st.empty()
free_space_placeholder = st.sidebar.empty()  # Placeholder for free spaces
st.sidebar.header("Available Spaces")
list_placeholder = st.sidebar.empty()

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    vl, img, spaceCounter = checkParkingSpace(imgDilate)
    img_pil = Image.fromarray(img)
    image_placeholder.image(img_pil, use_column_width=True)  # Update the video placeholder

    # Update the free spaces placeholder
    free_space_placeholder.markdown(f'<h1 style="color: green; font-size: 40px;">Free Spaces: {spaceCounter}/{len(posList)}</h1>', unsafe_allow_html=True)

    # Update the list placeholder
    list_placeholder.empty()
    df = pd.DataFrame(np.array(vl).reshape(-1, 1), columns=['Empty Slots'])  # Convert list to DataFrame
    list_placeholder.dataframe(df)  # Display DataFrame

    time.sleep(0)  # Delay for 30 FPS