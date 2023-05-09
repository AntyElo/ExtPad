#!/bin/python3
""" Part of extpad - Widgets"""
from deps import *

class CNotebook(ttk.Notebook): # With "CustomNotebook" and TNotebook
	__initialized = False
	def __init__(self, *args, **kwargs):
		self.img_close_raw = \
"""#define tmp1_width 16
#define tmp1_height 16
static unsigned char tmp1_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x08, 0x38, 0x1c, 0x70, 0x0e,
   0xe0, 0x06, 0xc0, 0x01, 0x80, 0x03, 0x60, 0x07, 0x70, 0x0e, 0x38, 0x1c,
   0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };"""
		self.img_file_raw = \
"""#define open16_width 16
#define open16_height 16
static unsigned char open16_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x0f, 0x04, 0x1c, 0x04, 0x3c, 0xf4, 0x3c,
   0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };"""
		self.img_close = tk.Image("bitmap", "img_close", data = self.img_close_raw, foreground = "steelblue")
		self.img_close_act = tk.Image("bitmap", "img_close_act", data=self.img_close_raw, foreground="lightsteelblue")
		self.img_close_pr = tk.Image("bitmap", "img_close_pr", data=self.img_close_raw, foreground="darkslateblue")

		self.style = kwargs.setdefault("cstyle")
		if not self.style: self.style=ttk.Style()
		kwargs.pop("cstyle")
		self.clr_bg = "#b7b7b7"
		self.clr_tw = "#ffffff"
		if not self.__initialized:
			self.__initialize_custom_style()
			self.__inititialized = True

		kwargs["style"] = "CNotebook"
		ttk.Notebook.__init__(self, *args, **kwargs)

		self._active = None

		self.bind("<ButtonPress-1>", self.on_close_press, True)
		self.bind("<ButtonRelease-1>", self.on_close_release)
		self.bind("<<ThemeChanged>>", lambda ev: self.__initialize_custom_style())

	def on_close_press(self, event):
		element = self.identify(event.x, event.y)

		if "close" in element:
			index = self.index("@%d,%d" % (event.x, event.y))
			self.state(['pressed'])
			self._active = index
			return "break"

	def on_close_release(self, event):
		if not self.instate(['pressed']):
			return

		element =  self.identify(event.x, event.y)
		if "close" not in element:
			# user moved the mouse off of the close button
			return

		index = self.index("@%d,%d" % (event.x, event.y))

		if self._active == index:
			self.event_generate("<<NotebookTabClosed>>", x=index)

		self.state(["!pressed"])
		self._active = None

	def __initialize_custom_style(self):
		self.style.theme_settings(self.style.theme_use(), {
			   "CNotebook": {
				"layout": [
					("CNotebook.client", {"sticky": "nswe"})
				]
			}, "CNotebook.Tab": {
				"layout": [
					("CNotebook.tab", {"sticky": "nswe", "children": [
						("CNotebook.focus", {"side": "top", "sticky": "nswe", "children": [
							("CNotebook.padding", {"side": "top", "sticky": "nswe", "children": [
									("CNotebook.label", {"side": "left", "sticky": ''}),
									("CNotebook.close", {"side": "left", "sticky": ''}),
							]})
						]})
					]})
				]
			}
		})
		if "close" in self.style.element_names(): return
		self.style.element_create(
			"close", "image", "img_close",
			("active", "pressed", "!disabled", "img_close_pr"),
			("active", "!disabled", "img_close_act"), 
			border=8, sticky=""
		)

