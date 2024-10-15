from tkinter import *
import re
from tkinter import messagebox, font, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import datetime
from database import DataBase
from utils import *


class UserAdmin(Tk):
    ASSETS_PATH = "assets\\frame1\\"
    def __init__(self):
        super().__init__()
        # Requirements
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))


        # Configuring Window
        self.geometry(f"700x550+{int(self.winfo_screenwidth()/2  - 700/2)}+{int(self.winfo_screenheight()/2  - 550/2)}")
        self.configure(bg="#262626")
        self.title("BookNest")
        self.iconbitmap('assets\\icon.ico')
        self.resizable(False, False)


        self.create_page()
        self.mainloop()

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def user_click(self):
        App.USER = "USER"
        self.destroy()
        SignIU()

    def admin_click(self):
        App.USER = "ADMIN"
        self.destroy()
        SignIU()

    def create_page(self):
        canvas = Canvas(self, bg="#262626", height=550, width=700, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_rectangle(0.0, 0.0, 700.0, 81.0, fill="#04A67F", outline="")
        canvas.create_text(268.0,18.0, anchor="nw", text="Book Nest", fill="#FFFFFF", font=("Roboto", 25, 'bold'))

        canvas.create_image(28.0, 43.0, image=self.image_1)
        canvas.create_image(349.0, 300.0, image=self.image_2)

        user_button = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.user_click, relief="flat", background="#292929", activebackground='#292929')
        user_button.place(x=268, y=278, width=162, height=44)

        admin_button = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.admin_click, relief="flat", background="#292929", activebackground='#292929')
        admin_button.place(x=268, y=352, width=162, height=44)

