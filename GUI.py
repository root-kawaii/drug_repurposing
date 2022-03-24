from html import entities
from tkinter import *
from functools import partial

root = Tk()
root.geometry('500x250')  
root.title('Configure your Graph')
Label(root, text = "Fields",font=("Arial", 15)).grid(row = 0, sticky = W)
Label(root, text = "Vocabulary",font=("Arial", 15)).grid(row = 1, sticky = W)
Label(root, text = "Entities",font=("Arial", 15)).grid(row = 2, sticky = W)
Label(root, text = "Relations",font=("Arial", 15)).grid(row = 3, sticky = W)


fields = Entry(root,font=("Arial", 15))
voc = Entry(root,font=("Arial", 15))
ent = Entry(root,font=("Arial", 15))
rel = Entry(root,font=("Arial", 15))


fields.grid(row = 0, column = 1)
voc.grid(row = 1, column = 1)
ent.grid(row = 3, column = 1)
rel.grid(row = 2, column = 1)


def getInput():

    a = fields.get()
    b = voc.get()
    c = ent.get()
    d = rel.get()
    
    global params
    params = [a,b,c,d]
    print(params)

Button(root, text = "submit",font=("Arial", 15),command = getInput).grid(row = 5, sticky = W)

root.mainloop()

#here i need to edit params in order to put commas in between values and 
#handle multiple inputs in same field

f = open("config2.yaml",'a')
f.write("{\n\'file\':[\n" + str(params[0]) + "\n],\n\'Vocabulary\':[" + str(params[1])
 + "\n],\n\'entities\':[" + str(params[2]) + "\n],\n\'relations\':[" + str(params[3]) + "]\n}" )
