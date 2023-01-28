#!/bin/python3
""" extpad-hg x-exec
"""

def main(api):
	"""Main method"""
	if api.vkw["build"] < 2: return
	def ex(*args, **kw):
		api
		lbl.insert("end", f"=== SoF eval\n{ent.get()}\n===\n{eval(ent.get(), globals(), locals())}\n=== Eof eval\n")
	import tkinter as tk
	from tkinter import ttk
	xeTop = tk.Toplevel()
	xeTop.title("ExtPad: Exec")
	api.topTk(True, win=xeTop)
	cmdbox = ttk.Frame(xeTop)
	ent = ttk.Entry(cmdbox)
	ent.bind("<Return>", ex)
	btn = ttk.Button(cmdbox, text="[Run]", command=ex)
	lbl = tk.Text(xeTop)
	ent.pack(expand=True, fill="both", side="left")
	btn.pack(fill="both", side="left")
	cmdbox.pack(expand=True, fill="both", side="top")
	lbl.pack(expand=True, fill="both", side="top")
	ttk.Sizegrip(xeTop).pack(fill="both", side="top")
	xeTop.mainloop()

if __name__ == "__main__":
	main(self)
