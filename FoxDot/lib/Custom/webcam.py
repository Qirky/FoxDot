""" Import any Python library you have installed """

import cv2
import numpy as np
import threading
from random import shuffle, choice

""" You can use FoxDot library code to make music! """

from ..Midi import midi, miditofreq
from ..Scale import default as scale

class dur:
    def __init__(self, val):
        self.val = val
    def update(self, new):
        self.val = new
        return self
    def __float__(self):
        return float(self.val)

class connect:
    """
        Example of a custom FoxDot module

    """

    def __init__(self, server, src=0):
        self.server = server
        self.src = src
        self.fps = 30
        self.cap = None
        self.img = None
        self.size = (320, 240)
        self.mesh_x = np.array([[range(320)]*240])
        self.mesh_y = np.array([[n]*320 for n in range(240)])
        self.queue = []
        self.q_size = 10
        self.display = lambda x: cv2.flip(x, 1)

        #  How do I want my sounds
        self.SynthDef = "orient"
        self.duration = dur(4)
        self.amp      = 0.5

    def __call__(self, *args):
        """ Sends an OSC message to the server """

        # Extract motion data

        m = self.motion()
        
        motion = np.count_nonzero(m)

        # 1. Amount of motion = shorter notes

        durs = [4.0 / (2**n) for n in range(8)]

        size = self.size[0] * self.size[1]

        QoM = min(1.0, (float(motion) / float(size)))

        i = int(QoM * len(durs))

        self.duration.update(durs[i])

        # 2. Amount of colours = variety in pitch

        #colours = len({tuple(row[0]) for row in self.img[:,:,1:3]})

        colours = choice(range(5))

        # 3. Centre of mass Y = octave (min 0, max 12)

        val = m.sum()
        x_coord = (self.mesh_x*m).sum() / val if motion > 0 else 0
        y_coord = (self.mesh_y*m).sum() / val if motion > 0 else 0

        height = 12 * ((self.size[1] - y_coord) / float(self.size[1]))

        m = midi(scale.pentatonic, octave=int(height), degree=int(colours))
        f = miditofreq(m)

        # 4. Centre of mass X = pan

        p = (2 * ((self.size[0] - x_coord) / float(self.size[0]))) - 1

        p = p if x_coord > 0 else 0

        self.server.sendNote(self.SynthDef, ["freq", f,
                                             "sus" , 4,
                                             "amp" , self.amp,
                                             "pan" , p ])
        
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

            #self.img = cv2.resize(self.img ,(0,0), fx=0.5, fy=0.5)
            self.img = cv2.resize(self.img, self.size)

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
