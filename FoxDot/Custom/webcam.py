import cv2
import numpy as np
import threading
from random import shuffle
from collections import deque

class connect:

    # Number of colours -> duration
    # Amount of change  -> degree
    # filter - > centre of mass?

    def __init__(self, server, src=0):
        self.server = server
        self.src = src
        self.fps = 30
        self.cap = None
        self.img = None
        self.queue = []
        self.q_size = 10
        self.display = lambda x: cv2.flip(x, 1)
        self.SynthDef = "pads"

    def __call__(self, *args):
        """ Sends an OSC message to the server """
        #: Extract motion data
        freq = np.count_nonzero(self.motion())

        self.server.sendNote(self.SynthDef, ["freq", freq, "slide", 1, "sus", 8])

        return

    def motion(self, *args):

        dim = self.img.shape

        if len(dim) is 3:
            w, h, rgb = dim
        else:
            w, h = dim

        motion_img = np.zeros((w,h), dtype=np.uint8)

        A = cv2.cvtColor(self.queue[0], cv2.COLOR_BGR2GRAY)

        for i in range(1, len(self.queue)):

            B = cv2.cvtColor(self.queue[i], cv2.COLOR_BGR2GRAY)

            dif = cv2.absdiff(B, A)

            motion_img = cv2.add(motion_img, dif)

            A = B

        r, motion_img = cv2.threshold(motion_img, 200, 255, cv2.THRESH_BINARY)
            
        return motion_img

    def start(self):
        threading.Thread(target=self.run).start()
        return self

    def run(self):

        if self.cap is None:

            self.cap = cv2.VideoCapture(self.src)

        while True:

            # Read from webcam
            
            ret, self.img = self.cap.read()

            # Resize

            self.img = cv2.resize(self.img ,(0,0), fx=0.5, fy=0.5)

            # Store the last few frames

            self.queue = self.queue[(self.q_size * -1):] + [self.img]    

            #: Process the image

            try:
            
                self.img = self.display(self.img)

            except Exception as e:

                print e

            # Show the image

            if ret: cv2.imshow('FoxDot', self.img)
            
            if cv2.waitKey(1000 / self.fps) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
