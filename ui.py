from tkinter import font, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from database import Library, UserAdminManager
from utils import *
from ui_utils import *
import threading
import datetime


class UserAdmin(Tk):
    """
    The Initial Login page which ask you to choose your role.
    Choices:
        1)USER  - Borrow Books
        2)ADMIN - Manage Library and view Records.
    """
    ASSETS_PATH = "assets/frame1/"
    def __init__(self):
        super().__init__()
        # Requirements
        self.image_1 = PhotoImage(file=self.get_path("image_1.png"))
        self.image_2 = PhotoImage(file=self.get_path("image_2.png"))
        self.button_image_1 = PhotoImage(file=self.get_path("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.get_path("button_2.png"))


        # Configuring Window
        self.geometry(f"700x550+{int(self.winfo_screenwidth()/2  - 700/2)}+{int(self.winfo_screenheight()/2  - 550/2)}")
        self.configure(bg="#262626")
        self.title("BookNest")
        self.iconbitmap('assets/icon.ico')
        self.resizable(False, False)


        self.create_page()
        self.mainloop()

    def get_path(self, path: str):
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
    """

    """
    ASSETS_PATH = "assets/frame2/"

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
        self.image_email = PhotoImage(file=self.get_path("image_1.png"))
        self.image_name = PhotoImage(file=self.get_path("image_2.png"))
        self.image_password = PhotoImage(file=self.get_path("image_3.png"))
        self.image_left_bg = PhotoImage(file=self.get_path("image_4.png"))
        self.image_shapes = PhotoImage(file=self.get_path("image_5.png"))
        self.image_circle = PhotoImage(file=self.get_path("image_6.png"))

        self.entry_image = PhotoImage(file=self.get_path("entry.png"))

        self.button_signup_1 = PhotoImage(file=self.get_path("button_1.png"))
        self.button_signin_1 = PhotoImage(file=self.get_path("button_2.png"))
        self.button_signin_2 = PhotoImage(file=self.get_path("button_3.png"))
        self.button_signup_2 = PhotoImage(file=self.get_path("button_4.png"))


        # Configuring Window
        self.geometry(f"917x580+{int(self.winfo_screenwidth()/2  - 917/2)}+{int(self.winfo_screenheight()/2  - 580/2)}")
        self.configure(bg="#262626")
        self.title("BookNest")
        self.iconbitmap('assets/icon.ico')
        self.resizable(False, False)
        self.focus_force()

        self.create_page()
        if App.USER == "ADMIN":
            self.sign_in(rm_left=True)
        self.mainloop()

    def get_path(self, path: str):
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
            self.entry_email.focus_set()
        else:
            email = self.entry_email.get()
            password = self.entry_password.get()
            if re.match(email_pattern, email):
                if App.USER == "USER":
                    try:
                        u_id = ua_data.is_user(email, password)
                        if u_id:
                            App.USER_ID = u_id
                            self.destroy()
                            App()
                        else:
                            show_notification(self, "Make sure your password is correct.",fg='red', x_pos=681)
                    except ValueError:
                        show_notification(self, "Unregistered email. Try to SignUp instead.", fg='red', x_pos=681)
                else:
                    if ua_data.is_admin(email, password):
                        self.destroy()
                        App()
                    else:
                        show_notification(self, "The email or the password you entered is wrong.", fg='red', x_pos=681)
            else:
                show_notification(self, "Make sure the email you entered is correct.", fg='red', x_pos=681)

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
            self.entry_name.focus_set()
        else:
            name = self.entry_name.get()
            email = self.entry_email.get()
            password = self.entry_password.get()
            if re.match(email_pattern, email):
                if is_strong_pass(password):
                    if len(name) >= 4:
                        if email not in ua_data.u_email:
                            App.USER_ID = ua_data.add_user([name, email, password])
                            self.destroy()
                            App()
                        else:
                            show_notification(self, "The email you are using is already registered.", fg='red', x_pos=681)
                    else:
                        show_notification(self, "Name should at least be 3 characters long.", fg='red', x_pos=681)
                else:
                    show_notification(self, "Password must be 8+ chars with upper, lower, digit, and special-char", fg='red', x_pos=699)
            else:
                show_notification(self, "Make sure the email you entered is correct.", fg='red', x_pos=681)

    def create_page(self):
        # Creating Canvas
        self.canvas = Canvas(self, bg="#262626", height=580, width=917, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.name_wid1 = self.canvas.create_image(528, 309, image=self.image_name)
        self.name_wid2 = self.canvas.create_image(677, 309, image=self.entry_image)

        self.entry_name = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_name.place(x=552, y=288, width=232, height=42)
        self.entry_name.focus_set()

        self.canvas.create_image(528, 366, image=self.image_email)
        self.canvas.create_image(678, 366, image=self.entry_image)

        self.entry_email = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_email.place(x=552, y=348, width=232, height=40)

        self.canvas.create_image(528, 422, image=self.image_password)
        self.canvas.create_image(676, 422, image=self.entry_image)

        self.entry_password = Entry(bd=0, bg="#E7E7E7", font=("Roboto", 11), highlightthickness=0)
        self.entry_password.place(x=552, y=401, width=232, height=40)

        self.signup_btn = Button(image=self.button_signup_1, borderwidth=0, highlightthickness=0, command=self.sign_up,
                                 relief="flat", background="#262626", activebackground='#262626')
        self.signup_btn.place(x=552, y=470, width=200, height=52)

        self.canvas.create_image(191, 290, image=self.image_left_bg)
        self.canvas.create_image(299, 263, image=self.image_shapes)
        self.canvas.create_image(20, 590, image=self.image_circle)

        self.right_heading = self.canvas.create_text(519, 182, anchor="nw", text="Create Account", fill="#38B593",
                                                     font=("Montserrat Bold", 32 * -1))
        self.right_msg = self.canvas.create_text(556, 231, anchor="nw", text="use your email for registration",
                                                 fill="#9A9A9A",
                                                 font=("Montserrat Regular", 12 * -1))

        self.left_heading = self.canvas.create_text(110, 190, anchor="nw", text="New User?", fill="#FFFFFF",
                                                    tags='left',
                                                    font=("Montserrat Bold", 32 * -1))
        self.left_msg1 = self.canvas.create_text(70, 250, anchor="nw", text="Join us to explore any book you choose",
                                                 fill="#FFFFFF", tags='left',
                                                 font=("Montserrat Regular", 14 * -1))
        self.left_msg2 = self.canvas.create_text(110, 270, anchor="nw", text="and dive into knowledge!", fill="#FFFFFF",
                                                 tags='left',
                                                 font=("Montserrat Regular", 14 * -1))

        self.signin_btn = Button(image=self.button_signin_1, borderwidth=0, highlightthickness=0, command=self.sign_in,
                                 relief="flat", activebackground="#04A67F", background="#04A67F")
        self.signin_btn.place(x=100, y=317, width=145, height=50)

class Home:
    ASSETS_PATH = "assets/home/"
    TOP_GAP = 130
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")
        self.copies_var = []
        self.prv_search = None

        Label(master=self.frame, text="Library", font=("Roboto", 25, 'bold'), background="#262626", foreground='white').place(x=10, y=15)

        self.image_search = PhotoImage(file=self.get_path("image_1.png"))
        self.search_canvas = Canvas(master=self.frame, bg="#262626", bd=0, highlightthickness=0)
        self.search_canvas.create_image(150, 20, image=self.image_search)
        self.entry_search = Entry(bd=0, bg="#E7E7E7", fg="#000716", highlightthickness=0, font=font.Font(family="Roboto", size=11))
        self.search_canvas.create_window((52, 4), window=self.entry_search, anchor='nw', height=33,
                                  width=222)
        self.search_canvas.place(x=self.parent.winfo_width() - 350, y=10, height=41, width=300)
        self.entry_search.bind("<KeyRelease>", self.update_books)

        self.image_left = PhotoImage(file=self.get_path("left_edge.png"))
        self.image_right = PhotoImage(file=self.get_path("right_edge.png"))
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
              foreground='white').place(relx=0.6 if App.USER != "ADMIN" else 0.5, y=75)
        if App.USER == "ADMIN":
            Label(master=self.frame, text="Copies", font=("Roboto", 20, 'bold'), background="#F37577",
                  foreground='white').place(relx=0.74, y=75)

        self.image_i_left = PhotoImage(file=self.get_path("item_left.png"))
        self.image_i_right = PhotoImage(file=self.get_path("item_right.png"))
        self.image_button = PhotoImage(file=self.get_path("button_.png"))
        self.image_maintenance = PhotoImage(file=self.get_path("maintenance.png"))
        self.image_remove = PhotoImage(file=self.get_path("remove.png"))


        self.scroll_frame = Frame(self.frame, height = self.parent.winfo_height() - self.TOP_GAP, width=self.parent.winfo_width()-50, bg="#262626")
        self.scroll_frame.pack(fill='both', expand=True, pady=(self.TOP_GAP,0))
        self.lib_books = library.lib_books()
        self.stripped_books = [[book[1].replace(" ", "").lower(), book[2].replace(" ", "").lower()] for book in self.lib_books]
        self.list_frame = ListFrame(self.scroll_frame, self.lib_books, 60, self.create_item)

    def get_path(self, path: str):
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
        index = library.l_ids.index(book_id)
        copies = self.copies_var[index].get()
        if copies != 0:
            self.copies_var[index].set(copies-1)
            library.books[index][7] = int(library.books[index][7]) - 1
            library.lib_dict[book_id]['Copies'] = library.books[index][7]
            library.update_library()
            show_notification(self.frame, "Removing the book.", fg='white')
        else:
            show_notification(self.frame, "No copies of the book available.", fg='red')

    def to_maintenance(self, book_id):
        index = library.l_ids.index(book_id)
        copies = self.copies_var[index].get()
        if copies != 0:
            self.copies_var[index].set(copies - 1)
            library.books[index][7] = int(library.books[index][7]) - 1
            library.books[index][9] = int(library.books[index][9]) + 1
            library.lib_dict[book_id]['Copies'] = library.books[index][7]
            library.lib_dict[book_id]['Maintenance'] = library.books[index][9]
            library.update_library()
            show_notification(self.frame, "Added the book to maintenance.", fg='white')
        else:
            show_notification(self.frame, "No copies of the book available.", fg='red')

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
        Label(frame, text=data[2], font=font.Font(family="Roboto", size=13), background='#333333', foreground='white').place(relx=0.6 if App.USER != "ADMIN" else 0.5, y=10)
        if App.USER == "USER":
            Button(master= frame, image=self.image_button,background='#333333', activebackground='#333333', borderwidth=0, highlightthickness=0, command=lambda identity=data[0]: self.borrow_book(identity), relief="flat").place(anchor='ne', relx=0.98, y=10)
        elif App.USER == "ADMIN":
            temp = IntVar(value=data[3])
            self.copies_var.append(temp)
            Label(frame, textvariable=temp, font=font.Font(family="Roboto", size=13), background='#333333',
                  foreground='white', ).place(relx=0.75, y=10)
            Button(master=frame, image=self.image_maintenance, background='#333333', activebackground='#333333',
                   borderwidth=0, highlightthickness=0, command=lambda s=data[0]: self.to_maintenance(s),
                   relief="flat").place(anchor='center', relx=0.92, y=27)
            Button(master=frame, image=self.image_remove, background='#333333', activebackground='#333333',
                   borderwidth=0, highlightthickness=0, command=lambda s=data[0]: self.remove_book(s),
                   relief="flat").place(anchor='center', relx=0.97, y=27)

        return frame

    def borrow_book(self, book_id):
        if library.already_borrowed(App.USER_ID, book_id):
            show_notification(self.frame, "You still haven't returned the book you borrowed.", fg='white')
        elif int(library.lib_dict[book_id]['Copies']) == 0:
            show_notification(self.frame, "Currently the book is unavailable.", fg='white')
        else:
            prev_bid = library.register[-1][0]
            bid = '#' + '0'*(5-len(str(int(prev_bid[1:]) + 1))) + str(int(prev_bid[1:]) + 1)
            i_date = datetime.date.today().strftime('%d-%m-%Y')
            library.register.append([bid, book_id, App.USER_ID, i_date, '-'])
            library.update_register()

            index = library.l_ids.index(book_id)
            library.books[index][7]  = int(library.books[index][7]) - 1
            library.books[index][8] = int(library.books[index][8]) + 1
            library.lib_dict[book_id]['Copies'] = library.books[index][7]
            library.lib_dict[book_id]['Borrowed'] = library.books[index][8]
            library.update_library()

            show_notification(self.frame, "You have borrowed the book successfully.", fg='white')

    def update_books(self, _):
        key = self.entry_search.get().replace(" ", "").lower()
        if key == "":
            self.list_frame.update_items(self.lib_books)
        else:
            self.prv_search = key
            books = sort_lib(key, self.lib_books, self.stripped_books)
            self.list_frame.update_items(books)

class AddBook:
    ASSETS_PATH = "assets/add_book/"
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=650, width=950, bg="#262626")

        self.image_bg = PhotoImage(file=self.get_path("frame_bg.png"))

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

        self.image_button = PhotoImage(file=self.get_path("button.png"))
        self.button_add = Button(image=self.image_button, background="#333333", activebackground="#333333", borderwidth=0, command=self.add_book)
        self.canvas.create_window((340, 520), window=self.button_add, anchor='center', height=60, width=230)

        self.canvas.create_text((310, 470), text="Copies", font=('Roboto', 12), fill="#FFFFFF")

        self.copies = IntVar(value=1)
        self.comb_box = ttk.Combobox(self.frame, textvariable=self.copies, values=[str(i) for i in range(1, 101)], background="#333333", state='readonly', exportselection=False)
        self.canvas.create_window((360, 470), window=self.comb_box, anchor='center', width=35)

        self.canvas.place(relx=0.5, rely=0.52, anchor='center')

    def get_path(self, path: str):
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
        l_id = library.books[-1][1]
        b_id = '#' + str(int(l_id[1:]) + 1)
        copies = self.comb_box.get()
        if all([len(title), len(author), len(genre), len(language), len(isbn), len(publisher)]):
            library.books.append([isbn, b_id, title, author, publisher, genre, language, copies, 0, 0])
            library.lib_dict[b_id] = {"ISBN": isbn, "Title": title, "Author": author, "Publisher": publisher, "Genre": genre,
                         "Language": language, "Copies": copies, "Borrowed": 0, "Maintenance": 0}

            library.update_library()
            show_notification(self.frame, "Added the book to Library.", fg='white')
            self.entry_isbn.config(validate='none')
            self.entry_isbn.delete(0, 'end')
            self.entry_isbn.config(validate='key')
            self.entry_title.delete(0, 'end')
            self.entry_author.delete(0, 'end')
            self.entry_publisher.delete(0, 'end')
            self.entry_genre.delete(0, 'end')
            self.entry_lang.delete(0, 'end')
            self.comb_box.set('1')

        else:
            show_notification(self.frame, "Make sure to fill all the fields.", fg='red')

class Statistics:
    ASSETS_PATH = "assets/stat/"
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=650, width=950, bg="#262626")
        self.frame.rowconfigure((0, 1), weight=1, uniform='b')
        self.frame.columnconfigure((0, 1), weight=1, uniform='a')

        self.image_lt = PhotoImage(file=self.get_path('lt.png'))
        self.image_lb = PhotoImage(file=self.get_path('lb.png'))
        self.image_rt = PhotoImage(file=self.get_path('rt.png'))
        self.image_rb = PhotoImage(file=self.get_path('rb.png'))

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
        books_borrowed = line_chart_values(library.register, dates)

        categories = ['Fiction', 'NonFiction', 'Mystery', 'Education', 'Fantasy']
        values = bar_values(library.books, categories)

        self.add_line_chart(books_borrowed, dates)
        self.add_bar_graph(categories, values)
        self.add_pie_chart(["Available", "Borrowed", "Maintenance"], pie_values(library.books))

    def get_path(self, path: str):
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
    ASSETS_PATH = "assets/register/"
    TOP_GAP = 100
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")

        self.image_notify = PhotoImage(file=self.get_path("notify_btn.png"))

        Label(self.frame, text="Borrowing History", font=("Roboto", 20, 'bold'), background='#262626', fg='white').place( x=10, y=8)
        Button(self.frame, image=self.image_notify, background='#262626', activebackground="#262626", borderwidth=0, command=self.send_notifications).place(anchor='ne', y=4, relx=1)


        self.image_left = PhotoImage(file=self.get_path("left_edge.png"))
        self.image_right = PhotoImage(file=self.get_path("right_edge.png"))

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


        self.image_i_left = PhotoImage(file=self.get_path("item_left.png"))
        self.image_i_right = PhotoImage(file=self.get_path("item_right.png"))
        self.image_done = PhotoImage(file=self.get_path("done.png"))
        self.image_return = PhotoImage(file=self.get_path("return.png"))

        self.scroll_frame = Frame(self.frame, height=self.parent.winfo_height() - self.TOP_GAP,
                                  width=self.parent.winfo_width() - 50, bg="#262626")
        self.scroll_frame.pack(expand=True, fill="both", pady=(self.TOP_GAP, 0))
        self.list_frame = ListFrame(self.scroll_frame, library.reg_info(), 60, self.create_item)

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

    def get_path(self, path: str):
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
        if data[4] != '-':
            Label(frame, image=self.image_done, background='#333333').place(anchor='ne', relx=0.97, y=14)
        else:
            Button(frame, image=self.image_return, background='#333333', activebackground='#333333', borderwidth=0,
                   command=lambda: self.return_book(data[5])).place(anchor='ne', relx=0.99, y=6)
        return frame

    def return_book(self, borrow_id):
        show_notification(self.frame, "Updating the return of book.", fg='white')
        bor_index = [row[0] for row in library.register].index(borrow_id)
        library.register[bor_index][4] = datetime.date.today().strftime('%d-%m-%Y')
        library.update_register()

        b_id = library.register[bor_index][1]
        book_index = library.l_ids.index(b_id)
        library.books[book_index][8] = int(library.books[book_index][8]) - 1
        library.books[book_index][7] = int(library.books[book_index][7]) + 1
        library.lib_dict[b_id]['Borrowed'] = library.books[book_index][8]
        library.lib_dict[b_id]['Copies'] = library.books[book_index][7]
        library.update_library()
        self.list_frame.update_items(library.reg_info())

    def send_notifications(self):
        show_notification(self.frame, "Emailing users who haven't returned books.")
        subject = "Friendly Reminder to Return Borrowed Books"
        unreturned_users = {}
        for row in library.register:
            if row[4] == '-':
                email = ua_data.users_dict[row[2]]['Email']
                name = ua_data.users_dict[row[2]]['Name']
                books = [library.lib_dict[row[1]]['Title']]
                i_date = row[3]
                try:
                    unreturned_users[email]['books']  += books
                    unreturned_users[email]['i_dates'] += [i_date]
                except KeyError:
                    unreturned_users[email] = {'name': name, 'books': books, 'i_dates': [i_date]}
        for key, value in unreturned_users.items():
            due_info = library.due_by(value['i_dates'])

            msg_info = ""
            for index, (book, due) in enumerate(zip(value['books'], due_info)):
                if due:
                    msg_info += f"{index+1}) {book} -> You have exceeded the due date and have to pay a fine of ₹{due[1]*library.FINE}\n\t\t"
                else:
                    msg_info += f"{index+1}) {book} -> {due[2]} is the last date to return the book({due[1]} more days!)\n\t\t"

            body = f"""Dear {value['name']},

\tI hope this message finds you well. I wanted to kindly remind you about the book(s) you borrowed from us. 
\tIf you have finished reading them, we would appreciate it if you could return them at your earliest convenience.

\tPlease check the list of books you currently have:
\t\t{msg_info[:-2]}
\tIf you have any issues feel free to contact us at support@booknest.com

\tThank you for your attention to this matter. We look forward to receiving the books back soon!

\tBest regards,
\tBook Nest
"""
            send_email_thread(subject, body, key)