class TextLN(tk.Canvas):
	def __init__(self, *args, **kwargs):
		tk.Canvas.__init__(self, *args, **kwargs)
		self.page = None
		self.top = None
		self.breakpoints = [-1]
		self.bind("<Button-1>", self.bpa)
		self.bind("<Button-3>", lambda ev: self.menu.tk_popup(ev.x_root, ev.y_root))

	def _textindex(self, seq, i=0):
		if not self.page: return
		return int(self.page.text.index(seq).split(".")[i])

	def bpc(self):
		if not self.page: return
		self.breakpoints = [i for i in self.breakpoints if 0 < i <= self._textindex("end-1c")]

	def bpa(self, ev):
		if not self.page: return
		elm = int(self.itemcget(self.find_closest(ev.x, ev.y), 'text')[:-1])
		if elm in self.breakpoints:
			self.breakpoints.remove(elm)
		else: self.breakpoints.append(elm)
		self.redraw()

	def on_return(self, ev):
		if not self.page: return
		self.bpc()
		self.breakpoints = [[elm, elm+1][elm > self._textindex("insert-1c")] for elm in self.breakpoints]
		self.redraw()

	def on_bs(self, ev):
		if not self.page: return
		self.bpc()
		self.page.text.see("insert-1c")
		if self.page.text.get("insert-1c") == "\n":
			self.breakpoints = [[elm, elm-1][elm > self._textindex("insert-1c")] for elm in self.breakpoints]
		self.redraw()

	def _as_min(self, i, m):
		return [m, i][i > m]

	def attach(self, page):
		self.page = page
		self.page.text.bind("<Return>", self.on_return)
		self.page.text.bind("<BackSpace>", self.on_bs)

	def redraw(self, *args):
		'''redraw line numbers'''
		self.delete("all")
		if not self.page.text: return
		i = self.page.text.index("@0,0")
		clr = self.page.ikw.get("clr_ln")
		if clr: self.__setitem__("bg", clr)
		w = int(self.cget("width"))-3
		f = self.page.text["font"]
		mi = len(self.page.text.index("end-1c").split(".")[0]+" ")
		while True:
			dline = self.page.text.dlineinfo(i)
			if dline is None: break
			t = str(i).split(".")[0]
			t2 = t+[" ", "+"][int(t) in self.breakpoints]
			self.create_text(w, dline[1], anchor="ne", font=f, text=t2)
			i = self.page.text.index(f"{i}+1line")
		self.__setitem__("width", self._as_min(mi, 3)*10)

class CText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)

		# create a proxy for the underlying widget
		self._orig = self._w + "_orig"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._proxy)

	def _proxy(self, *args):
		# let the actual widget perform the requested action
		cmd = (self._orig,) + args
		try: result = self.tk.call(cmd) # Undo/Redo fail
		except tk.TclError as err: print(f"[wlib.CText] Fail: {err}"); return

		# generate an event if something was added or deleted,
		# or the cursor position changed
		if (args[0] in ("insert", "replace", "delete") or 
			args[0:2] in [("xview", "moveto"), ("xview", "scroll"),
			("yview", "moveto"), ("yview", "scroll")] or
			args[0:3] == ("mark", "set", "insert")):
			self.event_generate("<<CTChange>>", when="tail")

		# return what the actual widget returned
		return result

class InfoFrame(ttk.Frame): # Frame to info`rmation
	def __init__(self, ikw, *args, **kwargs):
		self.style = ttk.Style()
		self.ikw = ikw
		super().__init__(*args, **kwargs)

		self.text = tk.Text(master=self)
		self.text.insert("end", self.ikw.get("text_ph"))
		self.SCY = ttk.Scrollbar(master=self, orient="vertical", command=self.text.yview)
		self.SCX = ttk.Scrollbar(master=self, orient="horizontal", command=self.text.xview)
		self.text.config(yscrollcommand=self.SCY.set, xscrollcommand=self.SCX.set)
		self.SCY.grid(sticky="nswe", column=1)
		self.SCX.grid(sticky="nswe", row=1)
		self.text.grid(sticky="nswe", row=0)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