class SignIU(Tk):
    ASSETS_PATH = "assets\\frame2\\"

    def __init__(self):
        super().__init__()
        self.cur_page = 'SIGNUP'
        self.canvas = None
        self.right_heading = None
        self.right_msg = None
        self.left_heading = None
        self.left_msg1 = None
        self.left_msg2 = None
        self.entry_name = None
        self.entry_email = None
        self.entry_password = None
        self.signup_btn = None
        self.signin_btn = None
        self.name_wid1 = None
        self.name_wid2 = None

        # Requirements
        self.image_email = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_name = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_password = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_left_bg = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_shapes = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_circle = PhotoImage(file=self.relative_to_assets("image_6.png"))

        self.entry_image = PhotoImage(file=self.relative_to_assets("entry.png"))

        self.button_signup_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_signin_1 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_signin_2 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_signup_2 = PhotoImage(file=self.relative_to_assets("button_4.png"))


        # Configuring Window
        self.geometry(f"917x580+{int(self.winfo_screenwidth()/2  - 917/2)}+{int(self.winfo_screenheight()/2  - 580/2)}")
        self.configure(bg="#262626")
        self.title("BookNest")
        self.iconbitmap('assets\\icon.ico')
        self.resizable(False, False)

        self.create_page()
        if App.USER == "ADMIN":
            self.sign_in(rm_left=True)
        self.mainloop()

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def sign_in(self, rm_left=False):
        if self.cur_page == "SIGNUP":
            self.cur_page = "SIGNIN"
            self.canvas.itemconfig(self.left_heading, text="Welcome Back!")
            self.canvas.coords(self.left_heading, 59, 190)

            self.canvas.itemconfig(self.left_msg1, text="To keep connected with us please")
            self.canvas.coords(self.left_msg1, 60, 250)

            self.canvas.itemconfig(self.left_msg2, text="login with your personal info")
            self.canvas.coords(self.left_msg2, 75, 270)

            self.canvas.itemconfig(self.right_heading, text="Enter Credentials")

            self.canvas.itemconfig(self.right_msg, text="use your email to login")
            self.canvas.coords(self.right_msg, 585, 231)

            if not rm_left:
                self.signup_btn.config(image=self.button_signup_2, activebackground='#04A67F', background='#04A67F')
                self.signup_btn.place(x=100, y=317, width=145, height=50)

            self.signin_btn.config(image=self.button_signin_2, activebackground='#262626', background="#262626")
            self.signin_btn.place(x=552, y=470, width=200, height=52)

            self.canvas.itemconfig(self.name_wid1, state='hidden')
            self.canvas.itemconfig(self.name_wid2, state='hidden')
            self.entry_name.place_forget()
        else:
            email = self.entry_email.get()
            password = self.entry_password.get()
            if re.match(email_pattern, email):
                if App.USER == "USER":
                    try:
                        index = db.u_email.index(email)
                        if db.users[index][3] == password:
                            App.USER_ID = db.users[index][0]
                            self.destroy()
                            App()
                        else:
                            messagebox.showinfo("Wrong Password", "You password doesn't match.")
                    except ValueError:
                        messagebox.showinfo("Unregistered Email", "The email you used is not registered try signing up instead.")
                else:
                    if email == db.a_email and password == db.a_pass:
                        self.destroy()
                        App()
                    else:
                        messagebox.showinfo("Invalid Credentials", "The email or the password you entered is wrong.")
            else:
                messagebox.showinfo("Invalid Email", "Make sure the email you entered is correct.")

    def sign_up(self):
        if self.cur_page == "SIGNIN":
            self.cur_page = "SIGNUP"
            self.canvas.itemconfig(self.left_heading, text="New User?")
            self.canvas.coords(self.left_heading, 110, 190)

            self.canvas.itemconfig(self.left_msg1, text="Join us to explore any book you choose")
            self.canvas.coords(self.left_msg1, 70, 250)

            self.canvas.itemconfig(self.left_msg2, text="and dive into knowledge!")
            self.canvas.coords(self.left_msg2, 110, 270)

            self.canvas.itemconfig(self.right_heading, text="Create Account")

            self.canvas.itemconfig(self.right_msg, text="use your email for registration")
            self.canvas.coords(self.right_msg, 556, 231)

            self.signup_btn.config(image=self.button_signup_1, activebackground='#262626', background="#262626")
            self.signup_btn.place(x=552, y=470, width=200, height=52)

            self.signin_btn.config(image=self.button_signin_1, activebackground='#04A67F', background='#04A67F')
            self.signin_btn.place(x=100, y=317, width=145, height=50)

            self.canvas.itemconfig(self.name_wid1, state='normal')
            self.canvas.itemconfig(self.name_wid2, state='normal')
            self.entry_name.place(x=552, y=288, width=232, height=42)
        else:
            name = self.entry_name.get()
            email = self.entry_email.get()
            password = self.entry_password.get()
            if re.match(email_pattern, email):
                if is_strong_pass(password):
                    if len(name) >= 4:
                        # add user to database if not already in database else ask him to sign in
                        pass
                        if email not in db.u_email:
                            App.USER_ID = db.add_user([name, email, password])
                            self.destroy()
                            App()
                        else:
                            messagebox.showinfo("Login Instead", "The email you are using is already registered.")
                    else:
                        messagebox.showinfo("Invalid Name", "Name should at least be 3 characters long.")
                else:
                    messagebox.showinfo("Weak password", "Make sure your password has at least 12 characters.")
            else:
                messagebox.showinfo("Invalid Email", "Make sure the email you entered is correct.")

    def create_page(self):
        # Creating Canvas
        self.canvas = Canvas(self, bg="#262626", height=580, width=917, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.name_wid1 = self.canvas.create_image(528, 309, image=self.image_name)
        self.name_wid2 = self.canvas.create_image(677, 309, image=self.entry_image)

        self.entry_name = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_name.place(x=552, y=288, width=232, height=42)

        self.canvas.create_image(528, 366, image=self.image_email)
        self.canvas.create_image(678, 366, image=self.entry_image)

        self.entry_email = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_email.place(x=552, y=348, width=232, height=40)

        self.canvas.create_image(528, 422, image=self.image_password)
        self.canvas.create_image(676, 422, image=self.entry_image)

        self.entry_password = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_password.place(x=552, y=401, width=232, height=40)

        self.signup_btn = Button(image=self.button_signup_1, borderwidth=0, highlightthickness=0, command=self.sign_up, relief="flat", background="#262626", activebackground='#262626')
        self.signup_btn.place(x=552, y=470, width=200, height=52)

        self.canvas.create_image(191, 290, image=self.image_left_bg)
        self.canvas.create_image(299, 263, image=self.image_shapes)
        self.canvas.create_image(20, 590, image=self.image_circle)

        self.right_heading = self.canvas.create_text(519, 182, anchor="nw", text="Create Account", fill="#38B593",
                           font=("Montserrat Bold", 32 * -1))
        self.right_msg = self.canvas.create_text(556, 231, anchor="nw", text="use your email for registration", fill="#9A9A9A",
                           font=("Montserrat Regular", 12 * -1))

        self.left_heading = self.canvas.create_text(110, 190, anchor="nw", text="New User?", fill="#FFFFFF", tags='left',
                                                    font=("Montserrat Bold", 32 * -1))
        self.left_msg1 = self.canvas.create_text(70, 250, anchor="nw", text="Join us to explore any book you choose", fill="#FFFFFF", tags='left',
                           font=("Montserrat Regular", 14 * -1))
        self.left_msg2 = self.canvas.create_text(110, 270, anchor="nw", text="and dive into knowledge!", fill="#FFFFFF", tags='left',
                           font=("Montserrat Regular", 14 * -1))

        self.signin_btn = Button(image=self.button_signin_1, borderwidth=0, highlightthickness=0, command=self.sign_in, relief="flat", activebackground="#04A67F", background="#04A67F")
        self.signin_btn.place(x=100, y=317, width=145, height=50)

class Home:
    # User rel pos instead of static pos
    ASSETS_PATH = "assets\\home\\"
    TOP_GAP = 130
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")
        self.copies_var = []
        self.prv_search = None

        Label(master=self.frame, text="Library", font=("Roboto", 25, 'bold'), background="#262626", foreground='white').place(x=10, y=15)

        self.image_search = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.search_canvas = Canvas(master=self.frame, bg="#262626", bd=0, highlightthickness=0)
        self.search_canvas.create_image(150, 20, image=self.image_search)
        self.entry_search = Entry(bd=0, bg="#E7E7E7", fg="#000716", highlightthickness=0, font=font.Font(family="Roboto", size=11))
        self.search_canvas.create_window((52, 4), window=self.entry_search, anchor='nw', height=33,
                                  width=222)
        self.search_canvas.place(x=self.parent.winfo_width() - 350, y=10, height=41, width=300)
        self.entry_search.bind("<KeyRelease>", self.update_books)

        self.image_left = PhotoImage(file=self.relative_to_assets("left_edge.png"))
        self.image_right = PhotoImage(file=self.relative_to_assets("right_edge.png"))
        self.head_canvas = Canvas(master=self.frame, bg="#262626", bd=0, highlightthickness=0)
        self.head_canvas.create_image(12, 22, image=self.image_left)
        self.right_id = self.head_canvas.create_image(0, 0, image=self.image_right)
        self.head_rect = self.head_canvas.create_rectangle(10, 10, 50, 50, fill="#F37577", outline="")
        self.head_canvas.place(x=10, y=50, width=self.parent.winfo_width()-57, height=44)

        Label(master=self.frame, text="ID", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=19, y=75)
        Label(master=self.frame, text="Book", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=120, y=75)
        Label(master=self.frame, text="Author", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=550 if App.USER != "ADMIN" else 500, y=75)
        if App.USER == "ADMIN":
            Label(master=self.frame, text="Copies", font=("Roboto", 20, 'bold'), background="#F37577",
                  foreground='white').place(x=700, y=75)

        self.image_i_left = PhotoImage(file=self.relative_to_assets("item_left.png"))
        self.image_i_right = PhotoImage(file=self.relative_to_assets("item_right.png"))
        self.image_button = PhotoImage(file=self.relative_to_assets("button_.png"))
        self.image_maintenance = PhotoImage(file=self.relative_to_assets("maintenance.png"))
        self.image_remove = PhotoImage(file=self.relative_to_assets("remove.png"))


        self.scroll_frame = Frame(self.frame, height = self.parent.winfo_height() - self.TOP_GAP, width=self.parent.winfo_width()-50, bg="#262626")
        self.scroll_frame.pack(fill='both', expand=True, pady=(self.TOP_GAP,0))
        self.lib_books = db.lib_books()
        self.stripped_books = [[book[1].replace(" ", "").lower(), book[2].replace(" ", "").lower()] for book in self.lib_books]
        self.list_frame = ListFrame(self.scroll_frame, self.lib_books, 60, self.create_item)

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def add_frame(self):
        self.list_frame.clean_add()
        self.frame.pack(expand=True, fill='both')

    def update_frame(self):
        self.search_canvas.place(x=self.parent.winfo_width() - 350, y=10, height=41, width=300)
        self.head_canvas.coords(self.head_rect, 20, 0, self.parent.winfo_width() - 80, 44)
        self.head_canvas.coords(self.right_id,  self.parent.winfo_width() - 73, 22)
        self.head_canvas.place(x=5, y=70, width=self.parent.winfo_width() - 60, height=50)

    def remove_frame(self):
        self.list_frame.clean_close()
        self.frame.pack_forget()

    def remove_book(self, book_id):
        index = db.l_ids.index(book_id)
        copies = self.copies_var[index].get()
        if copies != 0:
            self.copies_var[index].set(copies-1)
            db.library[index][7] = int(db.library[index][7]) - 1
            db.update_library()

    def to_maintenance(self, book_id):
        index = db.l_ids.index(book_id)
        copies = self.copies_var[index].get()
        if copies != 0:
            self.copies_var[index].set(copies - 1)
            db.library[index][7] = int(db.library[index][7]) - 1
            db.library[index][9] = int(db.library[index][9]) + 1
            db.update_library()

    def create_item(self, data, parent):
        frame = Frame(parent, bg='#333333', width=self.parent.winfo_width() - 80, height=50)
        lf = Frame(frame, bg='#333333')
        lf.place(x=0, y=0, relheight=1, width=21)
        Label(lf, image=self.image_i_left, bg="#262626").pack()

        rf = Frame(frame, bg='#333333')
        rf.place(anchor="ne", relx=1, y=0, relheight=1, width=21)
        Label(rf, image=self.image_i_right, bg="#262626").pack(side='left')

        Label(frame, text=data[0], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=5, y=10)
        Label(frame, text=data[1], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=110, y=10)
        Label(frame, text=data[2], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=540 if App.USER != "ADMIN" else 490, y=10)
        if App.USER == "USER":
            Button(master= frame, image=self.image_button,background='#333333', activebackground='#333333', borderwidth=0, highlightthickness=0, command=lambda identity=data[0]: self.borrow_book(identity), relief="flat").place(anchor='ne', relx=0.98, y=10)
        elif App.USER == "ADMIN":
            temp = IntVar(value=data[3])
            self.copies_var.append(temp)
            Label(frame, textvariable=temp, font=font.Font(family="Roboto", size=13), background='#333333',
                  foreground='white', ).place(x=730, y=10)
            Button(master=frame, image=self.image_maintenance, background='#333333', activebackground='#333333',
                   borderwidth=0, highlightthickness=0, command=lambda s=data[0]: self.to_maintenance(s),
                   relief="flat").place(anchor='center', relx=0.92, y=27)
            Button(master=frame, image=self.image_remove, background='#333333', activebackground='#333333',
                   borderwidth=0, highlightthickness=0, command=lambda s=data[0]: self.remove_book(s),
                   relief="flat").place(anchor='center', relx=0.97, y=27)

        return frame

    def borrow_book(self, identity):
        if already_borrowed(App.USER_ID, identity, db.register):
            messagebox.showinfo("Already Borrowed", "You haven't returned the copy of this book that you borrowed,")
        elif int(db.lib_dict[identity]['Copies']) - int(db.lib_dict[identity]['Borrowed']) - int(db.lib_dict[identity]['Maintenance']) == 0:
            messagebox.showinfo("Not Available", "Currently the book is unavailable.")
        else:
            prev_bid = db.register[-1][0]
            bid = '#' + '0'*(5-len(str(int(prev_bid[1:]) + 1))) + str(int(prev_bid[1:]) + 1)
            i_date = datetime.date.today().strftime('%d-%m-%Y')
            db.register.append([bid, identity, App.USER_ID, i_date, '-'])
            db.update_register()

            index = db.l_ids.index(identity)
            db.library[index][8] = int(db.library[index][8]) + 1
            db.update_library()

            messagebox.showinfo("Successfully Borrowed", "You can have the book now.")

    def update_books(self, _):
        key = self.entry_search.get().replace(" ", "").lower()
        if key == "":
            self.list_frame.update_items(self.lib_books)
        else:
            self.prv_search = key
            books = sort_lib(key, self.lib_books, self.stripped_books)
            self.list_frame.update_items(books)

class AddBook:
    ASSETS_PATH = "assets\\add_book\\"
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=650, width=950, bg="#262626")

        self.image_bg = PhotoImage(file=self.relative_to_assets("frame_bg.png"))

        self.canvas = Canvas(self.frame, height=610, width=730, bg="#262626", borderwidth=0, bd=0, highlightthickness=0)
        self.canvas.create_image(2, 8, anchor='nw', image=self.image_bg)

        self.validate_isbn = self.frame.register(lambda c: c in '123456789-X')

        self.entry_title = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11))
        self.entry_author = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11))
        self.entry_isbn = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11), validate='key', validatecommand=(self.validate_isbn, "%S"))
        self.entry_publisher = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11))
        self.entry_genre = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11))
        self.entry_lang = Entry(master=self.frame, background="white", borderwidth=0, font=font.Font(family="Roboto", size=11))

        self.canvas.create_window((172, 141), window=self.entry_title, anchor='center', height=37, width=230)
        self.canvas.create_window((172, 251), window=self.entry_isbn, anchor='center', height=37, width=230)
        self.canvas.create_window((172, 356), window=self.entry_genre, anchor='center', height=37, width=230)
        self.canvas.create_window((538, 141), window=self.entry_author, anchor='center', height=37, width=230)
        self.canvas.create_window((538, 251), window=self.entry_publisher, anchor='center', height=37, width=230)
        self.canvas.create_window((538, 356), window=self.entry_lang, anchor='center', height=37, width=230)

        self.image_button = PhotoImage(file=self.relative_to_assets("button.png"))
        self.button_add = Button(image=self.image_button, background="#333333", activebackground="#333333", borderwidth=0, command=self.add_book)
        self.canvas.create_window((340, 520), window=self.button_add, anchor='center', height=60, width=230)

        self.canvas.create_text((310, 470), text="Copies", font=('Roboto', 12), fill="#FFFFFF")

        self.copies = IntVar(value=1)
        self.comb_box = ttk.Combobox(self.frame, textvariable=self.copies, values=[str(i) for i in range(1, 101)], background="#333333", state='readonly', exportselection=False)
        self.canvas.create_window((360, 470), window=self.comb_box, anchor='center', width=35)

        self.canvas.place(relx=0.5, rely=0.5, anchor='center')

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def add_frame(self):
        self.frame.place(x=50, y=0)

    def remove_frame(self):
        self.frame.place_forget()

    def update_frame(self):
        self.frame.config(width=self.parent.winfo_width() - 50, height=self.parent.winfo_height())

    def add_book(self):
        isbn = self.entry_isbn.get()
        title = self.entry_title.get()
        author = self.entry_author.get()
        publisher = self.entry_publisher.get()
        genre = self.entry_genre.get()
        language = self.entry_lang.get()
        l_id = db.library[-1][1]
        b_id = '#' + str(int(l_id[1:]) + 1)
        copies = self.comb_box.get()
        if all([len(title), len(author), len(genre), len(language)]):
            db.library.append([isbn, b_id, title, author, publisher, genre, language, copies, 0, 0])
            db.update_library()
        else:
            messagebox.showinfo("Incomplete Values", "Make sure you entered all the values.")

