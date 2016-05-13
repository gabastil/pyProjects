#!/usr/bin/env Python
import Tkinter as tk

class template_Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text = "Wanest", command = self.quit)
        self.quitButton.grid()

app = template_Application()
app.master.title("Snimbya Nibyescnitesum")
app.mainloop()
