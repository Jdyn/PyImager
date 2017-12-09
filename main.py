from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image


class Main:
    def __init__(self, master):
        self.master = master
        self.showing_degree = 0
        self.cropping = 0

        self.canvas = Canvas(master, background='black', highlightthickness=1)
        self.master.resizable(width=False, height=False)
        self.canvas.pack()

        self.degree_text = IntVar()

        open_button = Button(master, text='Open Image', command=self.button_open)
        open_button.pack(fill=X, padx=1, side=LEFT)

        crop_button = Button(master, text='Crop Image', command=self.crop_button)
        crop_button.pack(fill=X, padx=1, side=LEFT)

        rotate_button = Button(master, text='Rotate Image', command=self.rotate_button)
        rotate_button.pack(fill=X, padx=1, side=LEFT)

        reset_button = Button(master, text='Reset Image', command=self.reset_button)
        reset_button.pack(fill=X, padx=1, side=LEFT)

        save_button = Button(master, text='Save Image', command=self.save_button)
        save_button.pack(fill=X, padx=1, side=LEFT)

    def nothing(self):
        pass

    def button_open(self):
        self.filePath = filedialog.askopenfilename()
        self.image = Image.open(self.filePath)
        self.photo = ImageTk.PhotoImage(self.image)
        self.modded = self.canvas.create_image(self.image.size[0] / 2, self.image.size[1] / 2, image=self.photo)
        self.canvas.config(width=self.image.size[0], height=self.image.size[1])
        print(self.image.format)
        print(self.image.size)
        print(self.image.mode)

    def reset_button(self):
        self.canvas.delete(ALL)
        self.cropping = 0
        self.image = Image.open(self.filePath)
        self.photo = ImageTk.PhotoImage(self.image)
        self.modded = self.canvas.create_image(self.image.size[0] / 2, self.image.size[1] / 2, image=self.photo)
        self.canvas.config(width=self.image.size[0], height=self.image.size[1])

    def rotate_button(self):
        if self.showing_degree == 0:
            self.degree = Label(self.master, text="Degrees")
            self.degree.pack(fill=X, padx=1, side=LEFT)
            self.input = Entry(self.master, textvariable=self.degree_text).pack(fill=X, padx=1, side=LEFT)
        self.master.bind('<Return>', self.record)
        self.showing_degree = 1

    def record(self, event):
        self.user = self.degree_text.get()
        print(self.user)
        self.rotated = self.image.rotate(self.user)
        self.rotphoto = ImageTk.PhotoImage(self.rotated)
        self.canvas.itemconfig(self.modded, image=self.rotphoto)
        self.image = self.rotated
        event.widget.pack_forget()
        self.degree.pack_forget()
        self.master.bind('<Return>', self.nothing)
        self.showing_degree = 0
        # self.rotated_image.show()
        # self.rotated_image.save(filedialog.asksaveasfilename())

    def crop_button(self):
        self.x = self.y = 0
        self.cropping = 1
        if self.cropping == 0:
            self.canvas.bind("<ButtonPress-1>", self.nothing)
            self.canvas.bind("<B1-Motion>", self.nothing)
            self.canvas.bind("<ButtonRelease-1>", self.nothing)

        if self.cropping == 1:
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

            self.rect = None

            self.start_x = None
            self.start_y = None

            self.end_X = None
            self.end_Y = None

    def on_button_press(self, event):
        if self.cropping == 1:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)

            # if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='white')

    def on_move_press(self, event):
        if self.cropping == 1:
            self.curX = self.canvas.canvasx(event.x)
            self.curY = self.canvas.canvasy(event.y)

            self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        if self.cropping == 1:
            self.end_X = self.canvas.canvasx(event.x)
            self.end_Y = self.canvas.canvasy(event.y)
            self.crop_region = (self.start_x, self.start_y, self.end_X, self.end_Y)

            self.cropped = self.image.crop(self.crop_region)
            self.cropphoto = ImageTk.PhotoImage(self.cropped)
            self.canvas.itemconfig(self.modded, image=self.cropphoto)
            self.image = self.cropped
            self.canvas.delete(self.rect)
            # self.cropped_image.show()
            # self.cropped_image.save(filedialog.asksaveasfilename())

    def save_button(self):
        self.image_save = filedialog.asksaveasfilename(defaultextension='.jpg')
        self.image.save(self.image_save)


root = Tk()
m = Main(root)

root.mainloop()
