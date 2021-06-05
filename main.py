import os
import tkinter as tk
from tkinter.constants import DISABLED, END, HIDDEN, NORMAL
from PIL import Image, ImageTk
import quick_test as qt
import threading 
from Thread_class import KThread

#Starting of the loop
root = tk.Tk()
icon = Image.open("./Resources/icon.png")
icon = ImageTk.PhotoImage(image=icon)
root.iconphoto(True,icon)
root.title("Speed Test")

bg_color="#090e14"

canvas = tk.Canvas(root, width=500, height=400, bg=bg_color,border=0, highlightthickness=0)
root.maxsize(500,600)
root.minsize(500,400)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open("./Resources/SPEEDTEST.png")
logo.resize((200,100), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image= logo, border=0)
logo_label.image = logo
logo_label.grid(column=1, row=0)


#function for the quick_test button
def do_quick_test():
    btn_qktest["state"] = DISABLED
    #clear previous test results.
    text_box.delete('1.0', END)  
    #start new test.  
    text_box.insert(END,"Download: {} Megabits/sec\n".format(qt.do_download_test()))

    text_box.insert(END, "Upload: {} Megabits/sec\n".format(qt.do_upload_test()))

    text_box.insert(END,"The Average ping is {}ms {}".format(qt.do_ping_test(),"\n"))
    # text_box.insert(END,"yayo")
    btn_qktest["state"] =  NORMAL
    return ""
    


#text box for info
text_box = tk.Text(root, height=8, width=62 )
text_box.grid(column=1,row=3)



#instructions
instructions = tk.Label(root, text="Select an option from below.", font="Raleway", border=0, bg=bg_color,fg="white")
instructions.grid(columnspan=3, column=0, row=1)

#quick_test Button
quicktst_text = tk.StringVar()
T = KThread(target=do_quick_test)
btn_qktest = tk.Button(root, textvariable=quicktst_text, command= T.start, font="Raleway", bg="#40e0d0", height=2, width=10)



quicktst_text.set("Quick Test")
btn_qktest.grid(column=1, row=2)

canvas = tk.Canvas(root, width=500, height=200, bg=bg_color, highlightthickness=0)
canvas.grid(columnspan=3 )

#End of the loop.
root.mainloop()


