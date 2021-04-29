from PIL import Image, ImageDraw, ImageFont

class pdfMaker():
	normalFont = ImageFont.truetype("micross.ttf", 40)
	head3Font = ImageFont.truetype("micross.ttf", 50)
	head2Font = ImageFont.truetype("micross.ttf", 65)
	head1Font = ImageFont.truetype("micross.ttf", 80)
	def __init__(self, txtfile):
		self.txtfile = txtfile
		self.txt = ""
		self.imgs = []
		self.processedImgs = []
		self.pages = []
		self.lines = []

	def txtRead(self):
		with open(self.txtfile, "r")as file:
			self.txt = file.read()
			file.seek(0)
			self.lines = file.readlines()
		num = 0
		for line in self.lines:
			if "//" in line:
				self.pages.append({"pos": num})
			num += 1

	def pageRead(self, page):
		start = self.pages[page]["pos"]
		end = len(self.lines)
		if page+1 in range(len(self.pages)):
			end = self.pages[page+1]["pos"]
		return self.lines[start+1:end]

	def textColor(self):
		textColor = None
		bg = self.backGround()
		newImg = Image.new(mode="RGB", size = (50,50), color=bg)
		greyscale = newImg.convert("L")
		if greyscale.getpixel((1,1)) <= 100:
			textColor = (255,255,255)
		if greyscale.getpixel((1,1)) > 100:
			textColor = (0,0,0)
		return textColor

	def hexToRGB(self, hexcode):
		rr = hexcode[0:2]
		gg = hexcode[2:4]
		bb = hexcode[4:6]
		val = [rr, gg, bb]
		RGB = [0,0,0]
		for color in range(3):
			for i in range(2):
				try:
					if i == 0:
						RGB[color] += int(val[color][i])*16
					elif i == 1:
						RGB[color] += int(val[color][i])
				except:
					num = 0
					if val[color][i] == "a":
						num = 10
					if val[color][i] == "b":
						num = 11
					if val[color][i] == "c":
						num = 12
					if val[color][i] == "d":
						num = 13
					if val[color][i] == "e":
						num = 14
					if val[color][i] == "f":
						num = 15
					if i == 0:
						RGB[color] += num*16
					elif i == 1:
						RGB[color] += num
		return tuple(RGB)

	def backGround(self):
		background = None
		for line in self.lines:
			if "% bg = " in line:
				if "#" in line:
					background = self.hexToRGB(line[line.find("#")+1:-3])
		return background

	def pageCreate(self, page):
		lines = self.pageRead(page)
		xtotal = 980
		ytotal = 1350
		y = 10
		mainPic = Image.new(mode="RGB", size=(xtotal,ytotal), color=self.backGround())
		draw = ImageDraw.Draw(mainPic)
		for line in lines:
			if "%" in line:
				pass
			elif "//" in line:
				return mainPic
			elif "###" in line:
				draw.text((10,y), line[4:], font=pdfMaker.head3Font, fill=self.textColor())
				y += 55
			elif "##" in line:
				draw.text((10,y), line[3:], font=pdfMaker.head2Font, fill=self.textColor())
				y += 70
			elif "#" in line:
				draw.text((10,y), line[2:], font=pdfMaker.head1Font, fill=self.textColor())
				y += 85
			else:
				draw.text((10,y), line, font=pdfMaker.normalFont, fill=self.textColor())
				y += 45
		return mainPic

	def converter(self, list1):
		list2 = []
		for i in list1:
			list2.append(i.convert("RGB"))
		return list2

	def makePDF(self, listy, filepath):
		listy[0].save(filepath,save_all=True, append_images=listy[1:])