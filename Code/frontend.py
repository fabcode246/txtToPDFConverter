from tkinter import filedialog, Frame, Scrollbar, Label, Text, Button, Tk
from backend import pdfMaker

root = Tk()
root.title("PyDF")
root.geometry("1000x600")
root.maxsize(979, 585)

filename = None

#Functions

def newFile(flag=True):
	textBox.delete("1.0", "end")
	root.title("PyDF - untitled")

def openFile(flag=True):
	global filename
	filename = filedialog.askopenfilename()
	with open(filename, "r")as file:
		text = file.read()
		textBox.insert("end", text)
	root.title(f"PyDF - {filename}")

def saveFile(flag=True):
	global filename
	if filename == None:
		filename = filedialog.asksaveasfilename(defaultextension='.txt')
		root.title(f"PyDF - {filename}")
	with open(filename, 'w')as file:
		file.write(textBox.get("1.0", "end"))

def saveAsFile(flag=True):
	global filename
	filename = filedialog.asksaveasfilename(defaultextension='.txt')
	with open(filename, 'w')as file:
		file.write(textBox.get("1.0", "end"))
	root.title(f"PyDF - {filename}")

def saveAsPDF(flag=True):
	pdf = pdfMaker(textBox.get("1.0", "end"))
	pdf.txtRead()
	pagelist = []
	for i in range(len(pdf.pages)):
		pagelist.append(pdf.pageCreate(i))
	pagelist = pdf.converter(pagelist)
	savepath = filedialog.asksaveasfilename(defaultextension='.pdf', title="Save As PDF")	
	pdf.makePDF(pagelist, savepath)

#Top Bar

frame1 = Frame(root, bg="#353535")
frame1.place(x=0, y=0)

newButton = Button(frame1, bd=0, text="New", command=newFile, bg="#404040", activebackground="#454545", fg="#ff6600", pady=10)
newButton.grid(row=0, column=0)

openButton = Button(frame1, bd=0, text="Open", command=openFile, bg="#404040", activebackground="#454545", fg="#ff6600", pady=10)
openButton.grid(row=0, column=1, padx=5)

saveButton = Button(frame1, bd=0, text="Save", command=saveFile, bg="#404040", activebackground="#454545", fg="#ff6600", pady=10)
saveButton.grid(row=0, column=2)

saveAsButton = Button(frame1, bd=0, text="Save as", command=saveAsFile, bg="#404040", activebackground="#454545", fg="#ff6600", pady=10)
saveAsButton.grid(row=0, column=3, padx=5)

saveAsPdfButton = Button(frame1, bd=0, text="Save as PDF", command=saveAsPDF, bg="#404040", activebackground="#454545", fg="#ff6600", pady=10)
saveAsPdfButton.grid(row=0, column=4)

label = Label(frame1, text="", padx=405, bg="#353535")
label.grid(row=0, column=5)

#Text Editor area

frame2 = Frame(root)
frame2.place(x=0, y=40)

scrollY = Scrollbar(frame2, bg="#444444")
scrollY.pack(side="right", fill="y")

textBox = Text(frame2, width=120, height=34, bg ="#757575", selectforeground="#353535", selectbackground="#ff6600", undo=True, yscrollcommand=scrollY.set)
textBox.pack()

scrollY.config(command=textBox.yview)

#Key Bindings

root.bind("<Control-n>", newFile)
root.bind("<Control-o>", openFile)
root.bind("<Control-s>", saveFile)
root.bind("<Alt-s>", saveAsPDF)

root.mainloop()