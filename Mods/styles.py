#!/bin/python3
""" extpad-tk-hg styles swither
"""

def main(api):
	def printd1(*a, **kw): print(f"1===\nargs: {a}\n1===\nkw: {kw}")
	def newst(*a, **kw):
		print(f"2===\nargs: {a}\n2===\nkw: {kw}")
		api.style.theme_use(combox.cget("text"))
		combox["values"] = api.style.theme_names()
	import tkinter as tk
	from tkinter import ttk
	api.mWin.bind("<<ThemeChanged>>", lambda ev: printd1)
	top = tk.Toplevel()
	top.title="Themes"
	combox = ttk.Combobox(top, values=api.style.theme_names())
	btn = ttk.Button(top, text="++", command=newst)
	combox.pack(expand=True, fill="both", side="left")
	btn.pack(expand=True, fill="both", side="left")
	top.mainloop()
	#api.mWin.nametowidget(".!frame")["bg"] = "red"

if __name__ == "__main__":
	main(self)