class History:
    ASSETS_PATH = "assets/history/"
    TOP_GAP = 100

    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")
        Label(self.frame, text="Borrowing History", font=("Roboto", 20, 'bold'), background='#262626',
              fg='white').place(x=5, y=8)
        self.borrow_history = library.borrow_hist(App.USER_ID)

        self.image_left = PhotoImage(file=self.get_path("left_edge.png"))
        self.image_right = PhotoImage(file=self.get_path("right_edge.png"))

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

        self.image_i_left = PhotoImage(file=self.get_path("item_left.png"))
        self.image_i_right = PhotoImage(file=self.get_path("item_right.png"))
        self.image_borrow = PhotoImage(file=self.get_path("borrow.png"))
        self.image_undone = PhotoImage(file=self.get_path("undone.png"))

        self.scroll_frame = Frame(self.frame, height=self.parent.winfo_height() - self.TOP_GAP,
                                  width=self.parent.winfo_width() - 50, bg="#262626")
        self.scroll_frame.pack(expand=True, fill="both", pady=(self.TOP_GAP, 0))
        self.list_frame = ListFrame(self.scroll_frame, self.borrow_history, 60, self.create_item)

    def add_frame(self):
        self.list_frame.update_items(library.borrow_hist(App.USER_ID))
        self.list_frame.clean_add()
        self.frame.pack(expand=True, fill="both")

    def remove_frame(self):
        self.list_frame.clean_close()
        self.frame.pack_forget()

    def update_frame(self):
        self.head_canvas.coords(self.head_rect, 20, 0, self.parent.winfo_width() - 80, 44)
        self.head_canvas.coords(self.right_id, self.parent.winfo_width() - 73, 22)
        self.head_canvas.place(x=5, y=50, width=self.parent.winfo_width() - 60, height=50)

    def get_path(self, path: str):
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

        if data[3] != '-':
            Button(frame, image=self.image_borrow, background='#333333',activebackground='#333333', borderwidth=0,
               command=lambda : self.borrow_again(data[0])).place(anchor='ne', relx=0.99, y=6)
        else:
            Label(frame, image=self.image_undone, background='#333333').place(
                anchor='ne', relx=0.97, y=14)

        return frame

    def borrow_again(self, b_id):
        if library.already_borrowed(App.USER_ID, b_id):
            show_notification(self.frame, "You haven't returned the previous copy you borrowed.", fg='red')
        elif int(library.lib_dict[b_id]['Copies']) == 0:
            show_notification(self.frame, "Oops! The book is unavailable.", fg='red')
        else:
            prev_bid = library.register[-1][0]
            bid = '#' + '0' * (5 - len(str(int(prev_bid[1:]) + 1))) + str(int(prev_bid[1:]) + 1)
            i_date = datetime.date.today().strftime('%d-%m-%Y')
            library.register.append([bid, b_id, App.USER_ID, i_date, '-'])
            library.update_register()

            index = library.l_ids.index(b_id)
            library.books[index][8] = int(library.books[index][8]) + 1
            library.books[index][7] = int(library.books[index][7]) - 1
            library.lib_dict[b_id]['Borrowed']  = library.books[index][8]
            library.lib_dict[b_id]['Copies'] = library.books[index][7]
            library.update_library()
            self.list_frame.update_items(library.borrow_hist(App.USER_ID))
            show_notification(self.frame, "You have borrowed the book successfully.", fg='white')