class EntryToolFrame(ttk.Frame):
	def __init__(self, master, text: str, catchf, tabf, *args, **kwargs):
		self.style = ttk.Style()
		kwargs["style"] = "Tool.TFrame"
		self.tabf = tabf
		super().__init__(master, *args, **kwargs)
		self.catchf = catchf
		self.text = ttk.Entry(self, width=5)
		self.lbl = ttk.Label(self, text=text)
		self.text.bind("<Return>", lambda ev: self.catchfx())
		self.lbl.bind("<Button-1>", lambda ev: self.catchfx())
		self.lbl.grid(row=0, column=0, padx=2, pady=2)
		self.text.grid(row=0, column=1, padx=2, pady=2)
	def catchfx(self):
		self.catchf(self.text.get())
		tab = self.tabf()
		if tab: tab.text.focus_force()

class ColorToolFrame(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		self.style = ttk.Style()
		kwargs["style"] = "Tool.TFrame"
		super().__init__(master, *args, **kwargs)
		self.text = ttk.Entry(self, width=5)
		self.lbl = ttk.Label(self, text="color:")
		self.text.bind("<Return>", lambda ev: self.colored())
		self.lbl.bind("<Button-1>", lambda ev: self.colored())
		self.lbl.grid(row=0, column=0, padx=2, pady=2)
		self.text.grid(row=0, column=1, padx=2, pady=2)
	def colored(self):
		try: end = str(tkcc.askcolor(self.text.get())[1])
		except tk.TclError: end = str(tkcc.askcolor()[1])
		self.text.delete(0, "end")
		self.text.insert(0,  end )

class IFrame(ttk.Frame):
	def __init__(self, ikw, *args, **kwargs):
		self.style = ttk.Style()
		self.ikw = ikw
		self.id = self.ikw.setdefault("fid", ["note", -1])
		self.name = self.ikw.get("name", self.id[0].title())
		super().__init__(*args, **kwargs)
		self.text = None
		self.api_on_tbar = lambda: f"{self.name}: {', '.join(self.id[1:])}"
		self.api_on_hbar = lambda: f"[{self.name}] hbar placeholder"

class NBFrame(ttk.Frame): # nFrame back-end
	def __init__(self, ikw, *args, **kwargs):
		self.style = ttk.Style()
		self.ikw = ikw
		self.ikw.setdefault("clr_ln", "gray95")
		self.id = self.ikw.setdefault("fid", ["note", -1])
		super().__init__(*args, **kwargs)

		self.text_frame = self
		self.text = CText(self, undo=True)
		self.SBX = ttk.Scrollbar(self, command=self.text.xview, orient="horizontal")
		self.SBY = ttk.Scrollbar(self, command=self.text.yview, orient="vertical")
		self.text.config(xscrollcommand=self.SBX.set, yscrollcommand=self.SBY.set)
		self.text.insert("1.0", self.ikw.setdefault("text", ""))
		self.text.edit_reset()
		self.text.edit_modified(0)
		self.lnw = TextLN(self, width=30, highlightthickness=0)
		self.lnw.attach(self)
		b3bind = self.ikw.setdefault('b3bind')
		if b3bind: self.text.bind("<Button-3>", b3bind)
		self.text.bind("<<CTChange>>", lambda ev: self.lnw.redraw())
		self.text.bind("<Configure>", lambda ev: self.lnw.redraw())
		# Grid controls
		self.lnw.grid(column=0, row=0, rowspan=2, sticky="nsew")
		self.SBX.grid(column=1, row=1, sticky="nsew")
		self.SBY.grid(column=2, row=0, sticky="nsew")
		self.text.grid(column=1, row=0, sticky="nsew")
		self.rowconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

class NBFrame_Note(NBFrame):
	def __init__(self, api, *args, **kwargs):
		ikw = kwargs.setdefault("ikw", {}); kwargs.pop("ikw")
		self.api = api
		self.noted()
		nclose = self.api_nclose
		super().__init__(ikw, *args, **kwargs)
		if self.ikw.get("tid") == None:
			self.ikw["tid"] = api.text_shared.addw(self.text)
	def filed(self):
		self.api_nsave = self.api_nsave_file
		self.api_nsaveas = self.api_nsaveas_file
	def noted(self):
		self.api_nsave = self.api_nsave_note
		self.api_nsaveas = self.api_nsaveas_note
	def api_on_tbar(self):
		return f"0{self.id[1]}" if self.id[0] == "file" else f"New{f' ({self.id[1]})' if self.id[1] else ''}"
	def api_on_hbar(self):
		il, ic = self.text.index("insert").split('.')
		cl, cc = self.text.index("current").split('.')
		el = self.text.index("end-1c").split(".")[0]
		ec = self.text.index(f"{il}.end").split(".")[1]
		return f"[{self.id[0].title()}]  Cur: {cl}.{cc}  Ins: {il}.{ic}  End: {el}.{ec}  {'Path' if self.id[0] == 'file' else 'Note'}: {self.id[1]}"
	def api_nclose(self, tabid):
		if self.text.edit_modified():
			tmp = ["", f" {self.id[1]}"][bool(self.id[1])]
			save = tkmb.askyesnocancel(
				f"Save f{self.id[0]}{tmp}",
				"You have unsaved changes.\nDo you want to save before closing?",
			)
			if save: fail = self.api_nsave()
			elif save == None: return "break"
		self.api.text_shared.rmw(self.ikw.get("tid"))
		self.api.mNB.forget(tabid)
	def api_nsave_file(self):
		self.text.edit_modified(0)
		nfile = open(self.id[1], "w")
		nfile.write(self.text.get("1.0", "end").rstrip("\n"))
		nfile.close()
		self.api.mLblCheck = 10
		self.api.mLbl["text"] = "[File] File saved"
	def api_nsaveas_file(self):
		path = tkfd.asksaveasfilename(
			title="Save as",
			defaultextension=".txt", 
			filetypes=self.api.fform
		)
		self.api.wTk_force()
		if not path: return path, "cancel:nopath"
		try:
			self.text.edit_reset()
			self.text.edit_modified(0)
			nfile = open(path, "w")
			nfile.write(self.text.get("1.0", "end").rstrip("\n"))
			nfile.close()
		except: print("[NBFrame_Note] Can't save file"); return path, "cancel:nofile"
		return path, None
	def api_nsave_note(self):
		self.api_nsaveas_note()
	def api_nsaveas_note(self):
		path, exc = self.api_nsaveas_file()
		if exc: return
		self.id = ["file", path]
		self.api.mNB.add(self, image=self.api.img_mbfile, text=self.id[1], compound="left")
		self.filed()

class EntryField(ttk.Frame): # nFrame back-end
	def __init__(self, ikw, *args, **kwargs):
		self.style = ttk.Style()
		self.ikw = ikw
		ebind = self.ikw.setdefault('ebind')
		super().__init__(*args, **kwargs)

		self.text = ttk.Entry(self)
		self.text.insert(1, self.ikw.setdefault('efill', ""))
		self.btn = ttk.Button(self, text=self.ikw.setdefault('bfill', "[Run]"))
		if ebind:
			self.text.bind("<Return>", lambda ev: ebind())
			self.btn["command"] = ebind
		self.text.grid(row=0, column=0, sticky="nsew")
		self.btn.grid(row=0, column=1, sticky="nsew")
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

class SharedConf(object):
	def __init__(self, **cfg):
		self.cfg = cfg
		self.ws = {}
		self.c = 0
	def __getitem__(self, key): return self.cfg[key]
	def __setitem__(self, key, new):
		self.cfg[key] = new
		self.update()
	def setdefault(self, key, default=None):
		return self.cfg.setdefault(key, default)
	def update(self):
		for e in self.ws.values():
			e.configure(**self.cfg)
	def addw(self, w):
		self.c += 1
		self.ws[self.c] = w
		self.update()
		return self.c
	def rmw(self, i):
		return self.ws.pop(i, None)

if __name__ == "__main__":
	win = tk.Tk()
	nb=CNotebook(win)
	nb.pack(expand=1, fill="both")
	fr = NBFrame(dict(text="Hello! I'm widgetlib test! \nPlease test me"), nb)
	nb.add(fr, text="Frame1")
	win.mainloop()
