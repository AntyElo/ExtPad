#!/bin/python3
""" extpad-tk-hg styles swither
"""

def main(api):
	def temme(*a, **kw):
		if api.imgd.get(): # dark
			for imgi in api.imgst:
				exec(f"api.img_{imgi}['foreground'] = api.clr_gw", locals())
		else:
			for imgi in api.imgst:
				exec(f"api.img_{imgi}['foreground'] = api.clr_sb", locals())

	def newst(*a, **kw):
		#print(f"[styles] newst func. args: {a}; kw: {kw}")
		api.style.theme_use(combox.get())
		combox["values"] = sorted(api.style.theme_names(), key=str.lower)
		#combox.set(invar)
	import tkinter as tk
	from tkinter import ttk
	def grcs(row, column, sticky, *args): return {"row": row, "column": column, "sticky": sticky}
	api.mWin.bind("<<ThemeChanged>>", temme)
	top = tk.Toplevel()
	top.title("ExtPad: Themes")
	api.topTk(True, win=top)
	combox = ttk.Combobox(top, values=sorted(api.style.theme_names(), key=str.lower))
	combox.bind("<Return>", newst)
	btn = ttk.Button(top, text="[Run]", command=newst)
	cbtn = ttk.Checkbutton(top, text="light/dark icon", variable=api.imgd, offvalue=False, onvalue=True, command=temme)
	combox.grid(**grcs(0, 0, "nswe"))
	btn.grid(**grcs(0, 1, "nswe"))
	cbtn.grid(**grcs(1, 0, "nswe"), rowspan=2)
	#top.rowconfigure(0, weight=1)
	top.columnconfigure(0, weight=1)
	top.mainloop()
	#api.mWin.nametowidget(".!frame")["bg"] = "red"

if __name__ == "__main__":
	main(self)
