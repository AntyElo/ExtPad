#!/bin/python3
from deps import *
currentpath = os.system('$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )')
imgCont = 0

from sourcelib import Source 
from wlib import CNotebook, InfoFrame
# Source and widgets merged on new files

class App():
	# Sourse
	def __init__(self):
		def grc(row, column, *args): return {"row": row, "column": column}
		self.vkw = {
			"codename": "mercurial", # Arch
			"build": 4, # Every update
			"path": 0, # Is path of version
			"type": "edge", # edge(alpha)/beta/rc(candidate)/release
		}
		self.version = f'{self.vkw["build"]}{self.vkw["type"]}{self.vkw["path"]}'# ~ 2beta1, 2release0
		self.vsm = "Version kw: "
		for k, i in self.vkw.items():
			self.vsm += f"\n    {str(k)}: {str(i)}"
		self.__doc__ = f"""New EXTantion notePAD [{self.version}]

Features:
   - Header-bar
   - Extentions (Hacks)
   - TKinter
   - Cute steel/silver - blue theme
 
TODO:
   - New ext-ons
   - New panel
 
FIXME:
   - New panel
"""
		self.source = Source()
		self.mWin = self.source.srcWin
		self.mWin.title(f"ExtPad {self.version}")
		self.mWin.geometry("400x300")
		self.istopTk = tk.BooleanVar(value=True)
		self.isCSD = tk.BooleanVar(value=True)
		self.is_floatinit = False
		self.ifloatTk()
		self.mWin["takefocus"] = True
		self.style = self.source.srcStyle
		self.nBuffer = ""
		for clri in ["bg", "tw", "gw", "sb", "dsb", "lsb"]:
			exec(f"self.clr_{clri} = self.source.clr_{clri}", locals())
		self.fform = self.source.fileforms
		self.nInfo_hints = self.source.hints
		self.imgd = tk.BooleanVar(value=True)
		self.imgst = ["save", "open", "note", "win", "min", "max", "close"]
		for imgi in self.imgst:
			exec(f"self.img_{imgi} = self.source.img_{imgi}(self.clr_gw)", locals())
		self.img_win_alt, self.imgname_win_alt = self.source.img_win(self.clr_gw, takename=1)
		self.imgst.append("win_alt")
		self.mWin.iconname(self.imgname_win_alt)
		self.mLblCheck = -1
		self.notec = 0
		self.style.map("ghost.TLabel", background = [("", self.clr_tw)])
		self.style.map("ghost.TFrame", background = [("", self.clr_tw)])
		self.style.map("ghost.TSizegrip", background = [("", self.clr_tw)])

		# Title-Bar: wmButton, mainLabel, mainLabel
		self.tBar = ttk.Frame(self.mWin)
		self.wmBtn = ttk.Button(self.tBar, style="Title.TButton", image=self.img_win)
		self.mMG = tk.Canvas(self.tBar, bg=self.clr_sb, highlightthickness=0, height=0)
		self.mMG.bind('<Button-1>', self.pointTk)
		self.mMG.bind('<B1-Motion>', self.moveTk)
		self.mMinBtn  = ttk.Button(self.tBar, style="Title.TButton", image=self.img_min,   command=self.withMin)
		self.mMaxBtn  = ttk.Button(self.tBar, style="Title.TButton", image=self.img_max,   command=self.withMax)
		self.mQuitBtn = ttk.Button(self.tBar, style="Title.TButton", image=self.img_close, command=self.withQuit)
			# Menu
				# Bind this
		self.wmBtn.bind('<Button-1>', self.popU)
				# Menus
		self.uMenu = tk.Menu(self.mWin, title="ExtPad: Menu") # Union(Wm also)
		self.fMenu = tk.Menu(self.mWin, tearoff=0) # File
		self.eMenu = tk.Menu(self.mWin, tearoff=0) # Edit
		self.vMenu = tk.Menu(self.mWin, tearoff=0) # View
		self.modMenu = tk.Menu(self.mWin, tearoff=0) # Mods
		self.hMenu = tk.Menu(self.mWin, tearoff=0) # Help

		self.uMenu.add_checkbutton(label="CSD/SSD", variable=self.isCSD, offvalue=False, onvalue=True, command=self.ifloatTk)
		self.uMenu.add_command(label="Normal window", command=self.withMin)
		self.uMenu.add_command(label="Zoom window", command=self.withMax)
		self.uMenu.add_checkbutton(label="Always at the top", variable=self.istopTk, offvalue=False, onvalue=True, command=self.topTk)
		self.uMenu.add_command(label="Quit", accelerator="Ctrl-Q", command=self.withQuit)
		self.uMenu.add_separator()
		self.uMenu.add_cascade(label="File", menu=self.fMenu)
		self.uMenu.add_cascade(label="Edit", menu=self.eMenu)
		self.uMenu.add_cascade(label="View", menu=self.vMenu)
		self.uMenu.add_cascade(label="Mods", menu=self.modMenu)
		self.uMenu.add_cascade(label="App/Help", menu=self.hMenu)

		self.fMenu.add_command(label="Save", accelerator="Ctrl-S", command=self.nSave)
		self.fMenu.add_command(label="Save as...", accelerator="Ctrl-Shift-S", command=self.nSaveas)
		self.fMenu.add_command(label="Open", accelerator="Ctrl-O", command=self.nOpen)
		self.fMenu.add_command(label="New", accelerator="Ctrl-N", command=self.nNew)
		self.fMenu.add_command(label="New note", accelerator="Ctrl-Shift-N", command=self.nNewnote)
		self.fMenu.add_command(label="Close", accelerator="Ctrl-Shift-D", command=self.nClose)

		self.eMenu.add_command(label="Copy", accelerator="Ctrl-C", command=self.eCopy)
		self.eMenu.add_command(label="Paste", accelerator="Ctrl-V", command=self.ePaste)
		self.eMenu.add_command(label="Cut", accelerator="Ctrl-X", command=self.eCut)

		self.vMenu.add_command(label="Styles (built-in mod)", command=self.mod_styles)

		self.modMenu.add_command(label="Exec", command=self.nExec)

		self.hMenu.add_command(label="About", accelerator="F1", command=self.nInfo)
			# Pack this
		self.mQuitBtn.pack(fill="both", side="right")
		self.mMaxBtn.pack(fill="both", side="right")
		self.wmBtn.pack(fill="both", side="left")
		self.mMG.pack(fill="both", expand=True)
		self.tBar.grid(**grc(0, 0), columnspan=2, sticky="nswe")

		# Help-Bar: mainSizegrip, tkhelpButton, mainLabel
		self.hBar = ttk.Frame(self.mWin)
		self.mSG = ttk.Sizegrip(self.hBar)
		self.mLbl = ttk.Label(self.hBar, text=f"Hello in ExtPad {self.version}")
			# Pack this
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.hBar.grid(**grc(2, 0), columnspan=2, sticky="nswe")

		# Hot-Bar
		self.hotBar = ttk.Frame(self.mWin)
		self.hotSave = ttk.Button(self.hotBar, image=self.img_save, command=lambda: self.nSave())
		self.hotOpen = ttk.Button(self.hotBar, image=self.img_open, command=lambda: self.nOpen())
		self.hotOpen_tip = Hovertip(self.hotOpen, "Open file")
		self.hotNN = ttk.Button(self.hotBar, image=self.img_note, command=lambda: self.nNewnote())
		self.hotNN_tip = Hovertip(self.hotNN, "New Note")
		self.hotSave.pack(fill="both", side="top", padx=2, pady=1)
		self.hotOpen.pack(fill="both", side="top", padx=2, pady=1)
		self.hotNN.pack(fill="both", side="top", padx=2, pady=1)
		self.hotBar.grid(**grc(1, 0), sticky="nswe")

		# mainNoteBook
		self.mNB = CNotebook(self.mWin, height=0)
		self.nNewnote()
		self.mNB.bind("<<NotebookTabChanged>>", self.nSel)
		self.mNB.bind("<<NotebookTabClosed>>", lambda event: self.nClose())
		self.mNB.grid(**grc(1, 1), sticky="nswe")
		self.mWin.grid_rowconfigure(1, weight=1)
		self.mWin.grid_columnconfigure(1, weight=1)

	# Funcions
		# Tk
	def mod_styles__temme(self, *a, **kw):
			if self.imgd.get(): # dark
				for imgi in self.imgst:
					exec(f"self.img_{imgi}['foreground'] = self.clr_gw", locals())
			else:
				for imgi in self.imgst:
					exec(f"self.img_{imgi}['foreground'] = self.clr_sb", locals())
	def mod_styles(self):
		def grcs(row, column, sticky, *args): return {"row": row, "column": column, "sticky": sticky}
		def newst(*a, **kw):
			#print(f"[styles] newst func. args: {a}; kw: {kw}")
			req = combox.get()
			if req.strip() == "":
				return
			self.style.theme_use(req)
			combox["values"] = sorted(self.style.theme_names(), key=str.lower)
			#combox.set(invar)
		self.mWin.bind("<<ThemeChanged>>", self.mod_styles__temme)
		top = tk.Toplevel()
		top.title("ExtPad: Themes")
		self.topTk(True, win=top)
		combox = ttk.Combobox(top, values=sorted(self.style.theme_names(), key=str.lower))
		combox.bind("<Return>", newst)
		btn = ttk.Button(top, text="[Run]", command=newst)
		cbtn = ttk.Checkbutton(top, text="light/dark icon", variable=self.imgd, offvalue=False, onvalue=True, command=self.mod_styles__temme)
		combox.grid(**grcs(0, 0, "nswe"))
		btn.grid(**grcs(0, 1, "nswe"))
		cbtn.grid(**grcs(1, 0, "nswe"), columnspan=2)
		ttk.Label(top).grid(**grcs(2, 0, "se"), columnspan=2)
		ttk.Sizegrip(top).grid(**grcs(3, 1, "se"))
		top.rowconfigure(2, weight=1)
		top.columnconfigure(0, weight=1)
		top.mainloop()
		#self.mWin.nametowidget(".!frame")["bg"] = "red"
	def forceTk(self): self.mWin.focus_force()
	def floatTk(self):
		if sysplatform == "win32": self.mWin.overrideredirect(True)
		else: self.mWin.attributes('-type', "dock")
		self.mWin.wm_state("withdraw")
		self.mWin.wm_state("normal")
	def unfloatTk(self):
		if sysplatform == "win32": self.mWin.overrideredirect(False)
		else: self.mWin.attributes('-type', "normal")
		self.mWin.wm_state("withdraw")
		self.mWin.wm_state("normal")
	def topTk(self, bl=None, **kw): 
		if bl == None: bl = self.istopTk.get()
		kw.setdefault("win", self.mWin).attributes("-topmost", bl)
	def ifloatTk(self, bl=None): 
		if bl == None: bl = self.isCSD.get()
		if sysplatform == "win32": self.mWin.overrideredirect(bl)
		else: self.mWin.attributes('-type', ["normal", "dock"][bl])
		if self.is_floatinit:
			if bl: self.tBar.grid()
			else: self.tBar.grid_remove()
		else: self.is_floatinit = True
		self.mWin.wm_state("withdraw")
		self.mWin.wm_state("normal")
	def pointTk(self, event):
		win_position = [int(coord) for coord in self.mWin.wm_geometry().split('+')[1:]]
		self.source.xTk, self.source.yTk = win_position[0] - event.x_root, win_position[1] - event.y_root
	def moveTk(self, event): 
		if self.source.Tk == "max": 
			self.withMin()
			return
		self.mWin.wm_geometry(f"+{str(event.x_root+self.source.xTk)}+{str(event.y_root+self.source.yTk)}")
	def withMin(self):
		if self.source.Tk == "normal": return
		self.mMinBtn.pack_forget()
		self.mMG.pack_forget()
		self.mLbl.pack_forget()
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.mWin.geometry(f"{self.source.ww}x{self.source.wh}+{self.source.wrx}+{self.source.wry}")
		self.mMaxBtn.pack(fill="both", side="right")
		self.mMG.pack(fill="both", expand=True)
		self.source.Tk = "normal"
	def withMax(self):
		if self.source.Tk == "max": return
		self.mMaxBtn.pack_forget()
		self.mMG.pack_forget()
		self.mSG.pack_forget()
		self.tmpx = self.mWin.cget("padx")
		self.tmpy = self.mWin.cget("pady")
		self.source.wrx = self.mWin.winfo_rootx()
		self.source.wry = self.mWin.winfo_rooty()
		self.source.ww  = self.mWin.winfo_width()
		self.source.wh  = self.mWin.winfo_height()
		self.mWin.geometry(f"{self.mWin.winfo_screenwidth()}x{self.mWin.winfo_screenheight()}+0+0")
		self.mMinBtn.pack(fill="both", side="right")
		self.mMG.pack(fill="both", expand=True)
		self.source.Tk = "max"
	def withQuit(self):
		if not tkmb.askokcancel("You sure?", "You may have unsaved changes"): return
		for i in range(len(self.mNB.tabs())): 
			if self.nClose(): return
		self.source.quit()
		# Menu
	def popU(self, event):
		self.uMenu.tk_popup(event.x_root, event.y_root, 0)
		#self.wmBtn.focus_force()
	def popEdit(self, event): self.eMenu.tk_popup(event.x_root, event.y_root, 0)
		# Notebook (aka n-prefixed)
	def get_nText(self): return self.mWin.nametowidget(self.mNB.select()+".!text")
	def get_npath(self):
		if self.mNB.select().split(":")[0].split(".")[-1] == "file":
			return self.mWin.nametowidget(self.mNB.select()+".filepath").cget("text")
		elif self.mNB.select().split(":")[0].split(".")[-1] == "note":
			return self.mWin.nametowidget(self.mNB.select()+".filepath").cget("text")
	def nSel(self, event):
		if   len(self.mNB.tabs()) == 0:
			self.mLbl["text"] = f"Hello in ExtPad {self.version}"
			self.mLblCheck = -1
		elif self.source.dbg.get() == True:
			self.mLbl["text"] = f'Selected "{str(self.mNB.select())}" tab: {self.mNB.tab(self.mNB.select())}'
			self.mLblCheck = 30
		else: self.mLblCheck = 0
	def nOpen(self, path=None):
		# Input path, text
		if path == None:
			path = tkfd.askopenfilename(
				title="Open file",
				filetypes=self.fform
			)
			self.forceTk()
			if not path: return
		nfile = open(str(path))
		text = nfile.read()
		nfile.close()
		name = ospath.split(path)[-1]
		# Controls
		nPage = ttk.Frame(self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"')
		nPath = tk.Label(nPage, text=path, name="filepath")
		nText = tk.Text(nPage, bd=0, highlightthickness=0, wrap="none", undo=True)
		nSBX = ttk.Scrollbar(nPage, command=nText.xview, orient="horizontal")
		nSBY = ttk.Scrollbar(nPage, command=nText.yview, orient="vertical")
		nText.config(xscrollcommand=nSBX.set, yscrollcommand=nSBY.set)
		nText.insert("1.0", text)
		nText.edit_reset()
		nText.edit_modified(0)
		nText.bind("<Button-3>", self.popEdit)
		# Grid controls
		nSBX.grid(column=0, row=1, sticky="nsew")
		nSBY.grid(column=1, row=0, sticky="nsew")
		nText.grid(column=0, row=0, sticky="nsew")
		nPage.rowconfigure(0, weight=1)
		nPage.columnconfigure(0, weight=1)
		self.mNB.add(nPage, text=name)
	def nSaveas(self):
		if self.mNB.tabs() == (): return
		ntype = self.mNB.select().split(":")[0].split(".")[-1]
		if ntype in ("file", "note"):
			path = tkfd.asksaveasfilename(
				title="Save as",
				defaultextension=".txt", 
				filetypes=self.fform
			)
			self.forceTk()
			if not path: return
			try:
				nText = self.get_nText()
				nText.edit_reset()
				nText.edit_modified(0)
				nfile = open(path, "w")
				nfile.write(nText.get("1.0", "end").rstrip("\n"))
				nfile.close()
			except: print("AppErorr: Can't save file")
		if ntype == "note":
			tmp = self.mNB.select()
			self.nOpen(path)
			self.mNB.forget(tmp)
	def nSave(self):
		if self.mNB.tabs() == (): return
		ntype = self.mNB.select().split(":")[0].split(".")[-1]
		if ntype == "file":
			path = self.get_npath()
			nText = self.get_nText()
			nText.edit_modified(0)
			nfile = open(path, "w")
			nfile.write(nText.get("1.0", "end").rstrip("\n"))
			nfile.close()
			self.mLblCheck = 10
			self.mLbl["text"] = "[File] All of file saved"
		elif ntype == "note": self.nSaveas()
	def nNew(self):
		path = tkfd.asksaveasfilename(
			title="New file",
			defaultextension=".txt", 
			filetypes=self.fform
		)
		self.forceTk()
		if not path: return
		name = ospath.split(path)[-1]
		# Controls
		nPage = ttk.Frame(self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"')
		nPath = tk.Label(nPage, text=path, name="filepath")
		nText = tk.Text(nPage, bd=0, highlightthickness=0, wrap="none", undo=True)
		nSBX = ttk.Scrollbar(nPage, command=nText.xview, orient="horizontal")
		nSBY = ttk.Scrollbar(nPage, command=nText.yview, orient="vertical")
		nText.config(xscrollcommand=nSBX.set, yscrollcommand=nSBY.set)
		nText.bind("<Button-3>", self.popEdit)
		# Grid controls
		nSBX.grid(column=0, row=1, sticky="nsew")
		nSBY.grid(column=1, row=0, sticky="nsew")
		nText.grid(column=0, row=0, sticky="nsew")
		ttk.Label(nPage, style="ghost.TFrame").grid(column=1, row=1, sticky="")
		nPage.rowconfigure(0, weight=1)
		nPage.columnconfigure(0, weight=1)
		self.mNB.add(nPage, text=name)
	def nNewnote(self):
		nPage = ttk.Frame(self.mNB, style="ghost.TFrame", name=f'note:{self.notec}')
		nText = tk.Text(nPage, bd=0, highlightthickness=0, wrap="none", undo=True)
		nSBX = ttk.Scrollbar(nPage, command=nText.xview, orient="horizontal")
		nSBY = ttk.Scrollbar(nPage, command=nText.yview, orient="vertical")
		nText.config(xscrollcommand=nSBX.set, yscrollcommand=nSBY.set)
		nText.bind("<Button-3>", self.popEdit)
		nSBX.grid(column=0, row=1, sticky="nsew")
		nSBY.grid(column=1, row=0, sticky="nsew")
		nText.grid(column=0, row=0, sticky="nsew")
		ttk.Label(nPage, style="ghost.TFrame").grid(column=1, row=1, sticky="")
		nPage.rowconfigure(0, weight=1)
		nPage.columnconfigure(0, weight=1)
		if self.notec: self.mNB.add(nPage, text=f"New ({self.notec})")
		else: self.mNB.add(nPage, text=f"New")
		self.notec += 1
	def nClose(self):
		if self.mNB.tabs() == (): return
		seltype = self.mNB.select().split(":")[0].split(".")[-1]
		if seltype == "file":
			nText = self.get_nText()
			if nText.edit_modified():
				tmp = self.mNB.select().split(":")[1].strip('"').replace("%2E", ".")
				save = tkmb.askyesnocancel(
					f"Save file {tmp}",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: self.nSave()
				elif save == None: return "break"
		elif seltype == "note":
			nText = self.get_nText()
			if nText.edit_modified():
				save = tkmb.askyesnocancel(
					f"Save note",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: self.nSave()
				elif save == None: return "break"
		elif seltype == "cfg":
			print("is Config!")
		else: print("fail type")
		self.mNB.forget(self.mNB.select())
	def eCopy(self): 
		try: self.nBuffer = self.get_nText().selection_get()
		except: print("AppError: Can't copy")
	def ePaste(self): 
		try: self.get_nText().insert("insert", self.nBuffer)
		except: print("AppError: Can't paste")
	def eCut(self):
		try:
			nText = self.get_nText()
			self.nBuffer = nText.selection_get()
			nText.delete(tk.SEL_FIRST, tk.SEL_LAST)
		except: print("AppError: Can't cut")
	def nInfo(self):
		iWin = tk.Toplevel(self.mWin)
		iWin.title("About ExtPad")
		iFrame = ttk.Notebook(master=iWin)
		frst = "ghost.TFrame"
		iFrame.add(InfoFrame(iFrame, style=frst, _infokw=dict(text_ph=self.vsm)), text="Version", sticky="nswe")
		iFrame.add(InfoFrame(iFrame, style=frst, _infokw=dict(text_ph=self.__doc__)), text="Description", sticky="nswe")
		iFrame.add(InfoFrame(iFrame, style=frst, _infokw=dict(text_ph=self.nInfo_hints)), text="Hints", sticky="nswe")
		iFrame.pack(fill="both", expand=True)

		# Etc
	def altstream(self):
		self.mWin.after(80, self.altstream)
		self.mLblCheck = round(self.mLblCheck)
		if self.mNB.tabs() != ():
			ntype = self.mNB.select().split(":")[0].split('.')[-1]
			nText = self.mWin.nametowidget(self.mNB.select()+".!text")
			if self.mLblCheck == 0:
				insLine, insCol = str.split(nText.index("insert"), ".")
				endLine = str(int(str.split(nText.index("end"), ".")[0]) - 1)
				endCol = str.split(nText.index(f"{insLine}.end"), ".")[1]
				if ntype == "file":
					path = self.get_npath()
					self.mLbl["text"] = f"[File] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}  Path: {path}"
				elif ntype == "note":
					self.mLbl["text"] = f"[Note] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}"
				else:
					self.mLbl["text"] = f"[Err] undifined type"
			elif self.mLblCheck > 0:
				self.mLblCheck -= 1
			if ntype == "file":
				path = self.get_npath()
				if sysplatform == "win32": tmp = path.split("\\")[-1]
				else: tmp = path.split("/")[-1]
				if nText.edit_modified() == True: self.mNB.tab(self.mNB.select(), text=tmp+"*")
				else: self.mNB.tab(self.mNB.select(), text=tmp.rstrip("*"))

	def nExec(self, path=None):
		if path == None:
			path = tkfd.askopenfilename(title="Exec file", filetypes=self.fform)
			if not path: return
		modtext = ""
		with open(path) as modfile:
			modtext = modfile.read()
		exec(modtext)

	# mainloop the mWin
	def init(self):
		self.forceTk()
		self.mWin.wm_protocol("WM_DELETE_WINDOW", self.withQuit)
		self.mWin.bind("<Button-3>", self.popU)
		self.mWin.bind("<Control-q>", lambda ev: self.withQuit())
		self.mWin.bind("<Control-o>", lambda ev: self.nOpen())
		self.mWin.bind("<Control-s>", lambda ev: self.nSave())
		self.mWin.bind("<Control-S>", lambda ev: self.nSaveas())
		self.mWin.bind("<Control-n>", lambda ev: self.nNew())
		self.mWin.bind("<Control-N>", lambda ev: self.nNewnote())
		self.mWin.bind("<Control-D>", lambda ev: self.nClose())
		self.mWin.bind("<Control-e>", lambda ev: self.nExec())
		self.mWin.bind("<F1>", lambda ev: self.nInfo())
		self.mWin.update()
		self.mWin.minsize(
			int(self.wmBtn.winfo_width() * 4.5), 
			self.tBar.winfo_height() + self.hBar.winfo_height()
		)
		# TODO: add label?
		self.mWin.after_idle(self.altstream)
		if sysplatform != "win32": self.mWin.after_idle(lambda: self.mWin.attributes('-type', "normal"))
		self.topTk(True)
		self.mWin.mainloop()


if __name__ == "__main__": 
	app = App()
	app.init()
