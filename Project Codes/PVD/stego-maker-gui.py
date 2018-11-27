from Tkinter import *
import ttk
import pvd.pvd
import tkMessageBox
import tkFileDialog as tfd
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import pvd.bit_planes.bit_planes as pvd_bits
import numpy as np
import threading

"""

    AUTHOR: Himanshu Sharma

"""

class Page(Frame):
    # Page class is a standard class to define frames in the Tk() window.
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class BitPlanePage(Page):
    # This Page shows the bit planes. Inherits Page class.
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.configure(background='black')

        self.header = Label(self, text="Bit-Plane Generator", font=("consolas", 30), bg = "#00FF87", fg = "#FF003A").pack(fill=BOTH)

        self.image = Label(self, text="", font=('courier', 20), fg="#83FF00", bg='black')
        self.image.pack()
        
        self.title_header = Label(self, text="Enter plane number (1-8)", font=("consolas", 15), fg = "#00FF87", bg='black').pack()
        self.plane = ttk.Entry(self, width=50)
        self.plane.pack(pady=10)

        self.choose = Button(self, text="Browse", command=self.browse, width=30)
        self.choose.pack()

        self.gen_bit_plane_button = Button(self, text="Generate", command=self.generate_bit_plane, width=30, fg="black", bg="red")
        self.gen_bit_plane_button.pack()
        self.gen_bit_plane_button.config(state="disabled")

        self.goback = Button(self, text="Go Back", command=lambda: main.hp.show(), width=30)
        self.goback.pack()

    def browse(self):
        try:
            f = tfd.askopenfile()
            self.image['text'] = f.name

            if self.image['text'] != "":
                self.gen_bit_plane_button.config(state="normal")
        except AttributeError:
            pass

    def generate_bit_plane(self):
        try:
            if int(self.plane.get()) in range(1, 9):
                bitplane = pvd_bits.generateBitPlane(self.image['text'], int(self.plane.get()))
                plt.imshow(bitplane, cmap='gray')
                plt.show()
            else:
                tkMessageBox.showinfo("Alert", "Bit plane numbers lie in range 1 to 8 and they are integers.")
        except:
            tkMessageBox.showwarning("Alert", "Something is wrong.")

class StegoGeneratorPage(Page):
    # This page is for Stego generation.
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configure(background='black')

        self.header = Label(self, text="Stego-Generator", font=("consolas", 30), bg = "#00FF87", fg = "#FF003A").pack(fill=BOTH)
        
        self.file_chosen = Label(self, text="", font=('courier', 20), fg="#83FF00", bg='black')
        self.file_chosen.pack(pady=5)

        self.message_chosen = Label(self, text="", font=('courier', 20), fg="#FF3A00", bg='black')
        self.message_chosen.pack(pady=5)

        self.block_size = ttk.Entry(self, width=50)
        self.block_size.pack(pady=5)
        self.block_size.insert(END, "Block size goes here...")

        self.browse_button = Button(self, text="Browse Cover Image", command=self.select_cover, width=25)
        self.browse_button.pack()

        self.message_file = Button(self, text="Browse Message Text File", command=self.select_message, width=25)
        self.message_file.pack()

        self.embedd_button = Button(self, text="Embedd", command=lambda: threading.Thread(target=self.hide).start(), width=25
                                    , bg = "red", fg="black")
        self.embedd_button.pack()
        self.embedd_button.config(state="disabled")

        self.goback_button = Button(self, text="Go Back", command=self.goback, width=25)
        self.goback_button.pack()

        Status_Static = Label(self, text="Status", font=('courier', 15), fg="#FF0017", bg='black').pack()
        self.status = Label(self, text="Nothing happening right now...", fg="#00FF87", font=('courier', 12), bg='black')
        self.status.pack()

        self.selected_image = Label(self, bg='black')
        self.selected_image.pack(fill=BOTH, expand=YES)

    def goback(self):
        main.hp.show()

    def resize_photo(self, image, width):
        w, h = image.size
        asp = w*h**(-1)

        new_height = width*asp**(-1)
        image = image.resize((width, int(new_height)), Image.ANTIALIAS)
        return image

    def select_cover(self):
        try:
            f = tfd.askopenfile()
            self.file_chosen['text'] = f.name

            img = Image.open(f.name)
            self.img = self.resize_photo(img, root.winfo_width()-10)
            self.img = ImageTk.PhotoImage(self.img)
            self.selected_image.configure(image = self.img)
            
            if self.message_chosen['text'] != "":
                self.embedd_button.config(state="normal")
        except AttributeError:
            pass

    def select_message(self):
        try:
            f = tfd.askopenfile()
            self.message_chosen['text'] = f.name

            if self.file_chosen['text'] != "":
                self.embedd_button.config(state="normal")
        except AttributeError:
            pass

    def hide(self):
        f = open(self.message_chosen['text'], 'r')
        message = f.read()
        f.close()
        try:
            block = int(self.block_size.get())
            self.status['text'] = "Process initiated. It will take few seconds."
            key = pvd.pvd.pixelate(self.file_chosen['text'], message, block)
            self.status['text'] = "Done"
            tkMessageBox.showinfo("Alert", "Cover image has been encrypted in the same folder. Stego-image: final.final.png")
        except:
            tkMessageBox.showwarning("Alert", "Something is wrong!!")

