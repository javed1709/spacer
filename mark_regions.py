from customtkinter import CTk, CTkButton, CTkLabel, CTkTabview
import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector

points = []

class SelectFromCollection(object):
    def __init__(self, ax):
        self.canvas = ax.figure.canvas
        self.poly = PolygonSelector(ax, self.onselect)

    def onselect(self, verts):
        global points
        points = verts
        self.canvas.draw_idle()

    def disconnect(self):
        self.poly.disconnect_events()
        self.canvas.draw_idle()

def onkeypress(event):
    global points
    if event.key == 'n': 
        pts = np.array(points, dtype=np.int32)   
        if len(set(map(tuple, pts))) == 4:
            # Calculate and print the height and width of the quadrilateral
            height = np.max(pts[:, 1]) - np.min(pts[:, 1])
            width = np.max(pts[:, 0]) - np.min(pts[:, 0])
            dimensions.set(f"Height: {height}, Width: {width}")

def open_image():
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(rgb_image)

    selector = SelectFromCollection(ax)
    plt.connect('key_press_event', onkeypress)
    plt.show()
    selector.disconnect()

app = CTk()
app.geometry("500x400")
app.config(bg="pink")

tabview = CTkTabview(master=app,bg_color="white",fg_color="white")
tabview.pack(padx=20, pady=20)
#tabview.config(tab_bg="red")

tabview.add("Image Selection")

open_button = CTkButton(master=tabview.tab("Image Selection"), text="Open Image", command=open_image)
open_button.pack(padx=20, pady=20)

dimensions = tk.StringVar()
dimensions.set("Dimensions will be displayed here")

dimensions_label = CTkLabel(master=tabview.tab("Image Selection"), textvariable=dimensions)
dimensions_label.pack(padx=20, pady=20)

app.mainloop()




