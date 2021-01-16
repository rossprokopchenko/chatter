import tkinter as tk

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.username = ""

        self.frames = {}
        for F in (Login, App):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame 

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.configure(bg="#1b1b1b")

        if(page_name == "Login"):
            windowWidth = 300
            windowHeight = 300
            posWidth = int(frame.winfo_screenwidth()/2 - windowWidth/2)
            posHeight = int(frame.winfo_screenheight()/2 - windowHeight/2)
            window = frame.winfo_toplevel()

            window.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, posWidth, posHeight))
            window.resizable(False, False)
            window.title("Login Page")

        elif(page_name == "App"):
            windowWidth = 800
            windowHeight = 500
            posWidth = int(frame.winfo_screenwidth()/2 - windowWidth/2)
            posHeight = int(frame.winfo_screenheight()/2 - windowHeight/2)
            window = frame.winfo_toplevel()

            window.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, posWidth, posHeight))
            window.resizable(True, True)
            window.title("Roskord")

        frame.grid()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.wrongEntries = 0
        
        
        self.frame = tk.Frame(self, highlightbackground="#3d3d3d", highlightthickness=.5, borderwidth=10)
        self.logoLabel = tk.Label(self.frame, text="COMPANY NAME INC.", font=("Sans", 10), pady=10)
        self.logoLabel.grid(sticky=tk.NSEW)
        self.usernameLabel = tk.Label(self.frame, text="Username")
        self.usernameLabel.grid(sticky=tk.W)
        self.entry1 = tk.Entry(self.frame)
        self.entry1.grid()
        self.entry1.focus()
        self.passwordLabel = tk.Label(self.frame, text="Password")
        self.passwordLabel.grid(sticky=tk.W)
        self.entry2 = tk.Entry(self.frame, show="•")
        self.entry2.grid()
        # c = Checkbutton(root, text="check")

        self.login = tk.Button(self.frame, text="log in", bg="#3d3d3d", fg="white", borderwidth=2, relief=tk.RAISED)
        self.login.config(command = lambda : controller.show_frame("App") if self.rightEntry() else self.createWrongLabel())
        self.login.grid(pady=7)
        self.helpLabel = tk.Label(self.frame, text="Username must not be empty.\nPass must be 12345.", font=("Sans", 8))
        self.helpLabel.grid()

        self.frame.place(relx=.5, rely=.5, anchor="c")

        self.entry1.bind("<Return>", lambda event : self.buttonPress(event))
        self.entry2.bind("<Return>", lambda event : self.buttonPress(event))
        self.login.bind("<Return>", lambda event : self.buttonPress(event))


    def buttonPress(self, event):
        self.login.config(relief=tk.SUNKEN)
        self.login.after(50, lambda : self.login.config(relief=tk.RAISED))
        self.login.invoke()

# Password must be 12345 in order to pass login page
    def rightEntry(self):
        if self.entry1.get() != "" and self.entry2.get() == "12345":
            self.controller.username = self.entry1.get()
            print(self.controller.username)
            return True

    def createWrongLabel(self):
        if self.wrongEntries == 0:
            self.wrongLabel = tk.Label(self.frame, text="Wrong user or pass", fg="red")
            self.wrongLabel.grid()

        self.entry2.delete(0, "end")
        self.wrongEntries += 1

class App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.frame = tk.Frame(self, width=400, height=500)
        self.frame.config(bg="grey", highlightthickness=.5, borderwidth=2, relief=tk.RAISED)

        self.canvas = tk.Canvas(self.frame, borderwidth=0, background="grey")
        self.messageFrame = tk.Frame(self.canvas, background="grey")
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.messageFrame, anchor="nw",
                                  tags="self.frame")

        self.messageFrame.bind("<Configure>", self.onFrameConfigure)

        self.messageEntry = tk.Text(self.frame, wrap=tk.WORD, height=1)
        self.messageEntry.focus()
        self.messageEntry.pack(fill="x", padx=5, pady=5, side="bottom")

        self.frame.pack(expand=True, fill="y", anchor="center", padx=10, pady=10)
        self.frame.pack_propagate(0)

        controller.bind("<Return>", lambda event : self.createMessage() if any(c.isalpha() for c in self.messageEntry.get("1.0", "end")) else self.messageEntry.delete("1.0", "end"))

    def createMessage(self):
        message = self.controller.username + ": " + self.messageEntry.get("1.0", "end")
        frameWidth = self.frame.winfo_width() - self.scrollbar.winfo_width() - 15
        self.newMessage = tk.Text(self.messageFrame, bg="grey", fg="black", font=("Arial", 10), width=52, relief=tk.FLAT, yscrollcommand=0)
        self.newMessage.insert(tk.END, message.rstrip())

        self.newMessage.config(height=int(self.newMessage.index('end').split('.')[0]), state=tk.DISABLED)
        self.newMessage.pack(side=tk.TOP, anchor=tk.W, pady=2, padx=2, expand=1)

        self.messageEntry.delete("1.0", "end")

    def modifyMessage(self):
        pass

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

