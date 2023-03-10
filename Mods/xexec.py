#!/bin/python3
" extpad-hg x-exec "

def main(api):
	if api.vkw["build"] < 7: return # Req version <ver> or high
	grc = api.grc
	EXP = {"sticky": "nswe"}
	def getsent(*args, **kw):
		entargs = [[], ["1.0", "end"]][is_exec_tkbv.get()]
		return [entev, entex][is_exec_tkbv.get()].get(*entargs)
	def _is_exec(*args, **kw):
		bl = is_exec_tkbv.get()
		if bl: cmdboxex.grid(); cmdboxev.grid_remove()
		else:  cmdboxev.grid(); cmdboxex.grid_remove()
	def _ex(*args, **kw):
		api
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
		api.config_frames["ext.xexec"].text.insert("end", [f"[eval] '{getsent()}': {_ex(backend=is_exec_tkbv.get())} \n", f"[exec] '''{getsent()}'''\n"][is_exec_tkbv.get()])
	import tkinter as tk
	from tkinter import ttk
	api
	api.config_frames["ext.xexec"] = api.IFrame(dict(fid=["conf", "exec"]), master=api.mNB)
	is_exec_tkbv = tk.BooleanVar(api.config_frames["ext.xexec"], value=False)
	cmdboxev = ttk.Frame(api.config_frames["ext.xexec"])
	entev = ttk.Entry(cmdboxev, width=2)
	entev.bind("<Return>", ex)
	btnev = ttk.Button(cmdboxev, text="[Run]", command=ex)
	entev.pack(expand=True, fill="both", side="left")
	btnev.pack(fill="both", side="left")
	cmdboxev.grid(**grc(0, 0), **EXP)
	
	cmdboxex = ttk.Frame(api.config_frames["ext.xexec"])
	entex = tk.Text(cmdboxex, width=2, height=3)
	entex.bind("<Shift-Return>", ex)
	btnex = ttk.Button(cmdboxex, text="[Run]", command=ex)
	entex.pack(expand=True, fill="both", side="left")
	btnex.pack(fill="both", side="left")
	cmdboxex.grid(**grc(1, 0), **EXP)
	cmdboxex.grid_remove()
	
	api.config_frames["ext.xexec"].text = tk.Text(api.config_frames["ext.xexec"])
	api.config_frames["ext.xexec"].text.grid(**grc(2, 0), **EXP)
	helpbar = ttk.Frame(api.config_frames["ext.xexec"])
	is_exec_btn = tk.Checkbutton(helpbar, text="eval/exec", variable=is_exec_tkbv, offvalue=False, onvalue=True, command=_is_exec)
	is_exec_btn.pack(side="left", fill="both")
	helpbar.grid(**grc(3, 0), **EXP)
	api.config_frames["ext.xexec"].rowconfigure(2, weight=1)
	api.config_frames["ext.xexec"].columnconfigure(0, weight=1)
	api.mNB_addc(api.config_frames["ext.xexec"], text="Exec")

if __name__ == "__main__":
	try:
		api
		v = api
	except NameError:
		print("run ExtPad >=7 before")
		exit()
	main(v)
