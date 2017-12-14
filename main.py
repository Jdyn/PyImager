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
        self.joining = False
        self.degree_text = IntVar()

        self.open_button = Button(master, text='Open Image', command=self.button_open)
        self.open_button.pack(fill=BOTH, side=LEFT)

        self.save_button = Button(master, text='Save Image', command=self.save_button)
        self.save_button.pack(fill=BOTH, side=RIGHT)

        self.canvas = Canvas(master, background='black', highlightthickness=1)
        self.master.resizable(width=False, height=False)
        self.canvas.pack(side=TOP)

        reset_button = Button(master, text='Reset Image', command=self.reset_button)
        reset_button.pack(fill=BOTH, side=BOTTOM)

        crop_button = Button(master, text='Crop Image', command=self.crop_button)
        crop_button.pack(fill=BOTH, side=LEFT, expand=True)

        rotate_button = Button(master, text='Rotate Image', command=self.rotate_button)
        rotate_button.pack(fill=BOTH, side=LEFT, expand=True)

        convert_button1 = Button(master, text='Convert Image', command=self.convert_button, relief="raised")
        convert_button1.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

        flip_button = Button(master, text='Flip Image', command=self.flip_button)
        flip_button.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

        join_button = Button(master, text='Join Image', command=self.join_button)
        join_button.pack(fill=BOTH, padx=1, side=LEFT, expand=True)

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
        self.crop_x = self.crop_y = 0
        self.cropping = True
        if self.cropping is False:
            self.canvas.bind("<ButtonPress-1>", self.nothing)
            self.canvas.bind("<B1-Motion>", self.nothing)
            self.canvas.bind("<ButtonRelease-1>", self.nothing)

        if self.cropping is True:
            self.joining = False
            self.canvas.bind("<ButtonPress-1>", self.crop_button_press)
            self.canvas.bind("<B1-Motion>", self.crop_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.crop_button_release)

            self.crop_rect = None

            self.crop_start_x = None
            self.crop_start_y = None

            self.crop_end_X = None
            self.crop_end_Y = None

    def crop_button_press(self, event):
        if self.cropping is True:
            self.crop_start_x = self.canvas.canvasx(event.x)
            self.crop_start_y = self.canvas.canvasy(event.y)

            self.crop_rect = self.canvas.create_rectangle(self.crop_x, self.crop_y, 1, 1, outline='white')

    def crop_move_press(self, event):
        if self.cropping is True:
            self.crop_cur_X = self.canvas.canvasx(event.x)
            self.crop_cur_Y = self.canvas.canvasy(event.y)

            self.canvas.coords(self.crop_rect, self.crop_start_x, self.crop_start_y, self.crop_cur_X, self.crop_cur_Y)

    def crop_button_release(self, event):
        if self.cropping is True:
            self.crop_end_X = self.canvas.canvasx(event.x)
            self.crop_end_Y = self.canvas.canvasy(event.y)
            self.crop_region = (self.crop_start_x, self.crop_start_y, self.crop_end_X, self.crop_end_Y)

            self.cropped = self.image.crop(self.crop_region)
            self.cropped_photo = ImageTk.PhotoImage(self.cropped)
            self.canvas.itemconfig(self.modded, image=self.cropped_photo)
            self.image = self.cropped
            self.canvas.config(width=self.image.size[0], height=self.image.size[1])
            self.canvas.coords(self.modded, self.image.size[0] / 2, self.image.size[1] / 2)
            print(self.image.size)
            self.canvas.delete(self.crop_rect)
        self.cropping = False

    def convert_button(self):

        if self.switch is True:

            self.colored_image()

            return

        if self.switch is False:
            
            self.greyed_image()

            return

    def colored_image(self):

        if self.switch is True:
            self.switch = False
            print("False")
            self.colored = self.image.convert('RGB')
            self.colored_photo = ImageTk.PhotoImage(self.colored)
            self.canvas.itemconfig(self.modded, image=self.colored_photo)
            print(self.image.mode)

    def greyed_image(self):
        self.switch = True
        print("True")
        self.greyed = self.image.convert('L')
        self.greyed_photo = ImageTk.PhotoImage(self.greyed)
        self.canvas.itemconfig(self.modded, image=self.greyed_photo)
        print(self.image.mode)


    def flip_button(self):
        self.flipped = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.flipped_photo = ImageTk.PhotoImage(self.flipped)
        self.canvas.itemconfig(self.modded, image=self.flipped_photo)
        self.image = self.flipped

    def save_button(self):
        self.image_save = filedialog.asksaveasfilename(defaultextension='.jpg')

        if self.switch is True:
            self.image = self.greyed
            if self.image_save:
                self.image.save(self.image_save)
            return
        if self.switch is False:
            if self.image_save:
                self.image.save(self.image_save)
            return

    def join_button(self):
        self.join_x = self.join_y = 0
        self.joining = True
        if self.joining is False:
            self.canvas.bind("<ButtonPress-1>", self.nothing)
            self.canvas.bind("<B1-Motion>", self.nothing)
            self.canvas.bind("<ButtonRelease-1>", self.nothing)

        if self.joining is True:
            self.cropping = False
            self.canvas.bind("<ButtonPress-1>", self.join_button_press)
            self.canvas.bind("<B1-Motion>", self.join_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.join_button_release)

            self.filePath2 = filedialog.askopenfilename()
            self.image2 = Image.open(self.filePath2)
            self.photo2 = ImageTk.PhotoImage(self.image2)
            # self.join_rect = None

            self.join_start_x = None
            self.join_start_y = None

            self.join_end_X = None
            self.join_end_Y = None

    def join_button_press(self, event):
        if self.joining is True:
            self.join_start_x = self.canvas.canvasx(event.x)
            self.join_start_y = self.canvas.canvasy(event.y)

            self.modded2 = self.canvas.create_image(self.join_start_x, self.join_start_y, image=self.photo2)
            # self.join_rect = self.canvas.create_rectangle(self.join_x, self.join_y, 1, 1, outline='white')

    def join_move_press(self, event):
        if self.joining is True:
            self.join_cur_X = int(self.canvas.canvasx(event.x))
            self.join_cur_Y = int(self.canvas.canvasy(event.y))

            self.canvas.coords(self.modded2, self.join_cur_X, self.join_cur_Y)

    def join_button_release(self, event):
        if self.joining is True:
            self.crop_end_X = int(self.canvas.canvasx(event.x))
            self.crop_end_Y = int(self.canvas.canvasy(event.y))
            self.position = (self.join_cur_X - (self.image2.width // 2), self.join_cur_Y - (self.image2.height // 2))

            self.image_copy = self.image.paste(self.image2, self.position)
            self.image.show()
root = Tk()
m = Main(root)

root.mainloop()
