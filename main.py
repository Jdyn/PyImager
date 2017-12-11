from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image


class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("PyImager")
        self.showing_degree = False
        self.cropping = False
        self.switch = False
        self.degree_text = IntVar()

        self.open_button = Button(master, text='Open Image', command=self.button_open)
        self.open_button.pack(fill=BOTH, side=LEFT)

        self.save_button = Button(master, text='Save Image', command=self.save_button)
        self.save_button.pack(fill=BOTH, side=RIGHT)

        self.canvas = Canvas(master, background='black', highlightthickness=1)
        self.master.resizable(width=False, height=False)
        self.canvas.pack(side=TOP)

        self.reset_button = Button(master, text='Reset Image', command=self.reset_button)
        self.reset_button.pack(fill=BOTH, side=BOTTOM)

        self.crop_button = Button(master, text='Crop Image', command=self.crop_button)
        self.crop_button.pack(fill=BOTH, side=LEFT, expand=True)

        self.rotate_button = Button(master, text='Rotate Image', command=self.rotate_button)
        self.rotate_button.pack(fill=BOTH, side=LEFT, expand=True)

        self.convert_button1 = Button(master, text='Convert Image', command=self.convert_button, relief="raised")
        self.convert_button1.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

        self.flip_button = Button(master, text='Flip Image', command=self.nothing)
        self.flip_button.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

        self.join_button = Button(master, text='Join Image', command=self.nothing)
        self.join_button.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

    def nothing(self):
        pass

    def button_open(self):
        self.filePath = filedialog.askopenfilename()
        if self.filePath:
            self.image = Image.open(self.filePath)
            self.photo = ImageTk.PhotoImage(self.image)
            self.modded = self.canvas.create_image(self.image.size[0] / 2, self.image.size[1] / 2, image=self.photo)
            self.canvas.config(width=self.image.size[0], height=self.image.size[1])
            print(self.image.format)
            print(self.image.size)
            print(self.image.mode)

    def reset_button(self):
        self.canvas.delete(ALL)
        self.cropping = False
        self.image = Image.open(self.filePath)
        self.photo = ImageTk.PhotoImage(self.image)
        self.modded = self.canvas.create_image(self.image.size[0] / 2, self.image.size[1] / 2, image=self.photo)
        self.canvas.config(width=self.image.size[0], height=self.image.size[1])

    def rotate_button(self):
        if self.showing_degree is False:
            self.degree = Label(self.master, text="Degrees")
            self.degree.pack(fill=X, padx=1, side=LEFT)
            self.input = Entry(self.master, textvariable=self.degree_text).pack(fill=X, padx=1, side=LEFT)
        self.master.bind('<Return>', self.record)
        self.showing_degree = True

    def record(self, event):
        self.user = self.degree_text.get()
        # print(self.user)
        self.rotated = self.image.rotate(self.user)
        self.rotphoto = ImageTk.PhotoImage(self.rotated)
        self.canvas.itemconfig(self.modded, image=self.rotphoto)
        self.image = self.rotated
        event.widget.pack_forget()
        self.degree.pack_forget()
        self.master.bind('<Return>', self.nothing)
        self.showing_degree = False

    def crop_button(self):
        self.x = self.y = 0
        self.cropping = True
        if self.cropping is False:
            self.canvas.bind("<ButtonPress-1>", self.nothing)
            self.canvas.bind("<B1-Motion>", self.nothing)
            self.canvas.bind("<ButtonRelease-1>", self.nothing)

        if self.cropping is True:
            self.canvas.bind("<ButtonPress-1>", self.crop_button_press)
            self.canvas.bind("<B1-Motion>", self.crop_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.crop_button_release)

            self.rect = None

            self.start_x = None
            self.start_y = None

            self.end_X = None
            self.end_Y = None

    def crop_button_press(self, event):
        if self.cropping is True:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)

            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='white')

    def crop_move_press(self, event):
        if self.cropping is True:
            self.curX = self.canvas.canvasx(event.x)
            self.curY = self.canvas.canvasy(event.y)

            self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def crop_button_release(self, event):
        if self.cropping is True:
            self.end_X = self.canvas.canvasx(event.x)
            self.end_Y = self.canvas.canvasy(event.y)
            self.crop_region = (self.start_x, self.start_y, self.end_X, self.end_Y)

            self.cropped = self.image.crop(self.crop_region)
            self.cropped_photo = ImageTk.PhotoImage(self.cropped)
            self.canvas.itemconfig(self.modded, image=self.cropped_photo)
            self.image = self.cropped
            self.canvas.delete(self.rect)
        self.cropping = False

    def convert_button(self):

        if self.switch is True:
            self.switch = False
            print("False")
            self.colored = self.image.convert('RGB')
            self.colored_photo = ImageTk.PhotoImage(self.colored)
            self.canvas.itemconfig(self.modded, image=self.colored_photo)
            self.image = self.colored
            print(self.image.mode)
            return

        if self.switch is False:
            self.switch = True
            print("True")
            self.greyed = self.image.convert('L')
            self.greyed_photo = ImageTk.PhotoImage(self.greyed)
            self.canvas.itemconfig(self.modded, image=self.greyed_photo)
            print(self.image.mode)
            return

    def save_button(self):
        self.image_save = filedialog.asksaveasfilename(defaultextension='.jpg')
        if self.switch is True:
            self.image = self.greyed
            if self.image_save:
                self.image.save(self.image_save)
            return
        else:
            if self.image_save:
                self.image.save(self.image_save)
            return


root = Tk()
m = Main(root)

root.mainloop()