class StegoDecoderPage(Page):
    # this page is for decoding the stego image.
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.configure(background='black')

        self.header = Label(self, text="Stego-Exposer", font=("consolas", 30), bg = "#00FF87", fg = "#FF003A").pack(fill=BOTH)

        self.file_chosen = Label(self, text="",  font=('courier', 20), fg="#83FF00", bg='black')
        self.file_chosen.pack()

        self.key_chosen = Label(self, text="", font=('courier', 20), fg="#FF3A00", bg='black')
        self.key_chosen.pack()

        self.choose_file = Button(self, text="Choose Stego-Image", command=self.choose_stego, width=25)
        self.choose_file.pack()

        self.choose_key = Button(self, text="Choose Key File", command=self.choose_key_file, width=25)
        self.choose_key.pack()

        self.decode_button = Button(self, text="Decode Image", command=lambda: threading.Thread(target=self.decode).start(), width=25
                             , bg = "red", fg="black")
        self.decode_button.pack()
        self.decode_button.config(state="disabled")

        self.show_image = Button(self, text="Show Image", command=self.display, width=25
                                 , bg = "green", fg="white")
        self.show_image.pack()
        self.show_image.config(state="disabled")

        self.goback_button = Button(self, text="Go Back", command=lambda: main.hp.show(), width=25)
        self.goback_button.pack()

        self.clear = Button(self, text="Clear", command=lambda: self.area.delete('1.0', END), width=25)
        self.clear.pack()

        self.heading = Label(self, text="Decoded text will be displayed here.", font=('courier', 15), fg="#00FF87"
                             , bg='black').pack()
        scrollbar = Scrollbar(self)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.area = Text(self, yscrollcommand = scrollbar.set, bg="#837E7D", fg='black')
        self.area.pack(expand=True, fill='both')
        scrollbar.config(command = self.area.yview)

    def choose_stego(self):
        try:
            f = tfd.askopenfile()
            self.file_chosen['text'] = f.name
            self.img = Image.open(self.file_chosen['text'])

            self.show_image.config(state="normal")
            if self.key_chosen['text'] != "":
                self.decode_button.config(state="normal")
        except AttributeError:
            pass

    def choose_key_file(self):
        try:
            f = tfd.askopenfile()
            self.key_chosen['text'] = f.name

            if self.file_chosen['text'] != "":
                self.decode_button.config(state="normal")
                self.show_image.config(state="normal")
        except AttributeError:
            pass

    def display(self):
        plt.imshow(self.img)
        plt.show()

    def decode(self):
        self.message = pvd.pvd.decode(self.file_chosen['text'], self.key_chosen['text'])
        self.area.delete('1.0', END)
        self.area.insert(END, self.message)

class DevPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.configure(background='black')

        scrollbar = Scrollbar(self)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.area = Text(self, yscrollcommand = scrollbar.set, bg="black", fg='white', bd=0)
        self.area.pack(expand=True, fill='both')
        scrollbar.config(command = self.area.yview)
        self.area.tag_configure("center", justify='center')
        
        abtText = open('about.txt', 'r')
        text = abtText.read()
        abtText.close()
        
        self.area.insert(END, text)
        self.area.configure(state="disabled")
        self.area.tag_add("center", 1.0, "end")

        self.goback_button = Button(self, text="Go Back", command=lambda: main.hp.show(), width=25)
        self.goback_button.pack()
        
class HomePage(Page):
    # Homepage.
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.configure(background='black')

        self.heading = Label(self, text = "Image Steganographer", bg = 'black', font=('consolas', 30), fg="#00FF6C").pack(pady=10)
        self.stego_generator_button = Button(self, text="Stego-Generator", command=lambda: main.sgp.show(), width=19
                                             , bg="white", fg="red", height=5)
        self.stego_generator_button.pack(pady=10)
        self.stego_generator_button.place(x=80, y=90)

        self.stego_decoder_button = Button(self, text="Stego-Exposer", command=lambda: main.sdp.show(), width=19
                                           , bg="white", fg="red", height=5)
        self.stego_decoder_button.pack(pady=10)
        self.stego_decoder_button.place(x=420, y=90)

        self.stego_decoder_button = Button(self, text="Bit Plane Generator", command=lambda: main.bpp.show(), width=19
                                           , bg="white", fg="red", height=5)
        self.stego_decoder_button.pack(pady=10)
        self.stego_decoder_button.place(x=80, y=230)

        self.devbutton = Button(self, text="About this Software", command=lambda: main.dev.show(), width=19
                                           , bg="white", fg="red", height=5)
        self.devbutton.pack(pady=10)
        self.devbutton.place(x=420, y=230)
        
        self.icon_label = Label(self, bg='black')
        self.icon_label.pack()
        self.icon_label.place(x=245, y=400)

        icon = Image.open('logo.png')
        icon = ImageTk.PhotoImage(icon)
        self.icon_label.image = icon
        self.icon_label.configure(image=icon)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.hp = HomePage()
        self.sgp = StegoGeneratorPage()
        self.sdp = StegoDecoderPage()
        self.bpp = BitPlanePage()
        self.dev = DevPage()

        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)

        self.hp.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.sgp.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.sdp.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.bpp.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.dev.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        
        self.hp.show()

if __name__ == '__main__':
    root = Tk()
    root.configure(background='black')
    main = MainView(root)
    main.pack(side = 'top', fill = 'both', expand = True)

    root.wm_geometry('700x650')
    root.resizable(height=0, width=0)

    root.title('Steganographer')

    root.mainloop()
        
