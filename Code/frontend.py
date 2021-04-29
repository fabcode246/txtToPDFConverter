from tkinter import filedialog, Frame, Label, Button, Tk
from backend import pdfMaker

root = Tk()
root.title("PyDF")
root.maxsize(240, 196)

txtfile = None

frame = Frame(root, width=560, height=700, bg="#757575")
frame.pack()

def txtFile():
	global txtfile
	txtfile = filedialog.askopenfilename()

def savePDF():
	pdf = pdfMaker(txtfile)
	pdf.txtRead()
	pagelist = []
	for i in range(len(pdf.pages)):
		pagelist.append(pdf.pageCreate(i))
	pagelist = pdf.converter(pagelist)
	savepath = filedialog.asksaveasfilename(defaultextension='.pdf')	
	pdf.makePDF(pagelist, savepath)

label = Label(frame, text="", pady=10, padx=120, bg="#757575")
label.pack()

txt_file_button = Button(frame, text="Select .txt file", command=txtFile, bg="#353535", pady=10)
txt_file_button.pack()

label = Label(frame, text=" ", pady=6, bg="#757575")
label.pack()

save_file_button = Button(frame, text="Save file as PDF", command=savePDF, bg="#353535", pady=10)
save_file_button.pack()

label = Label(frame, text=" ", pady=10, bg="#757575")
label.pack()

root.mainloop()