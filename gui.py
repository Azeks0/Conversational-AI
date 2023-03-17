import customtkinter
import tkinter
from PIL import ImageTk, Image
from functions.mails import *


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.after(0, lambda:root.state('zoomed'))





frame = customtkinter.CTkFrame(master=root,
                               width=1000,
                               height=200,
                               corner_radius=10)
chat = customtkinter.CTkTextbox(width=1000,height=200,master=frame,text_color="gray",font=("Arial",17),bg_color="gray")
chat.pack()
chat.insert(customtkinter.END,"input~ ")
mainframex=5
mainframey=5
frame.place(x=mainframex, y=mainframey,)
mainframex=mainframex+1000
mainframey=mainframey+200


mailsframe = customtkinter.CTkFrame(master=root,
                               width=500,
                               height=300,
                               corner_radius=10,

                               )
mailsframe.place(x=5,y=mainframey+10,)
mails = customtkinter.CTkTextbox(width=500,height=150,master=mailsframe,text_color="gray",font=("Arial",17),bg_color="blue")
mails.pack()
mails.insert(customtkinter.END, "Mails\n\nFrom : Glassdoor Jobs <noreply@glassdoor.com>\n\nSubject : Application Development Team Manager at Global Data Consultants and 17 more jobs in New York, NY for you. Apply Now.")




root.mainloop()


