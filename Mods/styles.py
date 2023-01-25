#!/bin/python3
""" extpad-tk-hg styles swither
"""

def main(api):
	def printd1(*a, **kw):
		pass #print(f"[styles] printd1 func. args: {a}; kw: {kw}")
	def newst(*a, **kw):
		#print(f"[styles] newst func. args: {a}; kw: {kw}")
		api.style.theme_use(combox.get())
		combox["values"] = sorted(api.style.theme_names(), key=str.lower)
		#combox.set(invar)
	import tkinter as tk
	from tkinter import ttk
	api.mWin.bind("<<ThemeChanged>>", printd1)
	top = tk.Toplevel()
	top.title("ExtPad: Themes")
	api.topTk(True, win=top)
	combox = ttk.Combobox(top, values=sorted(api.style.theme_names(), key=str.lower))
	combox.bind("<Return>", newst)
	btn = ttk.Button(top, text="[Run]", command=newst)
	combox.pack(expand=True, fill="both", side="left")
	btn.pack(expand=True, fill="both", side="left")
	top.mainloop()
	#api.mWin.nametowidget(".!frame")["bg"] = "red"

if __name__ == "__main__":
	main(self)
