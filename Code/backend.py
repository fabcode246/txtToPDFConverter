from PIL import Image, ImageDraw, ImageFont

class pdfMaker():
	normalFont = ImageFont.truetype("micross.ttf", 40)
	head3Font = ImageFont.truetype("micross.ttf", 50)
	head2Font = ImageFont.truetype("micross.ttf", 65)
	head1Font = ImageFont.truetype("micross.ttf", 80)
	def __init__(self, text):
		self.text = text
		self.imgs = []
		self.processedImgs = []
		self.pages = []
		self.lines = []

	def txtRead(self):
		self.lines = self.text.split("\n")
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

	def hexToRGB(self, hexcode:str):
		r,g,b = hexcode[:2], hexcode[2:4], hexcode[4:]
		return (int(r, 16), int(r, 16), int(r, 16))

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
			elif "-" in line:
				draw.text(20,y), f"● {line[2:]}", font=pdfMaker.normalFont, fill=self.textColor())
				y += 45
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