class Statistics:
    ASSETS_PATH = "assets\\stat\\"
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=650, width=950, bg="#262626")
        self.frame.rowconfigure((0, 1), weight=1, uniform='b')
        self.frame.columnconfigure((0, 1), weight=1, uniform='a')

        self.image_lt = PhotoImage(file=self.relative_to_assets('lt.png'))
        self.image_lb = PhotoImage(file=self.relative_to_assets('lb.png'))
        self.image_rt = PhotoImage(file=self.relative_to_assets('rt.png'))
        self.image_rb = PhotoImage(file=self.relative_to_assets('rb.png'))

        self.top_frame = Frame(self.frame, bg='#333333')
        self.bottom_left_frame = Frame(self.frame, bg="#333333")
        self.bottom_right_frame = Frame(self.frame, bg="#333333")

        for parent_frame in (self.top_frame, self.bottom_right_frame, self.bottom_left_frame):
            lt = Frame(parent_frame, bg='#262626')
            lt.place(x=0, y=0, height=25, width=25)
            Label(lt, image=self.image_lt, bg="#262626").pack()

            rt = Frame(parent_frame, bg='#262626')
            rt.place(anchor="ne", relx=1, y=0, height=25, width=25)
            Label(rt, image=self.image_rt, bg="#262626").pack(side='left')

            lb = Frame(parent_frame, bg='#262626')
            lb.place(anchor="sw", relx=0, rely=1, height=25, width=25)
            Label(lb, image=self.image_lb, bg="#262626").pack()

            rb = Frame(parent_frame, bg='#262626')
            rb.place(anchor="se", relx=1, rely=1, height=25, width=25)
            Label(rb, image=self.image_rb, bg="#262626").pack(side='left')

        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=12, pady=(12, 0))
        self.bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=12)
        self.bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=12, pady=12)

        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=x)) for x in range(10)]
        books_borrowed = line_chart_values(db.register, dates)

        categories = ['Fiction', 'NonFiction', 'Mystery', 'Education', 'Fantasy']
        values = bar_values(db.library, categories)

        self.add_line_chart(books_borrowed, dates)
        self.add_bar_graph(categories, values)
        self.add_pie_chart(["Available", "Borrowed", "Maintenance"], pie_values(db.library))

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def add_line_chart(self, books_borrowed, dates):
        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(dates, books_borrowed, marker='o', color='cyan', linewidth=2, markersize=5, alpha=0.8)

        ax.set_title("Books Borrowed Over Time", fontsize=16, color='white', fontweight='bold')
        ax.set_ylabel("Number of Books Borrowed", fontsize=12, color='white')
        ax.set_facecolor('#333333')
        fig.patch.set_facecolor('#333333')
        y_min = min(books_borrowed) - 2 if min(books_borrowed) > 1 else 0  # Slightly lower than the min value
        y_max = max(books_borrowed) + 3  # Slightly higher than the max value
        ax.set_ylim(y_min, y_max)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xticks(dates)
        ax.tick_params(axis='both', which='major', labelsize=10, colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')


        y_ticks = ax.get_yticks()
        for y in y_ticks:
            ax.axhline(y=y, color='white', linestyle='--', linewidth=0.5, alpha=0.3)

        for spine in ax.spines.values():
            spine.set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=self.top_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=25)

    def add_pie_chart(self, labels, values):
        colors = ['cyan', '#FF6F61', '#06A67E']

        fig, ax = plt.subplots(figsize=(5, 5))

        wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, autopct='%1.0f%%',
                                          startangle=90, pctdistance=0.85, shadow=True)

        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')

        centre_circle = plt.Circle((0, 0), 0.70, fc='#333333')
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')

        plt.title("Inventory Status", fontsize=16, fontweight='bold', color='white')

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')

        canvas = FigureCanvasTkAgg(fig, master=self.bottom_right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=25)

    def add_bar_graph(self, genres, values):
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')

        bars = ax.barh(genres, values, color='cyan', alpha=0.7)

        ax.tick_params(axis='both', which='major', labelsize=10, colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f'{width}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(3, 0),
                        textcoords="offset points",
                        ha='left', va='center', color='white')

        ax.set_title('Books in each Genre', fontsize=16, color='white', fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        plt.subplots_adjust(left=0.2)

        canvas = FigureCanvasTkAgg(fig, master=self.bottom_left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=25)

    def add_frame(self):
        self.frame.pack(fill='both', expand=True, padx=(0, 0))

    def remove_frame(self):
        self.frame.pack_forget()

    def update_frame(self):
        pass

class Register:
    ASSETS_PATH = "assets\\register\\"
    TOP_GAP = 100
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")

        self.image_notify = PhotoImage(file=self.relative_to_assets("notify_btn.png"))

        Label(self.frame, text="Borrowing History", font=("Roboto", 20, 'bold'), background='#262626', fg='white').place( x=10, y=8)
        Button(self.frame, image=self.image_notify, background='#262626', activebackground="#262626", borderwidth=0, command=self.send_notifications).place(anchor='ne', y=4, relx=1)


        self.image_left = PhotoImage(file=self.relative_to_assets("left_edge.png"))
        self.image_right = PhotoImage(file=self.relative_to_assets("right_edge.png"))

        self.head_canvas = Canvas(master=self.frame, bg="#262626", bd=0, highlightthickness=0)
        self.head_canvas.create_image(12, 22, image=self.image_left)
        self.right_id = self.head_canvas.create_image(0, 0, image=self.image_right)
        self.head_rect = self.head_canvas.create_rectangle(10, 10, 50, 50, fill="#F37577", outline="")
        self.head_canvas.place(x=5, y=50, width=self.parent.winfo_width() - 57, height=44)

        Label(master=self.frame, text="ID", font=("Roboto", 20, 'bold'), background="#F37577", foreground='white').place(x=19, y=55)
        Label(master=self.frame, text="Book", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=100, y=55)
        Label(master=self.frame, text="Borrower", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(relx=0.5, y=55)
        Label(master=self.frame, text="Issued", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(relx=0.68, y=55)
        Label(master=self.frame, text="Returned", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(anchor='ne', relx=0.98, y=55)


        self.image_i_left = PhotoImage(file=self.relative_to_assets("item_left.png"))
        self.image_i_right = PhotoImage(file=self.relative_to_assets("item_right.png"))
        self.image_done = PhotoImage(file=self.relative_to_assets("done.png"))
        self.image_undone = PhotoImage(file=self.relative_to_assets("undone.png"))

        self.scroll_frame = Frame(self.frame, height=self.parent.winfo_height() - self.TOP_GAP,
                                  width=self.parent.winfo_width() - 50, bg="#262626")
        self.scroll_frame.pack(expand=True, fill="both", pady=(self.TOP_GAP, 0))
        self.list_frame = ListFrame(self.scroll_frame, db.reg_info(), 60, self.create_item)

    def add_frame(self):
        self.frame.pack(expand=True, fill="both")
        self.list_frame.clean_add()

    def remove_frame(self):
        self.list_frame.clean_close()
        self.frame.pack_forget()

    def update_frame(self):
        self.head_canvas.coords(self.head_rect, 20, 0, self.parent.winfo_width() - 80, 44)
        self.head_canvas.coords(self.right_id, self.parent.winfo_width() - 73, 22)
        self.head_canvas.place(x=5, y=50, width=self.parent.winfo_width() - 60, height=50)

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def create_item(self, data, parent):
        frame = Frame(parent, bg='#333333', width=920, height=50)
        lf = Frame(frame, bg='#333333')
        lf.place(x=0, y=0, relheight=1, width=21)
        Label(lf, image=self.image_i_left, bg="#262626").pack()

        rf = Frame(frame, bg='#333333')
        rf.place(anchor="ne", relx=1, y=0, relheight=1, width=21)
        Label(rf, image=self.image_i_right, bg="#262626").pack(side='left')

        Label(frame, text=data[0], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=5, y=10)
        Label(frame, text=data[1], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=93, y=10)
        Label(frame, text=data[2], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(relx=0.5, y=10)
        Label(frame, text=data[3], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(relx=0.68, y=10)
        Label(frame, image=self.image_done if data[4] != '-' else self.image_undone, background='#333333').place(anchor='ne', relx=0.97, y=14)

        return frame

    def send_notifications(self):
        subject = "Friendly Reminder to Return Borrowed Books"
        unreturned_users = {}
        for row in db.register:
            if row[4] == '-':
                email = db.users_dict[row[2]]['Email']
                name = db.users_dict[row[2]]['Name']
                books = [db.lib_dict[row[1]]['Title']]
                try:
                    unreturned_users[email]['books']  += books
                except KeyError:
                    unreturned_users[email] = {'name': name, 'books': books}
        for key, value in unreturned_users.items():
            body = f"""Dear {value['name']},

\tI hope this message finds you well. I wanted to kindly remind you about the book(s) you borrowed from us. 
\tIf you have finished reading them, we would appreciate it if you could return them at your earliest convenience.

\tPlease check the list of books you currently have:
\t\t{"".join([f"{index+1}) {book}\n\t\t" for index, book in enumerate(value['books'])])}
\tIf you need more time with the book(s), feel free to let us know, and we can discuss an extension.

\tThank you for your attention to this matter. We look forward to receiving the books back soon!

\tBest regards,
\tBook Nest
"""
            send_email_thread(subject, body, key)

class History:
    ASSETS_PATH = "assets\\history\\"
    TOP_GAP = 100

    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")
        Label(self.frame, text="Borrowing History", font=("Roboto", 20, 'bold'), background='#262626',
              fg='white').place(anchor='center', relx=0.5, y=25)
        self.borrow_history = db.borrow_hist(App.USER_ID)

        self.image_left = PhotoImage(file=self.relative_to_assets("left_edge.png"))
        self.image_right = PhotoImage(file=self.relative_to_assets("right_edge.png"))

        self.head_canvas = Canvas(master=self.frame, bg="#262626", bd=0, highlightthickness=0)
        self.head_canvas.create_image(12, 22, image=self.image_left)
        self.right_id = self.head_canvas.create_image(0, 0, image=self.image_right)
        self.head_rect = self.head_canvas.create_rectangle(10, 10, 50, 50, fill="#F37577", outline="")
        self.head_canvas.place(x=5, y=50, width=self.parent.winfo_width() - 57, height=44)

        Label(master=self.frame, text="ID", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=19, y=55)
        Label(master=self.frame, text="Book", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(x=100, y=55)
        Label(master=self.frame, text="Issued", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(relx=0.68, y=55)
        Label(master=self.frame, text="Status", font=("Roboto", 20, 'bold'), background="#F37577",
              foreground='white').place(anchor='ne', relx=0.96, y=55)

        self.image_i_left = PhotoImage(file=self.relative_to_assets("item_left.png"))
        self.image_i_right = PhotoImage(file=self.relative_to_assets("item_right.png"))
        self.image_borrow = PhotoImage(file=self.relative_to_assets("borrow.png"))
        self.image_return = PhotoImage(file=self.relative_to_assets("return.png"))

        self.scroll_frame = Frame(self.frame, height=self.parent.winfo_height() - self.TOP_GAP,
                                  width=self.parent.winfo_width() - 50, bg="#262626")
        self.scroll_frame.pack(expand=True, fill="both", pady=(self.TOP_GAP, 0))
        self.list_frame = ListFrame(self.scroll_frame, self.borrow_history, 60, self.create_item)

    def add_frame(self):
        self.list_frame.update_items(db.borrow_hist(App.USER_ID))
        self.list_frame.clean_add()
        self.frame.pack(expand=True, fill="both")

    def remove_frame(self):
        self.list_frame.clean_close()
        self.frame.pack_forget()

    def update_frame(self):
        self.head_canvas.coords(self.head_rect, 20, 0, self.parent.winfo_width() - 80, 44)
        self.head_canvas.coords(self.right_id, self.parent.winfo_width() - 73, 22)
        self.head_canvas.place(x=5, y=50, width=self.parent.winfo_width() - 60, height=50)

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    def create_item(self, data, parent):
        frame = Frame(parent, bg='#333333', width=self.parent.winfo_width() - 80, height=50)
        lf = Frame(frame, bg='#333333')
        lf.place(x=0, y=0, relheight=1, width=21)
        Label(lf, image=self.image_i_left, bg="#262626").pack()

        rf = Frame(frame, bg='#333333')
        rf.place(anchor="ne", relx=1, y=0, relheight=1, width=21)
        Label(rf, image=self.image_i_right, bg="#262626").pack(side='left')

        Label(frame, text=data[0], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=5, y=10)
        Label(frame, text=data[1], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(x=93, y=10)
        Label(frame, text=data[2], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(relx=0.68, y=10)

        Button(frame, image=self.image_borrow if data[3] != '-' else self.image_return, background='#333333',activebackground='#333333', borderwidth=0,
               command=lambda : self.borrow_again(data[0]) if data[3] != '-' else self.return_book(data[4])).place(anchor='ne', relx=0.99, y=6)

        return frame

    def return_book(self, borrow_id):
        bor_index = [row[0] for row in db.register].index(borrow_id)
        db.register[bor_index][4] = datetime.date.today().strftime('%d-%m-%Y')
        db.update_register()

        book_index = db.l_ids.index(db.register[bor_index][1])
        db.library[book_index][8] = int(db.library[book_index][8]) - 1
        db.update_library()
        self.list_frame.update_items(db.borrow_hist(App.USER_ID))

    def borrow_again(self, b_id):
        if already_borrowed(App.USER_ID, b_id, db.register):
            messagebox.showinfo("Already Borrowed", "You haven't returned the copy of this book that you borrowed,")
        elif int(db.lib_dict[b_id]['Copies']) - int(db.lib_dict[b_id]['Borrowed']) - int(
                db.lib_dict[b_id]['Maintenance']) == 0:
            messagebox.showinfo("Not Available", "Currently the book is unavailable.")
        else:
            prev_bid = db.register[-1][0]
            bid = '#' + '0' * (5 - len(str(int(prev_bid[1:]) + 1))) + str(int(prev_bid[1:]) + 1)
            i_date = datetime.date.today().strftime('%d-%m-%Y')
            db.register.append([bid, b_id, App.USER_ID, i_date, '-'])
            db.update_register()

            index = db.l_ids.index(b_id)
            db.library[index][8] = int(db.library[index][8]) + 1
            db.update_library()
            self.list_frame.update_items(db.borrow_hist(App.USER_ID))
            messagebox.showinfo("Successfully Borrowed", "You can have the book now.")

class Love:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")

    def add_frame(self):
        self.frame.pack(expand=True, fill='both')

    def remove_frame(self):
        self.frame.pack_forget()

    def update_frame(self):
        pass

class ListFrame:
    def __init__(self, parent, text_data, item_height, create_item):
        self.master_frame = Frame(master=parent, bg="#262626")
        self.master_frame.place(x=0, y=0, width=950, height=600)
        self.create_item = create_item

        self.parent = parent
        self.text_data = text_data
        self.item_number = len(text_data)
        self.item_height = item_height
        self.list_height = self.item_height * self.item_number
        self.config_id = None

        self.canvas = Canvas(self.master_frame, bg="#262626", bd=0, highlightthickness=0, scrollregion=(0, 0, self.parent.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill="both")

        self.frame = Frame(self.master_frame, bg="#262626")
        for item in text_data:
            item = create_item(item, self.frame)
            item.pack(pady=4, padx=10)

        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', height=self.list_height, width=self.parent.winfo_width())

    def clean_add(self):
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.config_id = self.parent.bind('<Configure>', self.update_size, add='+')
        self.update_size('')

    def clean_close(self):
        self.canvas.unbind_all('<MouseWheel>')
        self.parent.unbind('<Configure>', self.config_id)

    def update_items(self, items):
        self.frame.destroy()
        self.frame = Frame(self.master_frame, bg="#262626")
        for item in items:
            item = self.create_item(item, self.frame)
            item.pack(pady=4, padx=10)
        self.list_height = len(items) * self.item_height
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', height=self.list_height,
                                  width=self.parent.winfo_width())
        self.canvas.config(scrollregion=(0, 0, self.parent.winfo_width(), self.list_height))

    def update_size(self, _):
        if self.list_height >= self.parent.winfo_height():
            height = self.list_height
            self.canvas.bind_all('<MouseWheel>',
                                 lambda event: self.canvas.yview_scroll(-int(event.delta / 120), "units"))
        else:
            # height = self.master_frame.winfo_height()
            height = self.list_height
            self.canvas.unbind_all("<MouseWheel>")

        for frame in self.frame.winfo_children():
            frame.config(width=self.parent.winfo_width())
        self.master_frame.place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', height=height, width=self.parent.winfo_width())

class App(Tk):
    ASSETS_PATH = "assets\\frame3\\"
    WIDTH = 1000
    HEIGHT = 650
    USER = None
    USER_ID = None
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.rect = None
        self.btn_books = None
        self.btn_stat = None
        self.btn_plus = None
        self.btn_love = None
        self.btn_hist = None
        self.btn_home = None

        self.cur_page = "HOME"
        self.home_frame = Home(self)
        self.add_book_frame = AddBook(self)
        self.stat_frame = Statistics(self)
        self.register_frame = Register(self)
        self.history_frame = History(self)
        self.love_frame = Love(self)

        self.add_frames    = {"HOME": self.home_frame.add_frame, "ADD": self.add_book_frame.add_frame, "STATISTICS": self.stat_frame.add_frame,
                              "REGISTER": self.register_frame.add_frame, "HISTORY": self.history_frame.add_frame, "LOVE": self.love_frame.add_frame}
        self.remove_frames = {"HOME": self.home_frame.remove_frame, "ADD": self.add_book_frame.remove_frame, "STATISTICS": self.stat_frame.remove_frame,
                              "REGISTER": self.register_frame.remove_frame, "HISTORY": self.history_frame.remove_frame, "LOVE": self.love_frame.remove_frame}
        self.update_frames = {"HOME": self.home_frame.update_frame, "ADD": self.add_book_frame.update_frame, "STATISTICS": self.stat_frame.update_frame,
                              "REGISTER": self.register_frame.update_frame, "HISTORY": self.history_frame.update_frame, "LOVE": self.love_frame.update_frame}

        # Configuring Window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{int(self.winfo_screenwidth() / 2 - self.WIDTH / 2)}+{int(self.winfo_screenheight() / 2 - self.HEIGHT / 2)}")
        self.configure(bg="#FFFFFF")
        self.title("BookNest")
        self.iconbitmap('assets\\icon.ico')
        self.minsize(self.WIDTH, self.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)


        # Loading Assets
        self.image_books = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.image_stat = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.image_plus = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.image_love = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.image_hist = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.image_home = PhotoImage(file=self.relative_to_assets("button_6.png"))

        self.image_books_hover = PhotoImage(file=self.relative_to_assets("button_hover_1.png"))
        self.image_stat_hover = PhotoImage(file=self.relative_to_assets("button_hover_2.png"))
        self.image_plus_hover = PhotoImage(file=self.relative_to_assets("button_hover_3.png"))
        self.image_love_hover = PhotoImage(file=self.relative_to_assets("button_hover_4.png"))
        self.image_hist_hover = PhotoImage(file=self.relative_to_assets("button_hover_5.png"))
        self.image_home_hover = PhotoImage(file=self.relative_to_assets("button_hover_6.png"))

        self.create_page()
        self.mainloop()

    def on_exit(self):
        self.quit()
        exit()

    def on_resize(self, _):
        self.canvas.coords(self.rect, 0, 0, 50, self.winfo_height())
        self.update_frames[self.cur_page]()

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH + path

    @staticmethod
    def hover_effect(btn, img_n, img_h):
        btn.bind('<Enter>', lambda e: btn.config(image=img_h))
        btn.bind('<Leave>', lambda e: btn.config(image=img_n))

    def change_frame(self, name):
        if self.cur_page != name:
            self.remove_frames[self.cur_page]()
            self.add_frames[name]()
            self.cur_page = name

    def create_page(self):
        self.canvas = Canvas(self, width=50, height=self.HEIGHT, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0, relheight=1)
        self.rect = self.canvas.create_rectangle(0, 0, 50, self.HEIGHT, fill="#06A67E", outline="")
        center_frame = Frame(self, bg="#06A67E")

        if self.USER == "USER":
            self.btn_home = Button(center_frame, image=self.image_home, borderwidth=0, highlightthickness=0, activebackground='#06A67E',
                                   command=lambda: self.change_frame("HOME"), relief="flat")
            self.btn_love = Button(center_frame, image=self.image_love, borderwidth=0, highlightthickness=0, activebackground='#06A67E',
                                   command=lambda: self.change_frame("LOVE"), relief="flat")
            self.btn_hist = Button(center_frame, image=self.image_hist, borderwidth=0, highlightthickness=0, activebackground='#06A67E',
                                   command=lambda: self.change_frame("HISTORY"), relief="flat")

            self.btn_home.pack(side='top', pady=10)
            self.btn_love.pack(side='top', pady=10)
            self.btn_hist.pack(side='top', pady=10)

            center_frame.pack(side="left", anchor="center")

            self.hover_effect(self.btn_home, self.image_home, self.image_home_hover)
            self.hover_effect(self.btn_love, self.image_love, self.image_love_hover)
            self.hover_effect(self.btn_hist, self.image_hist, self.image_hist_hover)

        elif self.USER == "ADMIN":
            self.btn_home = Button(center_frame, activebackground='#06A67E', image=self.image_home, borderwidth=0, highlightthickness=0,
                                   command=lambda: self.change_frame("HOME"), relief="flat")
            self.btn_books = Button(center_frame,activebackground='#06A67E', image=self.image_books, borderwidth=0, highlightthickness=0,
                                   command=lambda: self.change_frame("REGISTER"), relief="flat")
            self.btn_stat = Button(center_frame,activebackground='#06A67E', image=self.image_stat, borderwidth=0, highlightthickness=0,
                                   command=lambda: self.change_frame("STATISTICS"), relief="flat")
            self.btn_plus = Button(self, activebackground='#06A67E',image=self.image_plus, borderwidth=0, highlightthickness=0,
                                   command=lambda: self.change_frame("ADD"), relief="flat")

            self.btn_home.pack(side='top', pady = 10)
            self.btn_books.pack(side='top', pady=10)
            self.btn_stat.pack(side='top', pady=10)

            center_frame.pack(side="left", anchor="center")
            self.btn_plus.place(anchor='sw', x=0, rely=1)

            self.hover_effect(self.btn_home, self.image_home, self.image_home_hover)
            self.hover_effect(self.btn_books, self.image_books, self.image_books_hover)
            self.hover_effect(self.btn_stat, self.image_stat, self.image_stat_hover)
            self.hover_effect(self.btn_plus, self.image_plus, self.image_plus_hover)

        self.add_frames[self.cur_page]()
        self.bind("<Configure>", self.on_resize, add='+')

if __name__ == "__main__":
    db = DataBase()
    # App.USER = "USER"
    # # App.USER_ID = "#00002"
    # app = App()
    try:
        UserAdmin()
    except Exception:
        pass