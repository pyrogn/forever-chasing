import tkinter as tk


def onKeyPress(event):
    text.insert("end", "You pressed %s|%s\n" % (event.char, event.keysym))


root = tk.Tk()
root.geometry("300x200")
text = tk.Text(root, background="black", foreground="white", font=("Comic Sans MS", 12))
text.pack()
root.bind("<KeyPress>", onKeyPress)
root.mainloop()

# brew install python-tk # for MacOS
# import tkinter as tk  # either in python 2 or in python 3
#
#
# def event_handle(event):
#     # Replace the window's title with event.type: input key
#     root.title("{}: {}".format(str(event.type), event.keysym))
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     event_sequence = "<KeyPress>"
#     root.bind(event_sequence, event_handle)
#     root.bind("<KeyRelease>", event_handle)
#     root.mainloop()
