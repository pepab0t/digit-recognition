from tkinter import *
from tkinter import ttk
from PIL import Image
import threading
import tensorflow as tf
import cv2
import numpy as np

class MainWindow(Tk):
    def __init__(self, app_width, app_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f'{app_width}x{app_height}+{int(self.winfo_screenwidth()/2-app_width/2)}+{int(self.winfo_screenheight()/2 - app_height/2)}')
        self.resizable(False, False)

        self.lastx, self.lasty = 0,0
        self.running = False
        self.model = tf.keras.models.load_model('digit_quesser.model')

        # self.grid_rowconfigure(0, weight=4)
        # self.grid_rowconfigure(1,weight=2)
        # self.grid_rowconfigure(2,weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.frame_canvas = Frame(self, bg='gray', pady=0, padx=0)
        self.frame_canvas.grid(row=0, column=1, sticky='nsew')
        self.frame_canvas.grid_columnconfigure(1, weight=1)
        # self.frame_canvas.grid_rowconfigure(0, weight=1)
        # self.frame_canvas.grid_rowconfigure(1, weight=4)
        # self.frame_canvas.grid_rowconfigure(2, weight=1)

        self.frame_buttons = Frame(self, bg='green')
        self.frame_buttons.grid(row=1, column=1, sticky='nsew')
        self.frame_buttons.grid_columnconfigure(0, weight=1)
        self.frame_buttons.grid_columnconfigure(1, weight=1)
        self.frame_buttons.grid_columnconfigure(2, weight=1)

        self.label_title = ttk.Label(self.frame_canvas, text='Digit recognition', anchor='center')
        self.label_title.grid(row=0, column=1, sticky='wens')
        
        self.canvas = Canvas(self.frame_canvas, background='white', width=300, height=300, cursor='dot')
        self.canvas.grid(row=1, column=1, pady=0)
        self.canvas.bind('<Button-1>', self.locate)
        self.canvas.bind('<B1-Motion>', self.draw)

        self.label_prediction = ttk.Label(self.frame_canvas, anchor='center', text='')
        self.label_prediction.grid(row=2, column=1, sticky='nsew')

        self.button_quess = ttk.Button(self.frame_buttons, width=10, text='QUESS', command=self.quess)
        self.button_quess.grid(row=1, column=0)

        self.button_clear = ttk.Button(self.frame_buttons, width=10, text='CLEAR', command=self.clear)
        self.button_clear.grid(row=1, column=1)

        self.button_quit = ttk.Button(self.frame_buttons, width=10, text='QUIT', command=self.destroy)
        self.button_quit.grid(row=1, column=2)

        self.check()

    def locate(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, e):
        x, y = e.x, e.y
        self.canvas.create_line((self.last_x, self.last_y, x, y), capstyle=ROUND, width=20)
        self.last_x, self.last_y = x, y

    def clear(self):
        self.canvas.delete('all')

    def quess(self):
        self.running = True
        
        self.canvas.postscript(file = 'digit.eps') 
        # use PIL to convert to PNG 
        img = Image.open("digit.eps")
        img = img.resize((28, 28), Image.ANTIALIAS)
        img.save('digit.png')

        digit = cv2.imread('digit.png')[:,:,0]
        digit = np.invert(np.array([digit]))

        prediction = self.model.predict(digit)
        print(np.argmax(prediction))

        self.running = False

    def check(self):
        pass
        # if self.running:
        #     self.button_quess['state'] = 'disabled'
        # else:
        #     self.button_quess['state'] = 'normal'
        # self.after(50, self.check)

root = MainWindow(500, 400)
root.configure(background='yellow')

root.mainloop()