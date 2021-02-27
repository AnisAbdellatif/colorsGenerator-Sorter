import colorsys
import math
import tkinter as tk
from random import choice

WIDTH: int = 700
HEIGHT: int = 600
MAX_VALUE: int = 400


def genColors(n: int) -> list[list]:
	return [[(choice(range(256))) for _ in range(3)] for _ in range(n)]


def sortColours(colours: list[list[int]]) -> list[list[int]]:
	def step(r: int, g: int, b: int, repetitions: int = 1) -> tuple[int, float, int]:
		lum = math.sqrt(.241 * r + .691 * g + .068 * b)

		h, s, v = colorsys.rgb_to_hsv(r, g, b)

		h2 = int(h * repetitions)
		# lum2 = int(lum * repetitions)
		v2 = int(v * repetitions)

		return h2, lum, v2

	colours.sort(key=lambda col: step(*col, 8))
	return colours


class Bar(tk.Frame):
	def __init__(self, master, bg, wd: float) -> None:
		self.master = master

		super().__init__(self.master, bg=bg, width=wd, height=550)
		self.pack(side=tk.LEFT)


class BarSetting(tk.Scale):
	def __init__(self, master) -> None:
		self.master = master
		super().__init__(self.master,
						 from_=10, to=MAX_VALUE,
						 orient=tk.HORIZONTAL,
						 command=self.getValue,
						 resolution=10,
						 sliderlength=25,
						 length=200)
		self.set(100)
		self.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

	# self.setting.trace_add('write', self.getValue)

	def getValue(self, *args) -> None:
		# if not newN.isdigit(): return
		newN = int(self.get())
		if newN <= 0:
			return
		elif newN >= MAX_VALUE:
			self.set(str(MAX_VALUE))
			newN = MAX_VALUE
		# oldN = self.nametowidget('.').n
		# print(oldN)
		# print(newN)
		self.nametowidget('.').n = newN


class TopMenu(tk.Frame):
	def __init__(self, master, *args, **kwargs) -> None:
		self.master = master
		super().__init__(self.master, *args, **kwargs, width=WIDTH, height='50')
		self.pack()
		self.pack_propagate(0)

		self.btnText = tk.StringVar(value="Sort")

		self.btnSort = tk.Button(self, textvariable=self.btnText, width=round(WIDTH / 40), command=self.btnClick)
		self.btnSort.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

		BarSetting(self)

	def btnClick(self) -> None:
		if self.master.random:
			self.master.sort()
			self.btnText.set("Gen")
		else:
			self.master.genColors()
			self.btnText.set("Sort")


class MainActivity(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("Color Generator")
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.resizable(0, 0)
		try:
			self.iconphoto(True, tk.PhotoImage(file="icon.png"))
		except tk.TclError:
			print("Check your icon!")
			exit(1)
		self.setup()

	def setup(self) -> None:
		self.n: int = 100
		self.random: bool = True

		self.shownWD = self.n

		TopMenu(self)

		self.genColors()
		self.drawBars()

		self.mainloop()

	def genColors(self, draw: bool = True) -> None:
		self.colours = genColors(self.n)
		self.shownWD = self.n
		if draw:
			self.drawBars()
		self.random = True

	def drawBars(self) -> None:
		try:
			self.frameBars is None
		except AttributeError:
			self.frameBars = tk.Frame(self)
			self.frameBars.pack()

		self.frameBars.pack_propagate(1)

		for child in self.frameBars.winfo_children():
			child.destroy()

		for colour in self.colours:
			hexColor = "#{0:02x}{1:02x}{2:02x}".format(*colour)
			Bar(self.frameBars, hexColor, wd=(WIDTH / self.shownWD))

	# self.frameBars.pack_propagate(0)

	def sort(self) -> None:
		if not self.random:
			return
		self.colours = sortColours(self.colours)
		self.drawBars()
		self.random = False


MainActivity()