class Bot:
    ASSETS_PATH = "assets/bot/"
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, height=1000, width=600, bg="#262626")

        self.image_right = PhotoImage(file=self.get_path('right.png'))
        self.image_left = PhotoImage(file=self.get_path('left.png'))
        self.image_button = PhotoImage(file=self.get_path('button.png'))

        self.image_lt = PhotoImage(file=self.get_path('tl.png'))
        self.image_lb = PhotoImage(file=self.get_path('bl.png'))
        self.image_rt = PhotoImage(file=self.get_path('tr.png'))
        self.image_rb = PhotoImage(file=self.get_path('br.png'))

        self.search_frame = Frame(self.frame, bg="#262626", width=850, height=55)
        Label(self.search_frame, image=self.image_left, bg="#262626", borderwidth=0).place(x=0, y=0)
        self.entry = Entry(self.search_frame, bd=0, highlightthickness=0, bg="#393939", font=("Roboto", 12), fg='white', insertbackground="white")
        self.entry.bind('<Return>', lambda _: threading.Thread(target=self.on_click, args=(_, )).start())
        self.entry.place(height=50, width=775, x=20, y=0)
        Label(self.search_frame, image=self.image_right, bg="#262626", borderwidth=0).place(anchor='ne', relx=1, y=0)
        Button(self.search_frame, image=self.image_button, bg="#393939", borderwidth=0, activebackground="#393939", command=lambda: threading.Thread(target=self.on_click, args=("", )).start()).place(anchor='ne', relx=0.985, y=4, height=46, width=45)
        self.search_frame.pack(side='bottom', pady=(0, 5))

        self.chat_frame = Frame(self.frame, bg='#262626', width=850)
        self.chat_frame.pack(side='bottom', fill='y', expand=True, pady=(10, 3))
        self.chat_frame.pack_propagate(False)

        self.canvas = Canvas(self.chat_frame, bg="#262626", borderwidth=0, highlightthickness=0)
        self.scroll_frame = Frame(self.canvas, bg='#262626')
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=850)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.scroll_frame.bind("<Configure>", self.update_scroll_region )

        ai_data = f"Library Columns: {[library.l_header[:7] + ['is_book_available']]}, Data: {[row[:7] + [True if row[7] else False] for row in library.books]}"
        data = prompt + ai_data
        threading.Thread(target=get_gemini_response, args=(data, )).start()
        self.chat_widget(["Welcome to the Library Assistant!\nI'm here to help you with anything related to the library. You can ask me about available books, know which suits you, or get recommendations.\nHow can I assist you today?", 'response'], self.scroll_frame)

    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        content_height = self.canvas.bbox("all")[3]
        canvas_height = self.canvas.winfo_height()

        if content_height <= canvas_height:
            self.canvas.unbind_all("<MouseWheel>")
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_click(self, _):
        query = self.entry.get()
        if query == "":
            show_notification(self.frame, "Please enter your query!")
        else:
            self.entry.delete(0, 'end')
            self.chat_widget([query, 'query'], self.scroll_frame)

            resp = get_gemini_response(query)
            self.chat_widget([resp, 'response'], self.scroll_frame)

    def chat_widget(self, data, parent):
        master_frame = Frame(parent, bg="#262626")
        temp = Frame(master_frame, bg='#262626')

        frame = Frame(master_frame, bg="#333333")

        lt = Frame(frame, bg="#262626")
        lt.place(x=0, y=0, height=12, width=13)
        Label(lt, image=self.image_lt, bg="#262626").pack()

        rt = Frame(frame, bg="#262626")
        rt.place(anchor="ne", relx=1, y=0, height=12, width=13)
        Label(rt, image=self.image_rt, bg="#262626").pack(side='left')

        lb = Frame(frame, bg="#262626")
        lb.place(anchor="sw", relx=0, rely=1, height=12, width=13)
        Label(lb, image=self.image_lb, bg="#262626").pack()

        rb = Frame(frame, bg="#262626")
        rb.place(anchor="se", relx=1, rely=1, height=12, width=13)
        Label(rb, image=self.image_rb, bg="#262626").pack(side='left')

        Label(master=frame, text=data[0], fg='white', bg='#333333', font=("Roboto", 12), wraplength=700, anchor='w', justify='left').pack(fill='x', padx=13)

        if data[-1] == 'query':
            temp.pack(fill='x', side='left', expand=True)
            frame.pack(side="left")
        elif data[-1] == 'response':
            temp.pack(fill='x', side='right', expand=True)
            frame.pack(side="right")

        master_frame.pack(fill='x', pady=(10, 0))

        self.frame.after(100, lambda: self.canvas.yview_moveto(1))
        self.update_scroll_region()

    def add_frame(self):
        self.frame.pack(expand=True, fill='both')
        self.entry.focus_set()

    def remove_frame(self):
        self.frame.pack_forget()

    def update_frame(self):
        pass

    def get_path(self, path: str):
        return self.ASSETS_PATH + path

