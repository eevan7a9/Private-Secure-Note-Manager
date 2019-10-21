from tkinter import *
import sys
from tkinter import ttk, messagebox, font
from user_action import UserDb
from Note_action import NoteDb


class Gui:

    def __init__(self, master):
        self.users_action = UserDb()  # access UserDb
        self.notes_action = NoteDb()  # access NoteDb

        self.label_font = font.Font(family="Arial", size=10, weight="bold")
        self.btn_font = font.Font(family="arial", size=8, weight="bold")
        self.selected_note_id = StringVar()
        self.selected_note_title = StringVar()
        self.selected_note_title.set('Double Click to Select')
        self.confirmed_username = StringVar()  # Current users username holder
        self.confirmed_password = StringVar()  # Current users password holder
        self.confirmed_users_id = IntVar()  # Current users id holder
        self.master = master
        self.start_window = None
        self.tree_table = ttk.Treeview()
        self.selected_title = None
        self.login_window()  # To show login window

    def login_window(self):
        self.master.withdraw()
        self.start_window = Toplevel(self.master)
        self.start_window.focus_force()
        self.start_window.title("Login")
        self.start_window.geometry("360x230")
        self.start_window.resizable(0, 0)
        # self.start_window.iconbitmap(r'C:\Users\user_one\PycharmProjects\note_manager\e7.ico')

        label_app = Label(self.start_window, font=("Arial", 26, "bold"), text="Private Note Storage")
        label_app.pack(padx=10, pady=20)

        label_entry_frame = Frame(self.start_window, bg="lightBlue")
        label_entry_frame.pack(padx=10)

        label_name = Label(label_entry_frame, text="Username", font=self.label_font, bg="lightBlue")
        entered_name = Entry(label_entry_frame, width=30, font=('Arial', 10, 'bold'))

        label_pass = Label(label_entry_frame, text="Password", font=self.label_font, bg="lightBlue")
        entered_password = Entry(label_entry_frame, show="*", width=30, font=('Arial', 10, 'bold'))
        label_name.grid(row=0, column=0, pady=5, padx=10)
        entered_name.grid(row=0, column=1, padx=20)
        label_pass.grid(row=1, column=0, pady=5, padx=10)
        entered_password.grid(row=1, column=1, padx=20)

        btn_frame = Frame(self.start_window)
        btn_frame.pack()

        btn_signup = Button(btn_frame, text="Sign Up", bg="greenYellow", font=self.btn_font, command=self.register_user)
        btn_login = Button(btn_frame, text="Login", bg="lightBlue", font=self.btn_font,
                           command=lambda: self.login_action(entered_name.get(), entered_password.get()))
        btn_signup.grid(row=0, column=0, padx=40, pady=20)
        btn_login.grid(row=0, column=1)

    def content_window(self):
        self.start_window.withdraw()
        main_window = Toplevel(self.master)
        main_window.focus_force()
        main_window.geometry("510x320")
        main_window.title("Private Note Storage")
        main_window.resizable(0, 0)

        # adding menu bar
        menu_bar = Menu(main_window)
        main_window.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Item", command=lambda: self.create_edit_note("create"))
        file_menu.add_command(label="My account", command=self.user_account)
        file_menu.add_command(label="Exit", command=self.master.destroy)
        help_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about_menu)

        search_bar_frame = Frame(main_window)
        search_bar_frame.pack(anchor=W, padx=30)

        label_search = Label(search_bar_frame, text="Search Note :", font=self.label_font)
        entry_search = Entry(search_bar_frame, font=("arial", 10, "bold"), width=30)
        btn_search = Button(search_bar_frame, text="Find", font=self.btn_font, bg="greenYellow",
                            command=lambda: self.show_find_notes(entry_search.get(), self.confirmed_users_id.get()))
        btn_refresh = Button(search_bar_frame, text="Refresh", font=self.btn_font, bg="lightBlue",
                             command=self.show_notes)
        label_search.grid(row=0, column=0, pady=10)
        entry_search.grid(row=0, column=1, pady=10)
        btn_search.grid(row=0, column=2, pady=10)
        btn_refresh.grid(row=0, column=3, padx=10, pady=10)

        table_frame = Frame(main_window)
        table_frame.pack()

        self.tree_table = ttk.Treeview(table_frame, height=8)
        self.tree_table.pack(side="left")
        # adding scrollbar to our treeview Table
        scroll_bar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_table.yview)
        scroll_bar.pack(side="right", fill="y")
        self.tree_table.config(yscrollcommand=scroll_bar.set)

        self.tree_table.bind('<Double-1>', self.get_selected_note)
        self.tree_table["columns"] = ("#1", "#2", "#3", "#4", "#5")
        self.tree_table.heading("#1", text="")
        self.tree_table.heading("#2", text="Title")
        self.tree_table.heading("#3", text="Topic")
        self.tree_table.heading("#4", text="")  # this one will be hidden
        self.tree_table.heading("#5", text="Date Created")
        self.tree_table['show'] = "headings"    # to hide the first empty column
        self.tree_table.column("#1", minwidth=0, width=0)  # this one will be hidden
        self.tree_table.column("#2", width=150)
        self.tree_table.column("#3", width=150)
        self.tree_table.column("#4", minwidth=0, width=0)  # this one will be hidden
        self.tree_table.column("#5", width=150)

        selected_item_frame = Frame(main_window)
        selected_item_frame.pack(anchor=E, padx=30)

        label_selected = Label(selected_item_frame, text="Selected Item :", font=self.label_font)
        self.selected_title = Label(selected_item_frame, width=30, font=("", 11, "normal"), bg="grey", fg="#fff")
        self.selected_title.config(text=self.selected_note_title.get())
        btn_view = Button(selected_item_frame, text="View", font=self.btn_font, bg="lightBlue",
                          command=self.check_selected_note)
        label_selected.grid(row=0, column=0, pady=10)
        self.selected_title.grid(row=0, column=1, pady=10)
        btn_view.grid(row=0, column=2, pady=10)

    def create_edit_note(self, procedure):
        action = procedure
        create_edit_window = Toplevel(self.master)
        create_edit_window.grab_set()
        create_edit_window.focus_force()
        create_edit_window.geometry("350x300")
        create_edit_window.title("Notes Storage")
        create_edit_window.resizable(0, 0)
        label_entry_frame = Frame(create_edit_window)
        label_entry_frame.pack(pady=10, padx=10)

        if action == "create":
            label_title = Label(label_entry_frame, text="Title:", font=self.label_font, width=15, anchor=E)
            entry_title = Entry(label_entry_frame, font=("arial", 11, "bold"), width=30)
            label_topic = Label(label_entry_frame, text="Topic:", font=self.label_font, width=15, anchor=E)
            entry_topic = Entry(label_entry_frame, font=("arial", 11, "normal"), width=30)
            label_content = Label(label_entry_frame, text="Content:", font=self.label_font, width=15, anchor=E)
            entry_content = Text(label_entry_frame, font=("", 8, "normal"), width=40, height=10)
            label_title.grid(row=0, column=0, pady=5)
            entry_title.grid(row=0, column=1, pady=5)
            label_topic.grid(row=1, column=0, pady=5)
            entry_topic.grid(row=1, column=1, pady=5)
            label_content.grid(row=2, column=0, pady=5)
            entry_content.grid(row=2, column=1, pady=5)

            btn_frame = Frame(create_edit_window)
            btn_frame.pack(pady=10, padx=10)

            btn_create = Button(btn_frame, text="Create", font=self.btn_font, bg="greenYellow",
                                command=lambda: self.create_new_note(entry_title.get(), entry_topic.get(),
                                                                     entry_content.get(1.0, "end-1c"),
                                                                     create_edit_window))

            btn_create.grid(row=0, column=0)
        elif action == "edit":
            create_edit_window.geometry("550x500")
            for rows in self.notes_action.get_user_notes('id', self.selected_note_id.get()):
                note_title = rows[1]
                note_topic = rows[2]
                note_content = self.notes_action.decrypt_content(rows[3], self.confirmed_password.get())
                note_created_at = rows[4]
                note_modified_at = rows[5]

                label_title = Label(label_entry_frame, text="Title:", font=self.label_font, width=15, anchor=E)
                entry_title = Entry(label_entry_frame, font=("arial", 11, "bold"), width=50)
                entry_title.insert(0, note_title)
                label_topic = Label(label_entry_frame, text="Topic:", font=self.label_font, width=15, anchor=E)
                entry_topic = Entry(label_entry_frame, font=("arial", 11, "normal"), width=50)
                entry_topic.insert(0, note_topic)
                label_content = Label(label_entry_frame, text="Content:", font=self.label_font, width=15, anchor=E)
                entry_content = Text(label_entry_frame, font=("", 12, "normal"), width=50, height=10)
                entry_content.insert(0.0, note_content)
                label_created_at = Label(label_entry_frame, text="Created at:", font=self.label_font, width=15,
                                         anchor=E)
                created_at = Label(label_entry_frame, font=("arial", 11, "normal"), width=28, bg="grey", fg="white")
                created_at.config(text=note_created_at)
                label_modified_at = Label(label_entry_frame, text="Last modified:", font=self.label_font, width=15,
                                          anchor=E)
                modified_at = Label(label_entry_frame, font=("arial", 11, "normal"), width=28, bg="grey", fg="white")
                modified_at.config(text=note_modified_at)
                label_title.grid(row=0, column=0, pady=8)
                entry_title.grid(row=0, column=1, pady=8)
                label_topic.grid(row=1, column=0, pady=8)
                entry_topic.grid(row=1, column=1, pady=8)
                label_content.grid(row=2, column=0, pady=8)
                entry_content.grid(row=2, column=1, pady=8)
                label_created_at.grid(row=3, column=0, pady=10)
                created_at.grid(row=3, column=1, pady=10)
                label_modified_at.grid(row=4, column=0, pady=10)
                modified_at.grid(row=4, column=1, pady=10)

            btn_frame = Frame(create_edit_window)
            btn_frame.pack(pady=10, padx=10)

            btn_update = Button(btn_frame, text="Update", font=self.btn_font, bg="lightBlue",
                                command=lambda: self.update_existing_note(entry_title.get(), entry_topic.get(),
                                                                          entry_content.get(1.0, "end-1c"),
                                                                          self.selected_note_id.get(),
                                                                          create_edit_window))
            btn_update.grid(row=0, column=1, padx=20)
            btn_delete = Button(btn_frame, text="Delete", font=self.btn_font, bg="Red", fg="white",
                                command=lambda: self.delete_note(create_edit_window))
            btn_delete.grid(row=0, column=0, padx=30)

    def register_user(self):
        register_window = Toplevel(self.master)
        register_window.focus_force()
        register_window.grab_set()
        register_window.geometry("550x150")
        register_window.title("Create Account")
        register_window.resizable(0, 0)

        label_entry_frame = Frame(register_window, bg="lightBlue")
        label_entry_frame.pack()

        label_register_name = Label(label_entry_frame, text="Username", font=self.label_font, width=15, anchor=E,
                                    bg="lightBlue")
        entry_register_name = Entry(label_entry_frame, font=("arial", 9, "bold"), width=30)
        label_register_pass = Label(label_entry_frame, text="Password", font=self.label_font, width=15, anchor=E,
                                    bg="lightBlue")
        entry_register_pass = Entry(label_entry_frame, font=("arial", 9, "bold"), width=30, show="*")
        label_register_confirm = Label(label_entry_frame, text="Confirm Password", font=self.label_font, width=20,
                                       anchor=E, bg="lightBlue")
        entry_register_confirm = Entry(label_entry_frame, font=("arial", 9, "bold"), width=30, show="*")

        label_register_name.grid(row=0, column=0, pady=5, padx=10)
        entry_register_name.grid(row=0, column=1, pady=5, padx=10)
        label_register_pass.grid(row=1, column=0, pady=5, padx=10)
        entry_register_pass.grid(row=1, column=1, pady=5, padx=10)
        label_register_confirm.grid(row=2, column=0, pady=5, padx=20)
        entry_register_confirm.grid(row=2, column=1, pady=5, padx=20)

        btn_frame = Frame(register_window)
        btn_frame.pack()

        btn_create = Button(btn_frame, text="Create", font=self.btn_font, bg="greenYellow", anchor=E,
                            command=lambda: self.register_action(entry_register_name.get(), entry_register_pass.get(),
                                                                 entry_register_confirm.get(), register_window))
        btn_create.grid(row=0, column=0, pady=10, padx=10)

    def user_account(self):
        account_window = Toplevel(self.master)
        account_window.focus_force()
        account_window.grab_set()
        account_window.geometry("240x150")
        account_window.title("Account Info")
        account_window.resizable(0, 0)

        account_frame = Frame(account_window)
        account_frame.pack(pady=10, padx=10)

        label_name = Label(account_frame, text="Username :", font=self.label_font)
        entry_name = Label(account_frame)
        entry_name.config(text=self.confirmed_username.get())

        label_created_at = Label(account_frame, text="Date created :", font=self.label_font)
        created_at = Label(account_frame)
        for created in self.users_action.get_user_info('created_at', self.confirmed_username.get()):
            created_account_date = created
            created_at.config(text=created_account_date)

        label_number_notes = Label(account_frame, text="No. of Notes :", font=self.label_font)
        number_notes = Label(account_frame)
        for number in self.notes_action.count_notes(self.confirmed_users_id.get()):
            number_notes.config(text=number)

        label_name.grid(row=0, column=0, pady=5, padx=10)
        entry_name.grid(row=0, column=1, pady=5, padx=10)
        label_created_at.grid(row=1, column=0, pady=5, padx=10)
        created_at.grid(row=1, column=1, pady=5, padx=10)
        label_number_notes.grid(row=2, column=0, pady=5, padx=10)
        number_notes.grid(row=2, column=1, pady=5, padx=10)

    def about_menu(self):
        about_window = Toplevel(self.master)
        about_window.focus_force()
        about_window.grab_set()
        about_window.geometry("510x430")
        about_window.title("App Info")
        about_window.resizable(0, 0)

        about_frame = Frame(about_window)
        about_frame.pack(pady=10, padx=10)

        info = "Register and login. \n# This App will encrypt the notes you created\nand keep you're notes secure and private\n" \
               "# encrypted notes will be decrypted only  when viewed by its owner\n" \
               "# You must not lose you're password , If you lose you're password, you'll lose you're notes\n" \
               "\nTechnology used: Passlib for hashing user password" \
               "\nTechnology used: pycryptodome for encrypting Notes"

        label_name = Label(about_frame, text="App name :", font=self.label_font)
        app_name = Label(about_frame)
        app_name.config(text="Private Note Storage")

        label_created_at = Label(about_frame, text="Date created :", font=self.label_font)
        created_at = Label(about_frame)
        created_at.config(text="10/19/2018")

        app_info = Text(about_window, width=60, height=15, font=("arial", 10, "normal"), fg="greenYellow", bg="#444")
        app_info.insert(0.0, info)

        label_name.grid(row=0, column=0, pady=5, padx=10)
        app_name.grid(row=0, column=1, pady=5, padx=10)
        label_created_at.grid(row=1, column=0, pady=5, padx=10)
        created_at.grid(row=1, column=1, pady=5, padx=10)
        app_info.pack()

    def login_action(self, username, password):
        users_username = username
        users_password = password
        if (users_username is not "") and (users_password is not ""):
            if self.users_action.get_user_info('username', users_username):
                if self.users_action.verify_password(users_username, users_password):
                    self.confirmed_username.set(users_username)
                    self.confirmed_password.set(users_password)
                    for user_id in self.users_action.get_user_info('id', users_username):
                        self.confirmed_users_id.set(user_id)
                    self.content_window()
                    self.show_notes()
                else:
                    self.message_popup('Wrong Credentials', 'Invalid :username or password', 'warning')
            else:
                self.message_popup('Wrong Credentials', 'Invalid :username or password', 'warning')
        else:
            self.message_popup('Empty Field', 'Required: Username and password', 'info')

    def register_action(self, username, password, confirm_password, window):
        if username is not "":
            db_result = self.users_action.get_user_info('username', username)
            if db_result is None:
                if password is not "":
                    if password == confirm_password:
                        self.users_action.insert_user(username, confirm_password)
                        print("success")
                        window.grab_release()
                        window.withdraw()
                        self.message_popup('Success', 'you are now registered', 'info')
                    else:
                        self.message_popup("Confirmation Failed",
                                           "Confirm Password did not match to you're Password", "error")
                else:
                    self.message_popup('Empty Field', 'Must Provide Password', 'error')
            else:
                self.message_popup('Invalid Name', 'Name is already taken', 'error')
        else:
            self.message_popup('Empty Field', 'Must Provide Username', 'error')

    def show_notes(self):
        # clear treeView children
        for note in self.tree_table.get_children():
            self.tree_table.delete(note)
        # Show Users Notes
        for notes in self.notes_action.get_user_notes('created_by', self.confirmed_users_id.get()):
            self.tree_table.insert('', 0, values=notes)

    def show_find_notes(self, value, user_id):
        for note in self.tree_table.get_children():
            self.tree_table.delete(note)

        for notes in self.notes_action.find_note(value, user_id):
            self.tree_table.insert('', 0, value=notes)

    def get_selected_note(self, event):
        # Get Selected note from the Table/TreeView
        for selected_note in self.tree_table.selection():
            note = self.tree_table.item(selected_note, 'value')
            self.selected_note_id.set(note[0])
            self.selected_note_title.set(note[1])
            self.show_selected_title(self.selected_note_title.get())

    def show_selected_title(self, title):
        self.selected_title.config(text=title)

    def reset_selected(self):
        self.selected_note_id.set('')
        self.show_selected_title('Double Click to Select')

    def back_to_window(self, window):
        self.show_notes()
        window.grab_release()
        window.withdraw()
        self.reset_selected()

    def create_new_note(self, title, topic, content, window):
        self.notes_action.create_note(title, topic, content, self.confirmed_password.get(),
                                      self.confirmed_users_id.get())
        self.back_to_window(window)

    def update_existing_note(self, title, topic, content, note_id, window):
        self.notes_action.update_note('title', title, note_id)
        self.notes_action.update_note('topic', topic, note_id)
        self.notes_action.update_note('content', content, note_id, self.confirmed_password.get())
        self.back_to_window(window)

    def check_selected_note(self):
        if self.selected_note_id.get() is not "":
            self.create_edit_note('edit')
        else:
            self.message_popup('Empty', 'Select a note to view', 'info')

    def delete_note(self, window):
        answer = self.message_popup('Delete This?', "You are about to DELETE this Note.\nAre you sure?", 'question')
        if answer == "yes":
            self.notes_action.remove_note(self.selected_note_id.get())
            self.back_to_window(window)
        else:
            self.back_to_window(window)

    @staticmethod
    def message_popup(title, text, type_alert):

        if type_alert == "info":
            messagebox.showinfo('{}'.format(title), '{}'.format(text))
        elif type_alert == "warning":
            messagebox.showwarning('{}'.format(title), '{}'.format(text))
        elif type_alert == "question":
            result = messagebox.askquestion('{}'.format(title), '{}'.format(text), icon='warning', default='no')
            return result
        elif type_alert == "error":
            messagebox.showerror('{}'.format(title), '{}'.format(text))


root = Tk()
app = Gui(root)
root.mainloop()
