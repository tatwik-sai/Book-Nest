from tkinter import *
import _tkinter

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
            height = self.list_height
            self.canvas.unbind_all("<MouseWheel>")

        for frame in self.frame.winfo_children():
            frame.config(width=self.parent.winfo_width())
        self.master_frame.place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', height=height, width=self.parent.winfo_width())

current_notification = None
image_refs = []

def show_notification(master, msg: str, fg='white', x_pos=None):
    global current_notification, image_refs
    if current_notification is not None:
        current_notification[0].destroy()
        master.unbind("<Configure>", current_notification[1])

    if len(image_refs) == 0:
        image_lt = PhotoImage(file='assets/corners/tl.png')
        image_lb = PhotoImage(file='assets/corners/bl.png')
        image_rt = PhotoImage(file='assets/corners/tr.png')
        image_rb = PhotoImage(file='assets/corners/br.png')
        image_refs = [image_lt, image_lb, image_rt, image_rb]

    frame = Frame(master=master, bg="#333333")

    lt = Frame(frame, bg="#262626")
    lt.place(x=0, y=0, height=12, width=13)
    Label(lt, image=image_refs[0], bg="#262626").pack()

    rt = Frame(frame, bg="#262626")
    rt.place(anchor="ne", relx=1, y=0, height=12, width=13)
    Label(rt, image=image_refs[2], bg="#262626").pack(side='left')

    lb = Frame(frame, bg="#262626")
    lb.place(anchor="sw", relx=0, rely=1, height=12, width=13)
    Label(lb, image=image_refs[1], bg="#262626").pack()

    rb = Frame(frame, bg="#262626")
    rb.place(anchor="se", relx=1, rely=1, height=12, width=13)
    Label(rb, image=image_refs[3], bg="#262626").pack(side='left')

    Label(frame, text=msg, bg="#333333", fg=fg, font=("Roboto", 12)).pack(padx=13, pady=2)
    frame.place(anchor="sw", x=int(master.winfo_width()/2 - (len(msg)*9)/2) if not x_pos else int(x_pos - (len(msg)*9)/2), y=0)

    def center_align(_):
        frame.place(x=int(master.winfo_width()/2 - (len(msg)*9)/2) if not x_pos else int(x_pos - (len(msg)*9)/2))

    tag = master.bind("<Configure>", center_align, add='+')

    current_notification = (frame, tag)

    def animation(widget, tag, y=1, code='down'):
        try:
            global current_notification
            if code == "down":
                y += 1
                widget.place(y=y)
                widget.after(3, lambda: animation(widget, tag, y, 'down' if y <= 35 else 'sleep'))
            elif code == 'sleep':
                widget.after(2000, lambda: animation(widget, tag, y, 'up'))
            elif code == 'up':
                y -= 1
                widget.place(y=y)
                widget.after(3, lambda: animation(widget, tag, y, 'up' if y >= 0 else 'exit'))
            else:
                widget.destroy()
                master.unbind("<Configure>", tag)
                current_notification = None
        except _tkinter.TclError:
            return

    animation(frame, tag)