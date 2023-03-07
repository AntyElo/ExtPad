#!/bin/python3 -B
from deps import *
currentpath = os.system('$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )')
imgCont = 0

from sourcelib import Source 
from widgetlib import *
# Source and widgets merged on new files

class App():
	# Sourse
	def grc(main, row, column, *args): return {"row": row, "column": column}
	def __init__(self):
		grc = self.grc
		self.vkw = {
			"codename": "crypton", # Arch
			"build": 7, # Every update
			"path": 0, # Is path of version
			"channel": "b (beta)", # e(edge/alpha)/b(beta)/c(rc/release-candidate)/r(release)
		}
		verpath = self.vkw.setdefault("path")
		if not verpath: verpath = ""
		self.vsm = "Version kw: " + "".join((f"\n    {str(k)}: {str(w)}" for k, w in self.vkw.items()))
		self.version = f'{self.vkw["build"]}{self.vkw["channel"][0:1]}{verpath}'
		# ~~
		# 1e -> [2e]                 [1e]--> 2e
		#    \--> 1b -> 1c0 -> 1c1 -> 1r -/
		self.__doc__ = f"""New EXTernal notePAD [{self.version}]

Features:
   - Header-bar (csd/ssd support)
   - Hot-bar
   - Extentions (Hacks?)
   - TKinter (ttk)
   - Cute steelblue themes (deft & deftc)
 
TODO:
   - New ext-ons
 
FIXME:
   - Nuitka3
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
		self.nInfo_hints = \
"""WM: <C/S>SD = <Client/Server>-Side Decorartion
Use <Alt-B1> to move window
Use <Button-2> to call uMenu
Use <Control-Button-1> to find selecton in text"""
		self.imgd = tk.BooleanVar(value=True)
		self.imgst = ["save", "open", "note", "win", "min", "max", "close"]
		#TODO: make (?) self.imgpool[imgi] = self.source.imgspool[imgi](self.color)
		for imgi in self.imgst:
			exec(f"self.img_{imgi} = self.source.img_{imgi}(self.clr_gw)", locals())
		self.img_mbnote, self.img_mbfile = self.source.img_note(self.clr_sb), self.source.img_open(self.clr_sb)
		self.img_win_alt, self.imgname_win_alt = self.source.img_win(self.clr_gw, takename=1)
		self.imgst.append("win_alt")
		self.mWin.iconname(self.imgname_win_alt)
		self.config_frames = {}
		#FIXME: csd+ssd title src
		self.title_str = "[Miniformulas++ -> ExtPad-tk def[ept] -> ExtPad-Qt -> ExtPad-Qt-git; [ept] -> ExtPad-tk-hg]"
		self.title_trg = None
		self.mLblCheck = -1
		self.notec = 0
		self.eFind_str = tk.StringVar()
		self.theme_path_gw()

		# Title-Bar: wmButton, mainLabel, mainLabel
		self.tBar = tk.Frame(self.mWin, bg=self.clr_sb, highlightthickness=0, height=0)
		self.wmBtn = ttk.Button(self.tBar, style="Title.TButton", image=self.img_win)
		self.mMG = tk.Canvas(self.tBar, bg=self.clr_sb, highlightthickness=0, height=0)
		self.mMG.bind('<Button-1>', self.pointTk)
		self.mMG.bind('<B1-Motion>', self.moveTk)
		self.mWin.bind("<Alt-Button-1>", self.pointTk)
		self.mWin.bind("<Alt-B1-Motion>", self.moveTk)
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
		self.eMenu.add_command(label="Find", accelerator="Ctrl-B1", command=self.eFind)

		self.vMenu.add_command(label="Styles (built-in mod)", accelerator="F2", command=self.mod_styles)

		self.modMenu.add_command(label="Exec", accelerator="Ctrl-E", command=self.nExec)

		self.hMenu.add_command(label="About", accelerator="F1", command=self.nInfo)
			# Pack this
		self.mQuitBtn.pack(fill="both", side="right")
		self.mMaxBtn.pack(fill="both", side="right")
		self.wmBtn.pack(fill="both", side="left")
		self.mMG.pack(fill="both", expand=True)
		self.tBar.grid(**grc(0, 0), columnspan=2, sticky="nswe")

		# Help-Bar: mainSizegrip, tkhelpButton, mainLabel
		self.api_pane = ttk.Frame(self.mWin)
		self.hBar = ttk.Frame(self.mWin)
		self.mSG = ttk.Sizegrip(self.hBar)
		self.mLbl = ttk.Label(self.hBar, text=f"Hello in ExtPad {self.version}")
			# Pack this
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.api_pane.grid(**grc(2, 0), columnspan=2, sticky="nswe")
		self.hBar.grid(**grc(3, 0), columnspan=2, sticky="nswe")

		# Hot-Bar
		self.hotBar = ttk.Frame(self.mWin, style="Hotbar.TFrame")
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
		self.mNB.bind("<<NotebookTabClosed>>", self.iCloseEv)
		self.mNB.grid(**grc(1, 1), sticky="nswe")
		self.mWin.grid_rowconfigure(1, weight=1)
		self.mWin.grid_columnconfigure(1, weight=1)

		## The cfg-panes
		# cfg:info
		self.config_frames["root.info"] = IFrame(dict(fid=["conf", "info"]), master=self.mNB, name='conf:"info"')
		self.infoNB = ttk.Notebook(master=self.config_frames["root.info"])
		self.infoNB.add(InfoFrame(dict(text_ph=self.vsm), self.infoNB, style="ghost.TFrame"), text="Version", sticky="nswe")
		self.infoNB.add(InfoFrame(dict(text_ph=self.__doc__), self.infoNB, style="ghost.TFrame"), text="Description", sticky="nswe")
		self.infoNB.add(InfoFrame(dict(text_ph=self.nInfo_hints), self.infoNB, style="ghost.TFrame"), text="Hints", sticky="nswe")
		self.infoNB.pack(expand=1, fill="both")

		# cfg:theme
		self.config_frames["root.theme"] = IFrame(dict(fid=["conf", "theme"]), master=self.mNB, name='conf:"theme"')
		self.iTheme_combox = ttk.Combobox(self.config_frames["root.theme"], value=sorted(self.style.theme_names(), key=str.lower))
		self.iTheme_combox.set(self.style.theme_use())
		self.iTheme_combox.bind("<Return>", self.mod_styles__newst)
		self.iTheme_btn = ttk.Button(self.config_frames["root.theme"], text="[Run]", command=self.mod_styles__newst)
		self.iTheme_optbox = ttk.Frame(self.config_frames["root.theme"])
		self.iTheme_cbtn = ttk.Checkbutton(
			self.iTheme_optbox, text="light/dark icon", 
			variable=self.imgd, offvalue=False, onvalue=True, 
			command=self.themeChanged
		)
		self.iTheme_cbtn.pack(side="top", fill="x")
		self.iTheme_combox.grid(**self.grc(0, 0), sticky="nswe")
		self.iTheme_btn.grid(**self.grc(0, 1), sticky="nswe")
		self.iTheme_optbox.grid(**self.grc(1, 0), sticky="nswe", columnspan=2)
		ttk.Label(self.config_frames["root.theme"]).grid(**self.grc(2, 0), sticky="nswe", columnspan=2)
		self.config_frames["root.theme"].rowconfigure(2, weight=1)
		self.config_frames["root.theme"].columnconfigure(0, weight=1)
		self.mWin.bind("<<ThemeChanged>>", self.themeChanged)

	# Funcions
		# Tk
	def themeChanged(self, *a, **kw):
		for imgi in self.imgst:
			color = ['self.clr_sb', 'self.clr_gw'][self.imgd.get()]
			exec(f"self.img_{imgi}['foreground'] = {color}", locals())
		self.theme_path_gw()
	def mod_styles__newst(self, *a, **kw):
		#print(f"[styles] newst func. args: {a}; kw: {kw}")
		req = self.iTheme_combox.get()
		if req.strip() == "":
			return
		self.style.theme_use(req)
		self.iTheme_combox["value"] = sorted(self.style.theme_names(), key=str.lower)
		#combox.set(invar)
	def mod_styles(self): self.mNB.add(self.config_frames["root.theme"], text=f"Themes")
	def nInfo(self): self.mNB.add(self.config_frames["root.info"], text=f"Info")
	def theme_path_gw(self):
		self.style.map("ghost.TLabel", background = [("", self.clr_tw)])
		self.style.map("ghost.TFrame", background = [("", self.clr_tw)])
		self.style.map("ghost.TSizegrip", background = [("", self.clr_tw)])
	def forceTk(self): self.mWin.focus_force()
	def topTk(self, bl=None, **kw): 
		if bl == None: bl = self.istopTk.get()
		kw.setdefault("win", self.mWin).attributes("-topmost", bl)
	def csd_title(self, s):
		print(f"[app][csd_title] New title: {s}")
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
		if self.mNB.tabs() != () and self.source.future_fast_quit:
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
	def get_pfid(self, i): return self.mWin.nametowidget(self.mNB.select()).id[i]
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
		with open(str(path)) as nfile: text = nfile.read()
		# Controls
		nPage = NBFrame(
			dict(b3bind=self.popEdit, fid=["file", path], text=text),
			self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"'
		)
		self.mNB.add(nPage, image=self.img_mbfile, text=ospath.split(path)[-1], compound="left")
	def nSaveas(self):
		if self.mNB.tabs() == (): return "cancel:notabs"
		ntype = self.get_pfid(0)
		if ntype in ("file", "note"):
			path = tkfd.asksaveasfilename(
				title="Save as",
				defaultextension=".txt", 
				filetypes=self.fform
			)
			self.forceTk()
			if not path: return "cancel:nopath"
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
		ntype = self.get_pfid(0)
		if ntype == "file":
			path = self.get_pfid(1)
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
		# Controls
		nPage = NBFrame(
			dict(b3bind=self.popEdit, fid=["file", path]),
			self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"'
		)
		self.mNB.add(nPage, image=self.img_mbfile, text=ospath.split(path)[-1], compound="left")
	def nNewnote(self):
		nPage = NBFrame(
			dict(b3bind=self.popEdit, fid=["note", self.notec]), 
			self.mNB, style="ghost.TFrame", name=f'note:"{self.notec}"'
		)
		self.mNB.add(nPage, image=self.img_mbnote, text=f"New{['', f' ({self.notec})'][bool(self.notec)]}", compound="left")
		self.notec += 1
	def nClose(self):
		if self.mNB.tabs() == (): return
		seltype = self.get_pfid(0)
		fail = None
		if seltype == "file":
			nText = self.get_nText()
			if nText.edit_modified():
				tmp = self.mNB.select().split(":")[1].strip('"').replace("%2E", ".")
				save = tkmb.askyesnocancel(
					f"Save file {tmp}",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: fail = self.nSave()
				elif save == None: return "break"
		elif seltype == "note":
			nText = self.get_nText()
			if nText.edit_modified():
				save = tkmb.askyesnocancel(
					f"Save note",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: fail = self.nSave()
				elif save == None: return "break"
		elif seltype == "conf":
			print(f"[nClose] Closing config: {self.get_pfid(1)}")
		else: print("[nClose] Unknown type (fail)")
		if not fail: self.mNB.forget(self.mNB.select())
	def iCloseEv(self, ev, *args, **kw):
		#tab1 - write-select; tab2 - cursor-select
		tab1 = self.mNB.index(self.mNB.select())
		tab2 = ev.x
		self.mNB.select(tab2)
		self.nClose()
		if tab1 != tab2:
			if tab1 > tab2: tab1 -= 1
			self.mNB.select(tab1)
	def eCopy(self): 
		try: 
			nText = self.get_nText()
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
		except Exception as exc: print(f"AppError: Can't copy: {exc}")
	def ePaste(self): 
		try: 
			nText = self.get_nText()
			s = nText.clipboard_get()
			self.get_nText().insert("insert", s)
		except Exception as exc: print(f"AppError: Can't paste: {exc}")
	def eCut(self):
		try:
			nText = self.get_nText()
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
			nText.delete(tk.SEL_FIRST, tk.SEL_LAST)
		except Exception as exc: print(f"AppError: Can't cut: {exc}")
	def eFind_engene(self, s, w):
		fill = "".join([" ", "Z"][i == " "] for i in w)
		if w == "" or s == "": return
		ss = s.split("\n")
		rs = []
		for i, e in enumerate(ss):
			while 1:
				f = e.find(w)
				if f < 0: break
				e = e[0:f]+fill+e[f+len(w):]
				rs.append([i+1, f])
		return rs
	def eFind(self):
		nText = self.get_nText()
		nText.tag_remove("search", "1.0", "end")
		try: word = nText.selection_get()
		except tk.TclError: word = ""
		text = nText.get("1.0", "end")
		self.eFind_str.set(None)
		poss = self.eFind_engene(text, word)
		if poss:
			for i, f in poss:
				pos = f"{i}.{f}"
				nText.tag_add(f"search", pos, f"{pos} + {len(word)}c")
				nText.tag_configure(f"search", background='SkyBlue', relief='raised')

		# Etc
	def altstream(self):
		self.mWin.after(100, self.altstream)
		self.mLblCheck = round(self.mLblCheck)
		if self.mNB.tabs() != ():
			if self.get_pfid(0) == "conf": nText = None
			else: nText = self.mWin.nametowidget(self.mNB.select()+".!text")
			if self.mLblCheck == 0:
				if nText:
					insLine, insCol = str.split(nText.index("insert"), ".")
					endLine = str(int(str.split(nText.index("end"), ".")[0]) - 1)
					endCol = str.split(nText.index(f"{insLine}.end"), ".")[1]
				else: insLine, insCol, endLine, endCol = [0 for i in " "*4]
				if self.get_pfid(0) == "file":
					path = self.get_pfid(1)
					self.mLbl["text"] = f"[File] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}  Path: {path}"
				elif self.get_pfid(0) == "note":
					self.mLbl["text"] = f"[Note] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}"
				elif self.get_pfid(0) == "conf":
					self.mLbl["text"] = f"[Config] Name: {self.get_pfid(1)}"
				else:
					self.mLbl["text"] = f"[Err] undifined type"
			elif self.mLblCheck > 0:
				self.mLblCheck -= 1
			if self.get_pfid(0) == "file":
				path = self.get_pfid(1)
				if sysplatform == "win32": tmp = path.split("\\")[-1]
				else: tmp = path.split("/")[-1]
				if nText.edit_modified() == True: self.mNB.tab(self.mNB.select(), text=tmp+"*")
				else: self.mNB.tab(self.mNB.select(), text=tmp.rstrip("*"))

	def nExec(api, path=None):
		if path == None:
			path = tkfd.askopenfilename(title="Exec file", filetypes=api.fform)
			if not path: return
		modtext = ""
		with open(path) as modfile:
			modtext = modfile.read()
		exec(modtext)

	# mainloop the mWin
	def init(self):
		self.forceTk()
		self.mWin.wm_protocol("WM_DELETE_WINDOW", self.withQuit)
		self.mWin.bind("<Button-2>", self.popU)
		self.mWin.bind("<Control-q>", lambda ev: self.withQuit())
		self.mWin.bind("<Control-Button-1>", lambda ev: self.eFind())
		self.mWin.bind("<Control-o>", lambda ev: self.nOpen())
		self.mWin.bind("<Control-s>", lambda ev: self.nSave())
		self.mWin.bind("<Control-S>", lambda ev: self.nSaveas())
		self.mWin.bind("<Control-n>", lambda ev: self.nNew())
		self.mWin.bind("<Control-N>", lambda ev: self.nNewnote())
		self.mWin.bind("<Control-D>", lambda ev: self.nClose())
		self.mWin.bind("<Control-e>", lambda ev: self.nExec())
		self.mWin.bind("<F2>", lambda ev: self.mod_styles())
		self.mWin.bind("<F1>", lambda ev: self.nInfo())
		self.mWin.update()
		self.mWin.minsize(
			int(self.wmBtn.winfo_width() * 4.5), 
			self.tBar.winfo_height() + self.hBar.winfo_height()
		)
		# TODO: add csd+ssd title?
		self.mWin.after_idle(self.altstream)
		if sysplatform != "win32": self.mWin.after_idle(lambda: self.mWin.attributes('-type', "normal"))
		self.topTk(True)
		self.mWin.mainloop()


if __name__ == "__main__": 
	app = App()
	app.init()
