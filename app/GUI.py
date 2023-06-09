import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import user
import commit
import merge
import globals
import checkout
import hop
import sys
import os
import utils
import graph

# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using :0.0')
#     os.environ.__setitem__('DISPLAY', ':0.0')

# Global variables
# database_name = 'vcdb'
# vc_connect = None
# vc_cursor = None
# user_connect = None
# user_cursor = None
# current_version = None
# current_bid = None
# current_uid = None


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        #container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.iconbitmap('./image/version-control.ico')


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
        command_menu.add_command(
            label="checkout", command=lambda: self.show_frame(CheckoutPage)
        )
        command_menu.add_command(
            label="hop", command=lambda: self.show_frame(HopPage)
        )

        for F in (StartPage, InitPage, RegisterPage, LoginPage, CommitPage, LogPage, MergePage, CheckoutPage, HopPage):
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
        label = tk.Label(self, text="Welcome to VCDB system", font=("sans-serif", 30))
        label.pack(fill='both', expand=True)
        label.pack(pady=10, padx=10)


class InitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid(row=0, column=0, sticky="nsew")  # Set grid layout for InitPage frame

        label = tk.Label(self, text="Init", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        user_var = tk.StringVar()
        pwd_var = tk.StringVar()
        host_var = tk.StringVar()
        port_var = tk.StringVar()
        userDB_var = tk.StringVar()

        user_label = tk.Label(self, text='User:', font=("sans-serif", 15), justify='center')
        user_label.grid(row=1, column=0, sticky='e')
        user_entry = tk.Entry(self, textvariable=user_var, width=25)
        user_entry.insert(0, 'root')
        user_entry.grid(row=1, column=1)

        pwd_label = tk.Label(self, text='Password:', font=("sans-serif", 15), justify='center')
        pwd_label.grid(row=2, column=0, sticky='e')
        pwd_entry = tk.Entry(self, textvariable=pwd_var, show='*', width=25)
        pwd_entry.insert(0, 'dbcourse')
        pwd_entry.grid(row=2, column=1)

        host_label = tk.Label(self, text='Host:', font=("sans-serif", 15), justify='center')
        host_label.grid(row=3, column=0, sticky='e')
        host_entry = tk.Entry(self, textvariable=host_var, width=25)
        host_entry.insert(0, '127.0.0.1')
        host_entry.grid(row=3, column=1)

        port_label = tk.Label(self, text='Port:', font=("sans-serif", 15), justify='center')
        port_label.grid(row=4, column=0, sticky='e')
        port_entry = tk.Entry(self, textvariable=port_var, width=25)
        port_entry.insert(0, '3306')
        port_entry.grid(row=4, column=1)

        userDB_label = tk.Label(self, text='DB Name:', font=("sans-serif", 15), justify='center')
        userDB_label.grid(row=5, column=0, sticky='e')
        userDB_entry = tk.Entry(self, textvariable=userDB_var, width=25)
        userDB_entry.insert(0, 'userdb')
        userDB_entry.grid(row=5, column=1)

        parse_button = tk.Button(
            self,
            text='Initialize',
            command=lambda: self.init_database(
                user_var.get(), pwd_var.get(), host_var.get(), port_var.get(), userDB_var.get()
            ),
        )
        parse_button.grid(row=6, column=0, columnspan=2, pady=10)

    def init_database(self, db_user, pwd, host, port, user_db):
        return_msg = user.init(
            db_user, pwd, host, port, user_db
        )
        print("======================================")
        print("check global variables: user_connect, user_cursor, user_host, userdb_name, user_name, vc_connect, vc_cursor, ")
        print(globals.user_connect, globals.user_cursor, globals.user_host,
              globals.userdb_name, globals.user_name, globals.vc_connect, globals.vc_cursor)
        print("======================================")
        messagebox.showinfo('Init', return_msg)


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:', font=("sans-serif", 15), justify='center')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.grid(row=1, column=1)
        name_entry.insert(0, 'Leo')

        email_label = tk.Label(self, text='User Email:', font=("sans-serif", 15), justify='center')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.grid(row=2, column=1)
        email_entry.insert(0, 'Leo@gmail.com')

        parse_button = tk.Button(
            self,
            text='Register',
            command=lambda: self.register_user(
                name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def register_user(self, name, email):
        return_msg = user.register(name, email)

        if globals.vc_connect is None:
            print(
                "Error: Database connection is not initialized. Run 'init' command first.")
            messagebox.showinfo(
                'Register', "Error: Database connection is not initialized. Run 'init' command first.")
        else:
            print("======================================")
            print("check global variables: current_bid")
            print(globals.current_bid)
            messagebox.showinfo('Register', return_msg)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Login", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:', font=("sans-serif", 15), justify='center')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.insert(0, 'Leo')
        name_entry.grid(row=1, column=1)

        email_label = tk.Label(self, text='User Email:', font=("sans-serif", 15), justify='center')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.insert(0, 'Leo@gmail.com')
        email_entry.grid(row=2, column=1)

        user_var = tk.StringVar()
        pwd_var = tk.StringVar()
        host_var = tk.StringVar()
        userDB_var = tk.StringVar()

        user_label = tk.Label(self, text='User:', font=("sans-serif", 15), justify='center')
        user_label.grid(row=3, column=0, sticky='e')
        user_entry = tk.Entry(self, textvariable=user_var)
        user_entry.insert(0, 'root')
        user_entry.grid(row=3, column=1)

        pwd_label = tk.Label(self, text='Password:', font=("sans-serif", 15), justify='center')
        pwd_label.grid(row=4, column=0, sticky='e')
        pwd_entry = tk.Entry(self, textvariable=pwd_var, show='*')
        pwd_entry.insert(0, 'dbcourse')
        pwd_entry.grid(row=4, column=1)

        host_label = tk.Label(self, text='Host:', font=("sans-serif", 15), justify='center')
        host_label.grid(row=5, column=0, sticky='e')
        host_entry = tk.Entry(self, textvariable=host_var)
        host_entry.insert(0, '127.0.0.1')
        host_entry.grid(row=5, column=1)

        userDB_label = tk.Label(self, text='DB Name:', font=("sans-serif", 15), justify='center')
        userDB_label.grid(row=6, column=0, sticky='e')
        userDB_entry = tk.Entry(self, textvariable=userDB_var)
        userDB_entry.insert(0, 'userdb')
        userDB_entry.grid(row=6, column=1)

        parse_button = tk.Button(
            self,
            text='Login',
            command=lambda: self.login_user(
                user_var.get(), pwd_var.get(), host_var.get(
                ), userDB_var.get(), name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=7, column=0, columnspan=2, pady=10)

    def login_user(self, user_db, pwd, host, user_db_name, name, email):
        # try:
        #     return_msg = user.login(user_db, pwd, host, user_db_name, name, email)
        #     print("======================================")
        #     print("check global variables: user_connect, user_cursor, user_host, userdb_name, user_name, vc_connect, vc_cursor, ")
        #     print(globals.user_connect, globals.user_cursor, globals.user_host,
        #           globals.userdb_name, globals.user_name, globals.vc_connect, globals.vc_cursor)
        #     messagebox.showinfo('Login', "Login successfully.")
        #     self.controller.show_frame(CommitPage)

        # except Exception as e:
        #     print(e)
        #     messagebox.showinfo('Login', e)

        return_msg = user.login(user_db, pwd, host, user_db_name, name, email)
        user.getBnameFromBid()
        print("======================================")
        print("check global variables: user_connect, user_cursor, user_host, userdb_name, user_name, vc_connect, vc_cursor, ")
        print(globals.user_connect, globals.user_cursor, globals.user_host,
                globals.userdb_name, globals.user_name, globals.vc_connect, globals.vc_cursor)
        messagebox.showinfo('Login', return_msg)
        if return_msg != "Login fails.":
            self.controller.show_frame(CommitPage)
        

# After login show the page below
# class LogPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller

#         self.frames = {}

#         label = tk.Label(self, text="Log")
#         label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

#         name_var = tk.StringVar()
#         email_var = tk.StringVar()

#         name_label = tk.Label(self, text='User Name:')
#         name_label.grid(row=1, column=0, sticky='e')
#         name_entry = tk.Entry(self, textvariable=name_var)
#         name_entry.insert(0, 'Leo')
#         name_entry.grid(row=1, column=1)

#         email_label = tk.Label(self, text='User Email:')
#         email_label.grid(row=2, column=0, sticky='e')
#         email_entry = tk.Entry(self, textvariable=email_var)
#         email_entry.insert(0, 'Leo@gmail.com')
#         email_entry.grid(row=2, column=1)

#         parse_button = tk.Button(
#             self,
#             text='Parse',
#             command=lambda: self.login_user(
#                 name_var.get(), email_var.get()
#             ),
#         )
#         parse_button.grid(row=5, column=0, columnspan=2, pady=10)

#     def login_user(self, name, email):
#         global current_version
#         global current_bid
#         try:
#             current_version, current_bid = user.login(vc_cursor, database_name, name, email)
#             messagebox.showinfo('Login', "Login successfully.")
#             print(current_version, current_bid)
#             self.controller.show_frame()
#         except Exception as e:
#             print(e)
#             messagebox.showinfo('Login', e)


class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Commit", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        commit_var = tk.StringVar()

        commit_label = tk.Label(self, text='Commit Message:', font=("sans-serif", 15), justify='center')
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
        # try:
        #     print(globals.vc_connect, globals.user_cursor,
        #           globals.vc_cursor, globals.current_uid, globals.current_bid)
        #     version = commit.commit(msg)
        #     messagebox.showinfo('Commit', "Commit successfully.")
        # except Exception as e:
        #     print(e)
        #     messagebox.showinfo('Commit', e)
        print("======================================")
        print(globals.vc_connect, globals.user_cursor,
                  globals.vc_cursor, globals.current_uid, globals.current_bid)
        result_version = commit.commit(msg)
        if result_version != None:
            messagebox.showinfo('Commit', "Commit successfully.")
        else:
            messagebox.showinfo('Commit', "Cannot Commit.")


# After login show the page below
class LogPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Log", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.log_tree = ttk.Treeview(self, show="headings")
        self.log_tree["columns"] = ("Branch Name", "Version", "Time", "UID", "Message")
        self.log_tree.heading("Branch Name", text="Branch Name")
        self.log_tree.heading("Version", text="Version")
        self.log_tree.heading("Time", text="Time")
        self.log_tree.heading("UID", text="UID")
        self.log_tree.heading("Message", text="Message")
        self.log_tree.tag_configure("center", anchor='center')
        self.log_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        log_button = tk.Button(
            self,
            text='Log Commit',
            command=self.log_commit,
        )
        log_button.grid(row=2, column=0, columnspan=2, pady=10)

        gitgraph_button = tk.Button(
            self,
            text='Draw A VCDB Graph!',
            command=lambda: self.gitgraph(),
        )
        gitgraph_button.grid(row=3, column=0, columnspan=2, pady=10)

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
            bname = row[0]
            version = row[1]
            time = row[2]
            uid = row[3]
            message = row[4]
            self.log_tree.insert("", tk.END, values=(bname, version, time, uid, message), tags=("center",))
        # globals.current_version = result[0][1]
    def gitgraph(self):
        graph.draw_git_graph()
    
    


class MergePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Merge", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        merge_main_var = tk.StringVar()
        merge_target_var = tk.StringVar()
        self.fixed_sql_script_var = tk.StringVar()

        #main branch
        merge_main_label = tk.Label(self, text='Main Branch', font=("sans-serif", 15), justify='center')
        merge_main_label.grid(row=1, column=0, sticky='e')
        self.merge_main_entry = tk.Entry(self, textvariable=merge_main_var )
        self.merge_main_entry.grid(row=1, column=1)
        get_branch_button = tk.Button(
            self,
            text='Get Main Branch Name',
            command=lambda: self.get_current_branch(),
        )
        get_branch_button.grid(row=1, column=4, columnspan=2, pady=10)

        # target branch
        merge_target_label = tk.Label(self, text='Target Branch', font=("sans-serif", 15), justify='center')
        merge_target_label.grid(row=2, column=0, sticky='e')
        merge_target_entry = tk.Entry(self, textvariable=merge_target_var)
        merge_target_entry.grid(row=2, column=1)

        merge_button = tk.Button(
            self,
            text='merge',
            command=lambda: self.merge_GUI(
                merge_main_var.get(), merge_target_var.get()
            ),
        )
        merge_button.grid(row=2, column=3, columnspan=2, pady=10)

        separator = ttk.Separator(self, orient="horizontal")
        # separator.pack(fill="x", padx=10, pady=10)
        separator.grid(row=4, columnspan=20, sticky="ew")

        merge_conflict_label = tk.Label(self, text='Merge Conflict:', font=("sans-serif", 15), justify='center')
        merge_conflict_label.grid(row=5, column=0, sticky='e')
        self.conflict_text_entry = tk.Text(self, height=30, width=50)
        # self.conflict_text_entry = tk.Entry(self, textvariable=self.fixed_sql_script_var, height=30, width=50)
        self.conflict_text_entry.grid(row=6, column=1, columnspan=2, pady=10)


        conflict_button = tk.Button(
            self,
            text='solve conflict',
            command=lambda: self.after_merge_GUI(
                merge_main_var.get(), merge_target_var.get(), self.conflict_text_entry.get(1.0,tk.END)
            ),
        )
        conflict_button.grid(row=7, column=0, columnspan=5, pady=10)


    def merge_GUI(self, main_bname, target_bname):
        try:
            is_merged, conflict_script = merge.merge(main_bname, target_bname)
            if is_merged is False:
                self.conflict_text_entry.delete(1.0, tk.END)  # Clear previous content
                self.conflict_text_entry.insert(tk.END, conflict_script)  # Update with the return value
                print(main_bname, target_bname)
                # messagebox.showinfo('Merge', conflict_script)
            messagebox.showinfo('Merge', conflict_script)
        except Exception as e:
            print(e)
            messagebox.showinfo('Merge', e)
    
    def after_merge_GUI(self, main_bname, target_bname, fixed_sql_script):
        try:
            result = merge.merge_after_conflict_fixed(main_bname, target_bname, fixed_sql_script)
            is_merged = result[0]
            conflict_msg = result[1]
            if is_merged is False:
                conflict_script = result[2]
                
            
            #is_merged, conflict_msg, conflict_script= merge.merge_after_conflict_fixed(main_bname, target_bname, fixed_sql_script)
                print("_-------- in tkinter -----------")
            #print(conflict_script)
            #print(is_merged)
            # if is_merged is False:
                self.conflict_text_entry.delete(1.0, tk.END)  # Clear previous content
                self.conflict_text_entry.insert(tk.END, conflict_script)  # Update with the return value
                # self.update_merge_conflict_entry(fixed_sql_script, self.fixed_sql_script_var)
                print(main_bname, target_bname)
                messagebox.showinfo('Merge', conflict_msg)
            else:
                messagebox.showinfo('Merge', conflict_msg)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("============================================")
            print("Error file name: ", fname)
            print("Error Type: ", exc_type)
            print("Error occurs in line:", exc_tb.tb_lineno)
            print("Error msg:", exc_obj)
            print("============================================")
            #print(e)
            #messagebox.showinfo('Merge', e)

    def update_merge_conflict_entry(self, value):
        self.conflict_text_entry.delete(0, tk.END)  # Clear previous content
        self.conflict_text_entry.insert(0, value)
        
    def get_current_branch(self):
        # Retrieve the current branch using your implementation

        # Update the merge_main_entry widget with the current branch
        self.merge_main_entry.delete(0, tk.END)  # Clear previous content
        self.merge_main_entry.insert(0, str(globals.current_branch_name))


class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Checkout", font=("sans-serif", 25))
        label.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        newBranchName = tk.StringVar()
        isNewBranchOrNot = tk.StringVar()

        options = ["Yes", "No"]
        self.isNewBranchOrNot = tk.StringVar()
        self.isNewBranchOrNot.set(options[0])
        isNewBranchOrNot_label = tk.Label(self, text='Create New Branch?:', font=("sans-serif", 15))
        isNewBranchOrNot_label.grid(row=1, column=0, sticky='e')
        option_menu = tk.OptionMenu(self, self.isNewBranchOrNot, *options)
        option_menu.config(width=16)
        option_menu.grid(row=1, column=1)
        
        newBranchName_label = tk.Label(self, text='New Branch Name:', font=("sans-serif", 15))
        newBranchName_label.grid(row=5, column=0, sticky='e')
        newBranchName_entry = tk.Entry(self, textvariable=newBranchName)
        newBranchName_entry.grid(row=5, column=1)

        self.branch_list = tk.Text(self, height=5, width=30)
        self.branch_list.grid(row=2, column=1, sticky='e')

        parse_button = tk.Button(
            self,
            text='Get All Branches',
            command=lambda: self.getAllBranches(),
        )
        parse_button.grid(row=2, column=2, columnspan=2, pady=10)

        # isNewBranchOrNot_entry = tk.Entry(self, textvariable=isNewBranchOrNot)
        # isNewBranchOrNot_entry.grid(row=2, column=1)

        parse_button = tk.Button(
            self,
            text='Checkout',
            command=lambda: self.app_checkout(
                newBranchName.get(), isNewBranchOrNot.get()
            ),
        )
        parse_button.grid(row=9, column=1, columnspan=2, pady=10)

    def getAllBranches(self):
        result = utils.getAllBranchExceptCurrent()
        self.branch_list.delete(1.0, tk.END)  # Clear previous content
        self.branch_list.insert(1.0, result)

        

    def app_checkout(self, newBranchName, isNewBranchOrNot):
        new_ischeckout = self.isNewBranchOrNot.get()
        return_msg = checkout.checkout(
            newBranchName, new_ischeckout
        )
        messagebox.showinfo('Checkout Result:', f"{return_msg}")
    
    


class HopPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Hop", font=("sans-serif", 25), justify='center')
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        current_version_label_var = tk.StringVar()
         #main branch
        current_version_label = tk.Label(self, text='Current Version', font=("sans-serif", 15), justify='center')
        current_version_label.grid(row=1, column=0, sticky='e')
        self.current_version_label_entry = tk.Entry(self, textvariable=current_version_label_var )
        self.current_version_label_entry.grid(row=1, column=1)
        get_version_button = tk.Button(
            self,
            text='Get Current Version',
            command=lambda: self.get_current_version(),
        )
        get_version_button.grid(row=1, column=2, columnspan=2, pady=10)

        

        # destination = tk.StringVar()
        # destination_label = tk.Label(self, text='destination:', font=("sans-serif", 15), justify='center')
        # destination_label.grid(row=1, column=0, sticky='e')
        # destination_entry = tk.Entry(self, textvariable=destination)
        # destination_entry.grid(row=1, column=1)

        # options = utils.getCurrentBranchAllVersionsExceptCurrent()
        # destination = tk.StringVar()
        # destination.set(options[0])
        # destination_label = tk.Label(self, text='destination:', font=("sans-serif", 15), justify='center')
        # destination_label.grid(row=2, column=0, sticky='e')
        # option_menu = tk.OptionMenu(self, destination, *options)
        # option_menu.config(width=16)
        # option_menu.grid(row=2, column=1)

        version_list_label = tk.Label(self, text='Version List', font=("sans-serif", 15), justify='center')
        version_list_label.grid(row=3, column=0, sticky='e')
        parse_button = tk.Button(
            self,
            text='Get All Versions of Current Branch',
            command=lambda: self.getAllVersions(),
        )
        parse_button.grid(row=3, column=2, columnspan=2, pady=10)

        self.destination_list = tk.Text(self, height=5, width=27)
        self.destination_list.grid(row=3, column=1)


        destination_label = tk.Label(self, text='Destination', font=("sans-serif", 15), justify='center')
        destination_label.grid(row=2, column=0, sticky='e')
        destination = tk.StringVar()
        destination_entry = tk.Entry(self, textvariable=destination)
        destination_entry.grid(row=2, column=1)

        parse_button = tk.Button(
            self,
            text='Hop',
            command=lambda: self.hopping(
                destination.get()
            ),
        )
        parse_button.grid(row=10, column=0, columnspan=2, pady=10)

    def getAllVersions(self):
        result = utils.getCurrentBranchAllVersionsExceptCurrent()
        if len(result) == 0:
            messagebox.showinfo('Hop Result:', "Do not have more versions to hop")
        else:
            self.destination_list.delete(1.0, tk.END)  # Clear previous content
            self.destination_list.insert(1.0, result)
    
    def hopping(self, destination):
        return_msg = hop.hop(destination)
        messagebox.showinfo('Hop Result:', return_msg)

    def get_current_version(self):
        # Retrieve the current branch using your implementation

        # Update the merge_main_entry widget with the current branch
        self.current_version_label_entry.delete(0, tk.END)  # Clear previous content
        self.current_version_label_entry.insert(0, str(globals.current_version))


app = MyApp()
app.geometry("1100x700")
app.mainloop()
