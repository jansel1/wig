import tkinter as tk
from PIL import Image, ImageTk
import time, threading, os

sessions = []

class _LoadingScreenVessel:
    def __init__(self, image, dimensions=(500, 280), draggable=False, cursor="wait", 
                    fadein=True, fadein_delayms=10):

        global sessions

        self.image = image
        self.root = tk.Tk()

        self.windowexit = 0

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (dimensions[0] // 2)
        y = (screen_height // 2) - (dimensions[1] // 2)

        self.root.geometry(f"{dimensions[0]}x{dimensions[1]}+{x}+{y}")

        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        self.root.focus()
        self.root.bind("<Control-KeyRelease>", self.HandleWindowExit)

        self.root.config(cursor="wait")

        if draggable:
            self.root.bind("<ButtonPress-1>", self.start_drag)
            self.root.bind("<B1-Motion>", self.do_drag)

        image = Image.open(image)
        image = image.resize((dimensions[0], dimensions[1]))

        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.root, image=photo)
        image_label.place(x=0, y=0, width=dimensions[0], height=dimensions[1])

        sessions.append(self)
        if fadein: self.AnimationHandler_FadeIn(0.0, delayms=fadein_delayms)

        self.root.mainloop()

    def HandleWindowExit(self, x):
        self.windowexit += 1
        if (self.windowexit > 2):
            self.windowexit = 0

            self.root.destroy()
            quit()
    
    def AnimationHandler_FadeIn(self, i, delayms=10):
        if i < 1.0:
            self.root.attributes("-alpha", round(i, 1))
            self.root.after(delayms, self.AnimationHandler_FadeIn, i + 0.1)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")


####################################################################


class AddLoadingScreen:
    def __init__(self, image, dimensions=(500, 280), draggable=False, cursor="wait", 
                fadein=True, fadein_delayms=10):

        self.vessel = threading.Thread(target=lambda: _LoadingScreenVessel(image, dimensions, draggable, cursor, fadein=fadein, fadein_delayms=fadein_delayms))
        self.vessel.start()

        time.sleep(0.25)

        self.session = sessions[-1]
    
    def Destroy(self):
        self.session.root.after(0, self.session.root.destroy)

    def ChangeCursor(self, cursor=None):
        self.session.root.config(cursor="arrow" if not cursor else cursor)