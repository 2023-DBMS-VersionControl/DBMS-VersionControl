import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import user
import commit
import merge
import globals
import sys


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)
        self.config(menu=menu)

        command_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Pages", menu=command_menu)
        command_menu.add_command(
            label="Init", command=lambda: self.show_frame(InitPage)
        )
        command_menu.add_command(
            label="Register", command=lambda: self.show_frame(RegisterPage)
        )
        command_menu.add_command(
            label="Login", command=lambda: self.show_frame(LoginPage)
        )
        command_menu.add_command(
            label="commit", command=lambda: self.show_frame(CommitPage)
        )
        command_menu.add_command(
            label="log", command=lambda: self.show_frame(LogPage)
        )
        command_menu.add_command(
            label="merge", command=lambda: self.show_frame(MergePage)
        )

        for F in (StartPage, InitPage, RegisterPage, LoginPage, CommitPage, LogPage, MergePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to DBVC system")
        label.pack(pady=10, padx=10)


class InitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Init")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        user_var = tk.StringVar()
        pwd_var = tk.StringVar()
        host_var = tk.StringVar()
        port_var = tk.StringVar()
        userDB_var = tk.StringVar()

        user_label = tk.Label(self, text='User:')
        user_label.grid(row=1, column=0, sticky='e')
        user_entry = tk.Entry(self, textvariable=user_var)
        user_entry.insert(0, 'root')
        user_entry.grid(row=1, column=1)

        pwd_label = tk.Label(self, text='Password:')
        pwd_label.grid(row=2, column=0, sticky='e')
        pwd_entry = tk.Entry(self, textvariable=pwd_var)
        pwd_entry.insert(0, 'secure1234')
        pwd_entry.grid(row=2, column=1)

        host_label = tk.Label(self, text='Host:')
        host_label.grid(row=3, column=0, sticky='e')
        host_entry = tk.Entry(self, textvariable=host_var)
        host_entry.insert(0, '127.0.0.1')
        host_entry.grid(row=3, column=1)

        port_label = tk.Label(self, text='Port:')
        port_label.grid(row=4, column=0, sticky='e')
        port_entry = tk.Entry(self, textvariable=port_var)
        port_entry.insert(0, '3306')
        port_entry.grid(row=4, column=1)

        userDB_label = tk.Label(self, text='DB Name:')
        userDB_label.grid(row=4, column=0, sticky='e')
        userDB_entry = tk.Entry(self, textvariable=userDB_var)
        userDB_entry.insert(0, 'userdb')
        userDB_entry.grid(row=4, column=1)

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.init_database(
                user_var.get(), pwd_var.get(), host_var.get(), port_var.get(), userDB_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    # def init_database(self, db_user, pwd, host, port, user_db):
    #     global vc_connect, vc_cursor, user_connect, user_cursor
    #     vc_connect, vc_cursor, user_connect, user_cursor = user.init(
    #         db_user, pwd, host, port, user_db
    #     )

    #     print("vc_connect: ",vc_connect, "vc_cursor: ", vc_cursor, "user_connect: ", user_connect, "user_cursor: ",user_cursor)
    #     messagebox.showinfo('Init', 'Database initialized successfully.')

    def init_database(self, db_user, pwd, host, port, user_db):
        user.init(
            db_user, pwd, host, port, user_db
        )
        #print("vc_connect: ",vc_connect, "vc_cursor: ", vc_cursor, "user_connect: ", user_connect, "user_cursor: ",user_cursor)
        print("======================================")
        print("check global variables: vc_connect, vc_cursor")
        print(globals.vc_connect, globals.vc_cursor)
        print("======================================")
        messagebox.showinfo('Init', 'Database initialized successfully.')


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.grid(row=1, column=1)
        name_entry.insert(0, 'Leo')

        email_label = tk.Label(self, text='User Email:')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.grid(row=2, column=1)
        email_entry.insert(0, 'Leo@gmail.com')

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.register_user(
                name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def register_user(self, name, email):
        user.register(name, email)
        
        if globals.vc_connect is None:
            print("Error: Database connection is not initialized. Run 'init' command first.")
            messagebox.showinfo('Register', "Error: Database connection is not initialized. Run 'init' command first.")
        else:
            print("======================================")
            print("check global variables: current_bid")
            print(globals.current_bid)
            messagebox.showinfo('Register', 'User registered successfully.')


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Login")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.insert(0, 'Leo')
        name_entry.grid(row=1, column=1)

        email_label = tk.Label(self, text='User Email:')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.insert(0, 'Leo@gmail.com')
        email_entry.grid(row=2, column=1)

        user_var = tk.StringVar()
        pwd_var = tk.StringVar()
        host_var = tk.StringVar()
        userDB_var = tk.StringVar()

        user_label = tk.Label(self, text='User:')
        user_label.grid(row=3, column=0, sticky='e')
        user_entry = tk.Entry(self, textvariable=user_var)
        user_entry.insert(0, 'root')
        user_entry.grid(row=3, column=1)

        pwd_label = tk.Label(self, text='Password:')
        pwd_label.grid(row=4, column=0, sticky='e')
        pwd_entry = tk.Entry(self, textvariable=pwd_var)
        pwd_entry.insert(0, 'secure1234')
        pwd_entry.grid(row=4, column=1)

        host_label = tk.Label(self, text='Host:')
        host_label.grid(row=5, column=0, sticky='e')
        host_entry = tk.Entry(self, textvariable=host_var)
        host_entry.insert(0, '127.0.0.1')
        host_entry.grid(row=5, column=1)

        userDB_label = tk.Label(self, text='DB Name:')
        userDB_label.grid(row=6, column=0, sticky='e')
        userDB_entry = tk.Entry(self, textvariable=userDB_var)
        userDB_entry.insert(0, 'userdb')
        userDB_entry.grid(row=6, column=1)

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.login_user(
                user_var.get(), pwd_var.get(), host_var.get(), userDB_var.get(),name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=7, column=0, columnspan=2, pady=10)

    def login_user(self, user_db, pwd, host, user_db_name,name, email):
        try:
            user.login(user_db, pwd, host, user_db_name, name, email)
            messagebox.showinfo('Login', "Login successfully.")
            print(globals.current_uid, globals.current_version, globals.current_bid)
            self.controller.show_frame(CommitPage)
        except Exception as e:
            print(e)
            messagebox.showinfo('Login', e)

class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Commit")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        commit_var = tk.StringVar()

        commit_label = tk.Label(self, text='Commit Message:')
        commit_label.grid(row=1, column=0, sticky='e')
        commit_entry = tk.Entry(self, textvariable=commit_var)
        commit_entry.insert(0, 'Enter your commit message')
        commit_entry.grid(row=1, column=1)

        parse_button = tk.Button(
            self,
            text='commit',
            command=lambda: self.commit_user(
                commit_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def commit_user(self, msg):
        try:
            print(globals.vc_connect, globals.user_cursor, globals.vc_cursor, globals.current_uid, globals.current_bid)
            commit.commit(msg)
            messagebox.showinfo('Commit', "Commit successfully.")
        except Exception as e:
            print(e)
            messagebox.showinfo('Commit', e)

# After login show the page below
class LogPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Log")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.log_tree = ttk.Treeview(self, show="headings")
        self.log_tree["columns"] = ("Version", "Time", "UID", "Message")
        self.log_tree.heading("Version", text="Version")
        self.log_tree.heading("Time", text="Time")
        self.log_tree.heading("UID", text="UID")
        self.log_tree.heading("Message", text="Message")
        self.log_tree.tag_configure("center", anchor="center")
        self.log_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        log_button = tk.Button(
            self,
            text='Log Commit',
            command=self.log_commit,
        )
        log_button.grid(row=2, column=0, columnspan=2, pady=10)

    def log_commit(self):
        try:
            result = user.log()
            self.populate_log_tree(result)
            messagebox.showinfo('Log', "Log successfully.")
        except Exception as e:
            print(e)
            messagebox.showinfo('Log', e)

    def populate_log_tree(self, result):
        self.log_tree.delete(*self.log_tree.get_children())
        for row in result:
            version = row[0]
            time = row[1]
            uid = row[2]
            message = row[3]
            self.log_tree.insert("", tk.END, values=(version, time, uid, message), tags=("center",))



class MergePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Merge")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        merge_main_var = tk.StringVar()
        merge_target_var = tk.StringVar()
        conflict_var = tk.StringVar()

        merge_target_label = tk.Label(self, text='Merge Branch from')
        merge_target_label.grid(row=1, column=0, sticky='e')
        merge_target_entry = tk.Entry(self, textvariable=merge_target_var)
        merge_target_entry.grid(row=1, column=1)

        merge_main_label = tk.Label(self, text='To:')
        merge_main_label.grid(row=2, column=0, sticky='e')
        merge_main_entry = tk.Entry(self, textvariable=merge_main_var)
        # merge_main_entry.insert(0, str(merge.getBranchName(current_bid)))
        merge_main_entry.grid(row=2, column=1)
        
        merge_main_label = tk.Label(self, text='Merge Conflict:')
        merge_main_label.grid(row=3, column=0, sticky='e')
        self.result_text = tk.Text(self, height=30, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, pady=10)

        merge_button = tk.Button(
            self,
            text='merge',
            command=lambda: self.merge_GUI(
                merge_main_var.get(), merge_target_var.get()
            ),
        )
        merge_button.grid(row=5, column=0, columnspan=2, pady=10)

        conflict_button = tk.Button(
            self,
            text='solve conflict',
            command=lambda: self.merge_GUI(
                merge_main_var.get(), merge_target_var.get()
            ),
        )
        conflict_button.grid(row=5, column=2, columnspan=5, pady=10)


    def merge_GUI(self, main_bname, target_bname):
        try:
            conflict_msg = merge.merge(main_bname, target_bname)
            self.result_text.delete(1.0, tk.END)  # Clear previous content
            self.result_text.insert(tk.END, conflict_msg)  # Update with the return value
            print(main_bname, target_bname)
        
        except Exception as e:
            print(e)
            messagebox.showinfo('Merge', e)
    
    def after_merge_GUI(self, main_bname, target_bname, fixed_sql_script):
        try:
            merge.merge_after_conflict_fixed(main_bname, target_bname, fixed_sql_script)
        
        except Exception as e:
            print(e)
            messagebox.showinfo('Merge', e)

    def update_merge_main_entry(self, value, conflict_var):
        self.merge_main_entry = tk.Entry(self, textvariable=conflict_var)
        self.merge_main_entry.delete(0, tk.END)  # Clear previous content
        self.merge_main_entry.insert(0, value)

app = MyApp()
app.geometry("800x600")
app.mainloop()
