#!/bin/python3
""" extpad-hg x-exec
"""

def main(api):
	"""Main method"""
	if api.vkw["build"] < 2: return
	grc = api.grc
	EXP = {"sticky": "nswe"}
	def getsent(*args, **kw):
		entargs = [[], ["1.0", "end"]][is_exec_tkbv.get()]
		return [entev, entex][is_exec_tkbv.get()].get(*entargs)
	def _is_exec(*args, **kw):
		bl = is_exec_tkbv.get()
		if bl: #exec
			cmdboxex.grid()
			cmdboxev.grid_remove()
		else:
			cmdboxev.grid()
			cmdboxex.grid_remove()
		xeTop.title(f"ExtPad: {['Eval', 'Exec'][is_exec_tkbv.get()]}")
	def _ex(*args, **kw):
		src = getsent()
		if kw.setdefault("backend", True):
			bc = exec
		else: bc = eval
		try:
			e = bc(src, globals(), locals())
		except Exception as exc:
			e = f"<-Excepton: {exc}>"
		return e
	def ex(*args, **kw):
		api
		lbl.insert("end", [f"[eval] '{getsent()}': {_ex(backend=is_exec_tkbv.get())} \n", f"[exec] '''{getsent()}'''\n"][is_exec_tkbv.get()])
	import tkinter as tk
	from tkinter import ttk
	xeTop = tk.Toplevel()
	is_exec_tkbv = tk.BooleanVar(xeTop, value=False)
	xeTop.title("ExtPad: Eval")
	api.topTk(True, win=xeTop)
	cmdboxev = ttk.Frame(xeTop)
	entev = ttk.Entry(cmdboxev)
	entev.bind("<Return>", ex)
	btnev = ttk.Button(cmdboxev, text="[Run]", command=ex)
	entev.pack(expand=True, fill="both", side="left")
	btnev.pack(fill="both", side="left")
	cmdboxev.grid(**grc(0, 0), **EXP)
	
	cmdboxex = ttk.Frame(xeTop)
	entex = tk.Text(cmdboxex, height=3)
	entex.bind("<Shift-Return>", ex)
	btnex = ttk.Button(cmdboxex, text="[Run]", command=ex)
	entex.pack(expand=True, fill="both", side="left")
	btnex.pack(fill="both", side="left")
	cmdboxex.grid(**grc(1, 0), **EXP)
	cmdboxex.grid_remove()
	
	lbl = tk.Text(xeTop)
	lbl.grid(**grc(2, 0), **EXP)
	helpbar = ttk.Frame(xeTop)
	is_exec_btn = tk.Checkbutton(helpbar, text="eval/exec", variable=is_exec_tkbv, offvalue=False, onvalue=True, command=_is_exec)
	ttk.Sizegrip(helpbar).pack(side="right", fill="both")
	is_exec_btn.pack(side="left", fill="both")
	helpbar.grid(**grc(3, 0), **EXP)
	xeTop.rowconfigure(2, weight=1)
	xeTop.columnconfigure(0, weight=1)
	xeTop.mainloop()

if __name__ == "__main__":
	try:
		self
		v = self
	except NameError:
		try:
			api
			v = api
		except NameError:
			print("run ExtPad before")
			exit()
	main(v)
