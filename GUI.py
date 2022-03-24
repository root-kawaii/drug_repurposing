from html import entities
from tkinter import *
from functools import partial


def validateLogin(fields, vocabulary,entities1,relations):
	print("entered :", fields.get())
	print("entered :", vocabulary.get())
	print("entered :", relations.get())

	return

#window
tkWindow = Tk()  
tkWindow.geometry('900x700')  
tkWindow.title('Configure your Graph')

#username label and text entry box
usernameLabel = Label(tkWindow, text="Fields").grid(row=6, column=5)
fields = StringVar()
usernameEntry = Entry(tkWindow, textvariable=fields).grid(row=6, column=6) 


#password label and password entry box
passwordLabel = Label(tkWindow,text="Vocabulary").grid(row=7, column=5)  
vocabulary = StringVar()
passwordEntry = Entry(tkWindow, textvariable=vocabulary,).grid(row=7, column=6)  

passwordLabel = Label(tkWindow,text="Entities").grid(row=8, column=5)  
entities = StringVar()
passwordEntry = Entry(tkWindow, textvariable=entities,).grid(row=8, column=6)  

passwordLabel = Label(tkWindow,text="Relations").grid(row=9, column=5)  
relations = StringVar()
passwordEntry = Entry(tkWindow, textvariable=relations,).grid(row=9, column=6)  

validateLogin = partial(validateLogin, fields, vocabulary,entities,relations)

#login button
loginButton = Button(tkWindow, text="Enter", command=validateLogin).grid(row=0, column=0)  

tkWindow.mainloop()
