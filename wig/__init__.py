import tkinter as tk
from PIL import Image, ImageTk
import time, threading, os

sessions = []

screenWidth = None
screenHeight = None
screenCenter = None

def sleep(amt): time.sleep(amt/1000)

class _LoadingScreenVessel:
    def __init__(self, image, dimensions=(650, 390), draggable=False, cursor="wait", 
                    fadein=True, fadein_delayms=10, title="Notitle"):

        global sessions, screenWidth, screenHeight, screenCenter

        self.image = image
        self.root = tk.Tk()

        self.windowexit = 0

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        screenWidth = window_width,
        screenHeight = window_height

        screenCenter = (window_width + window_height) // 2


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

        try:
            image = Image.open(image)
        except:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            image = Image.open("inf.jpg")
        
        image = image.resize((dimensions[0], dimensions[1]), Image.Resampling.LANCZOS)

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


# This up here is the "vessel", basically the main program. We need two classes, one for the core, the second for handling
# functions, threading, etc. since you can't do much after the Tkinter mainloop.
####################################################################


class AddLoadingScreen:
    def __init__(self, image, dimensions=(700, 400), draggable=False, cursor="wait", 
                fadein=True, fadein_delayms=10, title="Notitle"):

        self.vessel = threading.Thread(target=lambda: _LoadingScreenVessel(image, dimensions, draggable, cursor, fadein=fadein, fadein_delayms=fadein_delayms, title=title))
        self.vessel.start()

        time.sleep(0.25)

        try:
            self.session = sessions[-1]
        except IndexError:
            raise IndexError("Fatal error: Could not find session. May be due to an error found inside _LoadScreenVessel.")
        
    def Destroy(self):
        self.session.root.after(0, self.session.root.destroy)

    def ChangeCursor(self, cursor=None):
        self.session.root.config(cursor="arrow" if not cursor else cursor)
    
    def AddText(self, text="Empty textlabel", pos=(0, 0), **args):
        root = self.session.root

        text = tk.Label(root, text=text, **args)
        text.place(x=pos[0], y=pos[1])

        return text

    def AddLoadingBar(self, color="black", height=7, **args):
        root = self.session.root
        dimensions = self.GetScreenDimensions()
        
        self.lbframe = tk.Frame(root, width=0, height=height, background=color, **args)
        self.lbframe.place(x=0, y=dimensions[1]-height)

        self.progress = 0

        print(dimensions[1])

        return self.lbframe

    def UpdateLoadingbar(self, amount):
        self.progress_width = (self.progress / 100) * self.session.root.winfo_width() 

        if self.progress < 100:
            self.progress += amount
            self.lbframe.configure(width=self.progress_width)
            

    def GetScreenDimensions(self):
        screen_width = self.session.root.winfo_width()
        screen_height = self.session.root.winfo_height()

        return (screen_width, screen_height)
    
    def GetWindowPosition(self):
        x = self.session.root.winfo_x
        y = self.session.root.winfo_y()

        return (x, y)

    def SetWindowPosition(self, x, y):
        root = self.session.root
        root.geometry(f"+{x}+{y}")

    def MoveWindow(self, x, y):
        p = self.GetWindowPosition()

        root = self.session.root
        root.geometry(f"+{x+p[0]}+{y+p[1]}")

    def SetTitleText(self, text): self.session.root.title(text)
    def SetDecorationMenuEnabled(self, io): self.session.root.overrideredirect(not io)

    def GetRoot(self): return self.session.root