class App(Tk):
    ASSETS_PATH = "assets/frame3/"
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
        self.bot_frame = Bot(self)

        self.add_frames    = {"HOME": self.home_frame.add_frame, "ADD": self.add_book_frame.add_frame, "STATISTICS": self.stat_frame.add_frame,
                              "REGISTER": self.register_frame.add_frame, "HISTORY": self.history_frame.add_frame, "BOT": self.bot_frame.add_frame}
        self.remove_frames = {"HOME": self.home_frame.remove_frame, "ADD": self.add_book_frame.remove_frame, "STATISTICS": self.stat_frame.remove_frame,
                              "REGISTER": self.register_frame.remove_frame, "HISTORY": self.history_frame.remove_frame, "BOT": self.bot_frame.remove_frame}
        self.update_frames = {"HOME": self.home_frame.update_frame, "ADD": self.add_book_frame.update_frame, "STATISTICS": self.stat_frame.update_frame,
                              "REGISTER": self.register_frame.update_frame, "HISTORY": self.history_frame.update_frame, "BOT": self.bot_frame.update_frame}

        # Configuring Window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{int(self.winfo_screenwidth() / 2 - self.WIDTH / 2)}+{int(self.winfo_screenheight() / 2 - self.HEIGHT / 2)}")
        self.configure(bg="#FFFFFF")
        self.title("BookNest")
        self.iconbitmap('assets/icon.ico')
        self.minsize(self.WIDTH, self.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.focus_force()


        # Loading Assets
        self.image_books = PhotoImage(file=self.get_path("button_1.png"))
        self.image_stat = PhotoImage(file=self.get_path("button_2.png"))
        self.image_plus = PhotoImage(file=self.get_path("button_3.png"))
        self.image_love = PhotoImage(file=self.get_path("button_4.png"))
        self.image_hist = PhotoImage(file=self.get_path("button_5.png"))
        self.image_home = PhotoImage(file=self.get_path("button_6.png"))

        self.image_books_hover = PhotoImage(file=self.get_path("button_hover_1.png"))
        self.image_stat_hover = PhotoImage(file=self.get_path("button_hover_2.png"))
        self.image_plus_hover = PhotoImage(file=self.get_path("button_hover_3.png"))
        self.image_love_hover = PhotoImage(file=self.get_path("button_hover_4.png"))
        self.image_hist_hover = PhotoImage(file=self.get_path("button_hover_5.png"))
        self.image_home_hover = PhotoImage(file=self.get_path("button_hover_6.png"))

        self.create_page()
        self.mainloop()

    def on_exit(self):
        self.quit()
        exit()

    def on_resize(self, _):
        self.canvas.coords(self.rect, 0, 0, 50, self.winfo_height())
        self.update_frames[self.cur_page]()

    def get_path(self, path: str):
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
                                   command=lambda: self.change_frame("BOT"), relief="flat")
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

ua_data = UserAdminManager()
library = Library()
