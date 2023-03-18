#!/bin/python3 -B
from deps import *
imgCont = 0

from sourcelib import Source 
from widgetlib import *
# Source and widgets merged on new files

#TODO: sys.argv - open files by `extpad.bin '%f'`
#TODO: kill, to_title, to_helpbar - func on IFrame-side
print(f"[extpad] Run with: {sys.argv[1:]}")
class App():
	# Sourse
	IFrame = IFrame
	vkw = {
		"codename": "crypton", # Arch
		"build": 9, # Every update
		"path": 3, # Is path of version
		"channel": "b (beta)", # e(edge/alpha)/b(beta)/c(rc/release-candidate)/r(release)
	}
	def grc(main, row, column, *args): return {"row": row, "column": column}
	def __init__(self):
		self.version = f'{self.vkw["build"]}{self.vkw["channel"][0:1]}{self.vkw.setdefault("path", "")}'
		self.vsm = "Version kw: " + "".join((f"\n    {str(k)}: {str(w)}" for k, w in self.vkw.items()))
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
		grc = self.grc
		self.source = Source()
		self.mWin = self.source.srcWin
		self.mWin.title(f"ExtPad {self.version}")
		self.mWin.geometry("400x300")
		self.is_topTk = tk.BooleanVar(value=True)
		self.isCSD = tk.BooleanVar(value=True)
		self.is_menubar = tk.BooleanVar(value=False)
		self.is_hotbar = tk.BooleanVar(value=True)
		self.is_floatinit, self.is_mNBinit = [False for i in " "*2]
		self.wTk_float()
		self.style = self.source.srcStyle
		self.text_shared = SharedConf(tabs="0.5c", bd=0, highlightthickness=0, wrap="none")
		for clri in ["tw", "gw", "sb", "dsb", "lsb"]:
			exec(f"self.clr_{clri} = self.source.clr_{clri}", locals())
		self.clr_bg, self.clr_ts = self.clr_tw, self.clr_lsb
		self.fform = self.source.fileforms
		self.vInfo_hints = \
"""WM: <C/S>SD = <Client/Server>-Side Decorartion
Use <Alt-B1> to move window
Use <Button-2> to call uMenu
Move window to take focus (On CSD mode)
"""
		self.imgd = tk.BooleanVar(value=True)
		self.imgstmb = ["file", "note", "run"]
		self.imgst = self.imgstmb + ["save", "saveas", "new", "open", "min", "max", "normal", "close", "win"]
		#TODO: make (?) self.imgpool[imgi] = self.source.imgspool[imgi](self.color)
		for imgi in self.imgst:
			exec(f"self.img_{imgi} = self.source.img_{imgi}(self.clr_gw)", locals())
			exec(f"self.img_{imgi}_dark = self.source.img_{imgi}(self.clr_sb)", locals())
		for imgi in self.imgstmb:
			exec(f"self.img_mb{imgi} = self.source.img_{imgi}(self.clr_sb)", locals())
		self.mWin.iconphoto(True, self.source.img_win3)
		self.config_frames = {}
		self.mLblCheck = -1
		self.notec = 0
		self.eFind_str = tk.StringVar()
		self.theme_path_gw()

		# Title-Bar: wmButton, mainLabel, mainLabel
		self.tBar = tk.Frame(self.mWin, bg=self.clr_sb, highlightthickness=0, height=0)
		self.wmBtn = ttk.Button(self.tBar, style="Title.TButton", image=self.img_win)
		self.mMG = tk.Frame(self.tBar, bg=self.clr_sb, highlightthickness=0, height=0)
		self.mMGL = tk.Label(self.mMG, text=f"ExtPad {self.version}", bg=self.clr_sb, fg=self.clr_gw, height=0, width=0)
		self.mMGL.pack(fill="y", expand=1)
		for subel in [self.mMG, self.mMGL]:
			subel.bind('<Button-1>', self.wTk_point)
			subel.bind('<B1-Motion>', self.wTk_move)
			subel.bind('<Button-3>', lambda ev: self.pop_menu(ev, self.uMenu))
			subel.bind('<Double-Button-1>', lambda ev: self.withDB1())
		self.mWin.bind("<Alt-Button-1>", self.wTk_point)
		self.mWin.bind("<Alt-B1-Motion>", self.wTk_move)
		self.mMinBtn     = ttk.Button(self.tBar, style="Title.TButton", image=self.img_min,    command=self.withMin)
		self.mNormalBtn  = ttk.Button(self.tBar, style="Title.TButton", image=self.img_normal, command=self.withNormal)
		self.mMaxBtn     = ttk.Button(self.tBar, style="Title.TButton", image=self.img_max,    command=self.withMax)
		self.mQuitBtn    = ttk.Button(self.tBar, style="Title.TButton", image=self.img_close,  command=self.withQuit)
			# Menu
				# Bind this
		self.wmBtn.bind('<Button-1>', lambda ev: self.pop_menu(ev, self.uMenu, self.wmBtn))
				# Menus
		self.uMenu = tk.Menu(self.mWin) # Union(Wm also)
		self.wMenu = tk.Menu(self.mWin, tearoff=0)
		self.fMenu = tk.Menu(self.mWin, tearoff=0)
		self.eMenu = tk.Menu(self.mWin, tearoff=0)
		self.vMenu = tk.Menu(self.mWin, tearoff=0)

		self.mMTree = {
			self.uMenu: [
			["File",   self.fMenu],
			["Edit",   self.eMenu],
			["View",   self.vMenu],
			["Window", self.wMenu],
		], self.wMenu: [
			["CSD/SSD",         "",    self.isCSD,    self.wTk_float], 
			["Normal window",   "[8]", self.withNormal], 
			["Zoom window",     "[0]", self.withMin], 
			["Minimise window", "[_]", self.withMax], 
			["Window at top",   "",    self.is_topTk, self.wTk_top], 
			["Menubar",         "",    self.is_menubar, self.wTk_menubar], 
		], self.fMenu: [
			["Save",        "Ctrl-S",       self.nSave],
			["Save as...",  "Ctrl-Shift-S", self.nSaveas], 
			["Open",        "Ctrl-O",       self.nOpen],
			["New",         "Ctrl-N",       self.nNew], 
			["New note",    "Ctrl-Shift-N", self.nNewnote], 
			["Close",       "Ctrl-Shift-D", self.nClose], 
			["Exec ext-on", "Ctrl-E",       self.nExec], 
			["Quit",        "Ctrl-Q, [X]",  self.withQuit], 
		], self.eMenu: [
			["Undo",  "Ctrl-Z",        self.eUndo], 
			["Redo",  "Ctrl-Shift-Z",  self.eRedo], 
			["Cut",   "Ctrl-X",        self.eCut], 
			["Copy",  "Ctrl-C",        self.eCopy], 
			["Paste", "Ctrl-V",        self.ePaste], 
			["Find",  "Ctrl-B1",       self.eFind],
		], self.vMenu: [
			["About",         "F1",     self.vInfo], 
			["Themes",        "F2",     self.vThemes], 
			["Hotbar",        "",       self.is_hotbar, self.vHotbar], 
			["Swith pages >", "Ctrl->", self.mergeTab_left], 
			["Swith pages <", "Ctrl-<", self.mergeTab_right], 
		]}
		
		for mmenu, mmenu_casc in self.mMTree.items():
			for mma in mmenu_casc:
				match len(mma):
					case 0: mmenu.add_separator()
					case 2: mmenu.add_cascade(label=mma[0], menu=mma[1])
					case 3: mmenu.add_command(label=mma[0], accelerator=mma[1], command=mma[2])
					case 4: mmenu.add_checkbutton(label=mma[0], accelerator=mma[1], variable=mma[2], offvalue=False, onvalue=True, command=mma[3])

			# Pack this
		self.mQuitBtn.pack(fill="both", side="right")
		self.mMaxBtn.pack(fill="both", side="right")
		self.mMinBtn.pack(fill="both", side="right")
		self.wmBtn.pack(fill="both", side="left")
		self.mMG.pack(fill="both", expand=True)
		self.tBar.grid(**grc(0, 0), columnspan=2, sticky="nswe")

		# Help-Bar: mainSizegrip, tkhelpButton, mainLabel
		self.api_pane = ttk.Frame(self.mWin)
		self.hBar = ttk.Frame(self.mWin)
		self.mSG = ttk.Sizegrip(self.hBar)
		self.mLbl = ttk.Label(self.hBar, text=\
f'''Hello in first tab of ExtPad {self.version}; 
Take help/hints with F1-key press e.g. `Use Control->< to move tab (title)`''')
			# Pack this
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.api_pane.grid(**grc(2, 0), columnspan=2, sticky="nswe")
		self.hBar.grid(**grc(3, 0), columnspan=2, sticky="nswe")

		# Hot-Bar
		self.hotBar = ttk.Frame(self.mWin, style="Hotbar.TFrame")
		self.hotBtns = [
			[self.img_open, self.nOpen, "Open file"], 
			[self.img_save, self.nSave, "Save file"], 
			[self.img_saveas, self.nSaveas, "Save as ..."],
			[self.img_note, self.nNewnote, "New note"], 
			[self.img_new, self.nNew, "New file"], 
			[self.img_run, self.nExec, "Exec ext-on"], 
		]
		for i in list(range(len(self.hotBtns))):
			self.hotBtns[i].append(ttk.Button(self.hotBar, image=self.hotBtns[i][0], command=self.hotBtns[i][1]))
			Hovertip(self.hotBtns[i][3], self.hotBtns[i][2], hover_delay=80)
			self.hotBtns[i][3].pack(fill="both", side="top", padx=2, pady=1)
		self.hotBar.grid(**grc(1, 0), sticky="nswe")

		# mainNoteBook
		self.mNB = CNotebook(self.mWin, height=0)
		if not sys.argv[1:]: self.nNewnote()
		else: print("ENV!")
		self.mNB.bind("<<NotebookTabChanged>>", self.nSel)
		self.mNB.bind("<<NotebookTabClosed>>", lambda ev: self.nClose(k=ev.x))
		self.mNB.grid(**grc(1, 1), sticky="nswe")
		self.is_mNBinit = True
		self.mWin.grid_rowconfigure(1, weight=1)
		self.mWin.grid_columnconfigure(1, weight=1)

		## The cfg-panes
		# cfg:info
		self.config_frames["root.info"] = IFrame(dict(fid=["conf", "info"]), master=self.mNB, name='conf:"info"')
		self.infoNB = ttk.Notebook(master=self.config_frames["root.info"])
		self.infoNBpages = {
			"ver": InfoFrame(dict(text_ph=self.vsm), self.infoNB, style="ghost.TFrame"),
			"doc": InfoFrame(dict(text_ph=self.__doc__), self.infoNB, style="ghost.TFrame"),
			"hint": InfoFrame(dict(text_ph=self.vInfo_hints), self.infoNB, style="ghost.TFrame")
		}
		self.infoNB.add(self.infoNBpages["ver"], text="Version", sticky="nswe")
		self.infoNB.add(self.infoNBpages["doc"], text="Description", sticky="nswe")
		self.infoNB.add(self.infoNBpages["hint"], text="Hints", sticky="nswe")
		for e in self.infoNBpages.values():
			self.text_shared.addw(e.text)
		self.infoNB.bind("<<NotebookTabChanged>>", lambda ev: self.vInfo_text())
		self.infoNB.pack(expand=1, fill="both")

		# cfg:theme
		self.config_frames["root.theme"] = IFrame(dict(fid=["conf", "theme"]), master=self.mNB, name='conf:"theme"')
		self.iTheme_tcombox = ttk.Combobox(self.config_frames["root.theme"], value=sorted(self.style.theme_names(), key=str.lower))
		self.iTheme_tcombox.set(self.style.theme_use())
		self.iTheme_tcombox.bind("<Return>", self.vThemes_sel)
		self.iTheme_tbtn = ttk.Button(self.config_frames["root.theme"], text="[Run]", command=self.vThemes_sel)
		self.iTheme_cbtn = ttk.Checkbutton(
			self.config_frames["root.theme"], text="light/dark icon", 
			variable=self.imgd, offvalue=False, onvalue=True, 
			command=self.themeChanged)
		self.iTheme_bgfield = EntryField(dict(ebind=self.vThemes_textbg, efill=self.clr_bg, bfill="[text_bg]"), self.config_frames["root.theme"])
		self.iTheme_fgfield = EntryField(dict(ebind=self.vThemes_textfg, efill="black", bfill="[text_fg]"), self.config_frames["root.theme"])
		self.iTheme_tsfield = EntryField(dict(ebind=self.vThemes_textsel, efill=self.clr_ts, bfill="[text_ts]"), self.config_frames["root.theme"])
		self.iTheme_tcombox.grid(**self.grc(0, 0), sticky="nswe")
		self.iTheme_tbtn.grid(**self.grc(0, 1), sticky="nswe")
		self.iTheme_cbtn.grid(**self.grc(1, 0), sticky="nswe", columnspan=2)
		self.iTheme_bgfield.grid(**self.grc(2, 0), sticky="nswe", columnspan=2)
		self.iTheme_fgfield.grid(**self.grc(3, 0), sticky="nswe", columnspan=2)
		self.iTheme_tsfield.grid(**self.grc(4, 0), sticky="nswe", columnspan=2)
		ttk.Label(self.config_frames["root.theme"])\
		.grid(**self.grc(9, 0), sticky="nswe", columnspan=2)
		self.config_frames["root.theme"].rowconfigure(9, weight=1)
		self.config_frames["root.theme"].columnconfigure(0, weight=1)
		self.mWin.bind("<<ThemeChanged>>", self.themeChanged)

		self.wTk_force()
		self.mWin.wm_protocol("WM_DELETE_WINDOW", self.withQuit)
		self.mWin.bind("<Button-2>", lambda ev: self.pop_menu(ev, self.uMenu))
		self.mWin.bind("<Control-q>", lambda ev: self.withQuit())
		self.mWin.bind("<Control-greater>", lambda ev: self.mergeTab_left())# ^>
		self.mWin.bind("<Control-less>", lambda ev: self.mergeTab_right())# ^<
		self.mWin.bind("<Control-Button-1>", lambda ev: self.eFind())
		self.mWin.bind("<Control-o>", lambda ev: self.nOpen())
		self.mWin.bind("<Control-s>", lambda ev: self.nSave())
		self.mWin.bind("<Control-S>", lambda ev: self.nSaveas())
		self.mWin.bind("<Control-n>", lambda ev: self.nNew())
		self.mWin.bind("<Control-N>", lambda ev: self.nNewnote())
		self.mWin.bind("<Control-D>", lambda ev: self.nClose())
		self.mWin.bind("<Control-e>", lambda ev: self.nExec())
		self.mWin.bind("<F2>", lambda ev: self.vThemes())
		self.mWin.bind("<F1>", lambda ev: self.vInfo())
		self.mWin.update()
		self.mWin.after_idle(self.altstream)
		if sys.platform != "win32": self.mWin.after_idle(lambda: self.mWin.attributes('-type', "normal"))
		self.wTk_top(True)
		self.mWin.minsize(*self.mWin_min())
		self.mWin.mainloop()

	# Funcions
		# Tk
	def mWin_min(self, i=None):
		s0 = self.wmBtn.winfo_width()*4+self.mMGL.winfo_width()
		max_little0 = self.wmBtn.winfo_width()*10
		out = [[max_little0, s0][s0 <= max_little0], (self.tBar.winfo_height()+self.hBar.winfo_height())]
		if i != None: return out[i]
		return out
	def mNB_addc(self, frame, text):
		self.mNB.add(frame, image=self.img_mbrun, text=text, compound="left")
	def themeChanged(self, *a, **kw):
		color1 = ['self.clr_sb', 'self.clr_gw'][self.imgd.get()]
		color2 = ['self.clr_gw', 'self.clr_sb'][self.imgd.get()]
		for imgi in self.imgst:
			exec(f"self.img_{imgi}['foreground'] = {color1}", locals())
			exec(f"self.img_{imgi}_dark['foreground'] = {color2}", locals())
		self.theme_path_gw()
	def vThemes_sel(self, *a, **kw):
		req = self.iTheme_tcombox.get()
		if req.strip() == "": return
		self.style.theme_use(req)
		self.iTheme_tcombox["value"] = sorted(self.style.theme_names(), key=str.lower)
	def vThemes_textbg(self, *a, **kw):
		req = self.iTheme_bgfield.text.get().strip()
		if req == "": return
		old = self.text_shared.setdefault("bg", self.clr_bg)
		try:
			self.text_shared["bg"] = req
			self.clr_bg = req
		except:
			self.text_shared["bg"] = old
			self.clr_bg = old
		self.theme_path_gw()
	def vThemes_textfg(self, *a, **kw):
		req = self.iTheme_fgfield.text.get().strip()
		if req == "": return
		old = self.text_shared.setdefault("fg", "black")
		try: self.text_shared["fg"] = req
		except: self.text_shared["fg"] = old
	def vThemes_textsel(self, *a, **kw):
		req = self.iTheme_tsfield.text.get().strip()
		if req == "": return
		self.clr_ts = req
	def vThemes(self): self.mNB_addc(self.config_frames["root.theme"], text=f"Themes")
	def vInfo_text(self):
		self.config_frames["root.info"].text = self.mWin.nametowidget(self.infoNB.select()).text
	def vInfo(self): self.mNB_addc(self.config_frames["root.info"], text=f"Info")
	def vHotbar(self, bl=None):
		if bl == None: bl = self.is_hotbar.get()
		if bl: self.hotBar.grid()
		else: self.hotBar.grid_remove()
	def theme_path_gw(self):
		is_customst = self.style.theme_use() in ["deft", "deftc"]
		self.style.map("ghost.TLabel", background = [("", self.clr_bg)])
		self.style.map("ghost.TFrame", background = [("", self.clr_bg)])
		self.style.map("ghost.TSizegrip", background = [("", self.clr_bg)])
		self.style.map("CNotebook", background=[("selected", self.clr_bg)])
		self.style.map("CNotebook.Tab", background=[("selected", self.clr_bg)])
		if self.is_mNBinit:
			self.mNB.style.theme_use(self.style.theme_use())
		if is_customst:
			self.style.map("TScrollbar", background = [("", self.clr_bg)])
	def wTk_force(self, *args): 
		self.mWin.focus_force()
		self.mWin.grab_release()
	def wTk_top(self, bl=None, **kw): 
		if bl == None: bl = self.is_topTk.get()
		kw.setdefault("win", self.mWin).attributes("-topmost", bl)
	def retitle(self, s):
		self.mMGL["text"] = s
		self.mWin.title(s)
	def mergeTab_left(self):
		c = self.mNB.index("current")
		l = self.mNB.index("end")
		w = self.mWin.nametowidget(self.mNB.select())
		if c >= l-1: return
		self.mNB.insert(c+1, w)
	def mergeTab_right(self):
		c = self.mNB.index("current")
		l = self.mNB.index("end")
		w = self.mWin.nametowidget(self.mNB.select())
		if not c: return
		self.mNB.insert(c-1, w)
	def wTk_float(self, bl=None): 
		if bl == None: bl = self.isCSD.get()
		if sys.platform == "win32": self.mWin.overrideredirect(bl)
		else: self.mWin.attributes('-type', ["normal", "dock"][bl])
		if self.is_floatinit:
			if bl: self.tBar.grid()
			else: self.tBar.grid_remove()
		else: self.is_floatinit = True
		self.mWin.wm_state("withdraw")
		self.mWin.wm_state("normal")
		self.mWin["takefocus"] = True
	def wTk_menubar(self, bl=None): 
		if bl == None: bl = self.is_menubar.get()
		if bl: self.mWin["menu"] = self.uMenu
		else:  self.mWin["menu"] = False
	def wTk_point(self, event):
		win_position = [int(coord) for coord in self.mWin.wm_geometry().split('+')[1:]]
		self.source.xTk, self.source.yTk = win_position[0] - event.x_root, win_position[1] - event.y_root
		self.wTk_force() # Take focus
	def wTk_move(self, event): 
		if self.source.Tk == "max": 
			self.withNormal()
			return
		self.mWin.wm_geometry(f"+{str(event.x_root+self.source.xTk)}+{str(event.y_root+self.source.yTk)}")
	def withNormal(self):
		if self.source.Tk == "normal": return
		self.mWin.minsize(*self.mWin_min())
		self.mNormalBtn.pack_forget()
		self.mMaxBtn.pack_forget()
		self.mMinBtn.pack_forget()
		self.mMG.pack_forget()
		self.mLbl.pack_forget()
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.mWin.geometry(f"{self.source.ww}x{self.source.wh}+{self.source.wrx}+{self.source.wry}")
		self.mMaxBtn.pack(fill="both", side="right")
		self.mMinBtn.pack(fill="both", side="right")
		self.hBar.grid()
		self.mMG.pack(fill="both", expand=True)
		self.source.Tk = "normal"
	def withMax(self):
		if   self.source.Tk == "max": return
		elif self.source.Tk == "min": 
			self.withNormal()
			return
		self.mNormalBtn.pack_forget()
		self.mMaxBtn.pack_forget()
		self.mMinBtn.pack_forget()
		self.mMG.pack_forget()
		self.mSG.pack_forget()
		self.tmpx = self.mWin.cget("padx")
		self.tmpy = self.mWin.cget("pady")
		self.source.wrx = self.mWin.winfo_rootx()
		self.source.wry = self.mWin.winfo_rooty()
		self.source.ww  = self.mWin.winfo_width()
		self.source.wh  = self.mWin.winfo_height()
		self.mWin.geometry(f"{self.mWin.winfo_screenwidth()}x{self.mWin.winfo_screenheight()}+0+0")
		self.mNormalBtn.pack(fill="both", side="right")
		self.mMinBtn.pack(fill="both", side="right")
		self.mMG.pack(fill="both", expand=True)
		self.source.Tk = "max"
	def withMin(self):
		if   not self.isCSD.get():
			self.mWin.state("icon")
			return
		if   self.source.Tk in ["min", "max"]:
			self.withNormal()
			return
		self.mNormalBtn.pack_forget()
		self.mMaxBtn.pack_forget()
		self.mMinBtn.pack_forget()
		self.mMG.pack_forget()
		self.hBar.grid_remove()
		self.tmpx = self.mWin.cget("padx")
		self.tmpy = self.mWin.cget("pady")
		self.source.wrx = self.mWin.winfo_rootx()
		self.source.wry = self.mWin.winfo_rooty()
		self.source.ww  = self.mWin.winfo_width()
		self.source.wh  = self.mWin.winfo_height()
		tBarh = self.tBar.winfo_height()
		self.mWin.minsize(self.mWin_min(0), tBarh)
		self.mWin.geometry(f"{self.mWin_min(0)}x{tBarh}+0+{self.mWin.winfo_screenheight()-tBarh}")
		self.mMaxBtn.pack(fill="both", side="right")
		self.mMinBtn.pack(fill="both", side="right")
		self.mMG.pack(fill="both", expand=True)
		self.source.Tk = "min"
	def withDB1(self):
		if   self.source.Tk in ["max", "min"]: self.withNormal()
		elif self.source.Tk == "normal": self.withMax()
	def withQuit(self):
		if self.mNB.tabs() != () and self.source.future_fast_quit:
			if not tkmb.askokcancel("You sure?", "You may have unsaved changes"): return
		for i in range(len(self.mNB.tabs())): 
			if self.nClose(): return
		self.source.quit()
		# Menu
	def pop_menu(self, ev, menu, button=None):
		try:
			menu.tk_popup(ev.x_root, ev.y_root, "none")
			if not button: menu.bind("<FocusOut>", lambda ev: menu.unpost())
		finally:
			menu.grab_release()
		if button: button["state"] = "!selected"
	def get_nPage(self): return self.mWin.nametowidget(self.mNB.select())
	def nSel(self, *args):
		if   self.mNB.tabs() == ():
			self.mLbl["text"] = f"Hello in ExtPad {self.version}"
			self.mLblCheck = -1
		#elif self.mWin.nametowidget(self.mNB.select()).id == ["note", 0]:
		#	self.mLbl["text"] = " ... "
		#	self.mLblCheck = 100
		else: self.mLblCheck = 0
	def nOpen(self, path=None):
		# Input path, text
		if path == None:
			path = tkfd.askopenfilename(
				title="Open file",
				filetypes=self.fform
			)
			self.wTk_force()
			if not path: return
		with open(str(path)) as nfile: text = nfile.read()
		# Controls
		nPage = NBFrame(
			dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["file", path], text=text),
			self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"'
		)
		nPage.ikw["tid"] = self.text_shared.addw(nPage.text)
		self.mNB.add(nPage, image=self.img_mbfile, text=ospath.split(path)[-1], compound="left")
	def nSaveas(self):
		if self.mNB.tabs() == (): return "cancel:notabs"
		nPage = self.get_nPage()
		ntype = nPage.id[0]
		if ntype in ("file", "note"):
			path = tkfd.asksaveasfilename(
				title="Save as",
				defaultextension=".txt", 
				filetypes=self.fform
			)
			self.wTk_force()
			if not path: return "cancel:nopath"
			try:
				nText = nPage.text
				nText.edit_reset()
				nText.edit_modified(0)
				nfile = open(path, "w")
				nfile.write(nText.get("1.0", "end").rstrip("\n"))
				nfile.close()
			except: print("[app][nSaveas] Can't save file")
		if ntype == "note":
			nPage.id = ["file", path]
			self.mNB.add(nPage, image=self.img_mbfile, text=ospath.split(path)[-1], compound="left")
	def nSave(self):
		if self.mNB.tabs() == (): return
		nPage = self.get_nPage()
		ntype = nPage.id[0]
		if ntype == "file":
			path = nPage.id[1]
			nText = nPage.text
			nText.edit_modified(0)
			nfile = open(path, "w")
			nfile.write(nText.get("1.0", "end").rstrip("\n"))
			nfile.close()
			self.mLblCheck = 10
			self.mLbl["text"] = "[File] File saved"
		elif ntype == "note": self.nSaveas()
	def nNew(self):
		path = tkfd.asksaveasfilename(
			title="New file",
			defaultextension=".txt", 
			filetypes=self.fform
		)
		self.wTk_force()
		if not path: return
		# Controls
		nPage = NBFrame(
			dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["file", path]),
			self.mNB, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"'
		)
		nPage.ikw["tid"] = self.text_shared.addw(nPage.text)
		self.mNB.add(nPage, image=self.img_mbfile, text=ospath.split(path)[-1], compound="left")
	def nNewnote(self):
		nPage = NBFrame(
			dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["note", self.notec]), 
			self.mNB, style="ghost.TFrame", name=f'note:"{self.notec}"'
		)
		nPage.ikw["tid"] = self.text_shared.addw(nPage.text)
		self.mNB.add(nPage, image=self.img_mbnote, text=f"New{['', f' ({self.notec})'][bool(self.notec)]}", compound="left")
		self.notec += 1
	def nClose(self, **kw):
		if self.mNB.tabs() == (): return
		tabid = kw.setdefault("k", self.mNB.index("current"))
		tab = self.mWin.nametowidget(self.mNB.tabs()[tabid])
		fail = None
		if tab.id[0] == "file":
			nText = self.get_nPage().text
			if nText.edit_modified():
				tmp = self.mNB.select().split(":")[1].strip('"').replace("%2E", ".")
				save = tkmb.askyesnocancel(
					f"Save file {tmp}",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: fail = self.nSave()
				elif save == None: return "break"
		elif tab.id[0] == "note":
			nText = self.get_nPage().text
			if nText.edit_modified():
				save = tkmb.askyesnocancel(
					f"Save note",
					"You have unsaved changes.\nDo you want to save before closing?",
				)
				if save: fail = self.nSave()
				elif save == None: return "break"
		elif tab.id[0] == "conf":
			print(f"[app][nClose] Closing config: {tab.id[1]}")
		else: print("[app][nClose] Unknown type (fail)")
		tid = tab.ikw.setdefault("tid")
		if   isinstance(tid, dict): pass
		elif not isinstance(tid, list | tuple): self.text_shared.rmw(tid)
		elif isinstance(tid, list | tuple): [self.text_shared.rmw(i) for i in tid]
		if not fail: self.mNB.forget(tabid)
	def eUndo(self): 
		try: 
			self.get_nPage().text.edit_undo()
		except tk.TclError as exc: print(f"[app][eUndo] Can't undo: {exc}")
	def eRedo(self): 
		try: 
			self.get_nPage().text.edit_redo()
		except tk.TclError as exc: print(f"[app][eRedo] Can't redo: {exc}")
	def eCopy(self): 
		try: 
			nText = self.get_nPage().text
			if nText.index(tk.SEL_FIRST) == nText.index(tk.SEL_LAST): return "break:seleq"
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
		except tk.TclError as exc: print(f"[app][eCopy] Can't copy: {exc}")
	def ePaste(self): 
		try: 
			nText = self.get_nPage().text
			s = nText.clipboard_get()
			self.get_nPage().text.insert("insert", s)
			if nText.index(tk.SEL_FIRST) == nText.index(tk.SEL_LAST): return "seleq" 
			nText.selection_clear()
		except tk.TclError as exc: print(f"[app][ePaste] Can't paste: {exc}")
	def eCut(self):
		try:
			nText = self.get_nPage().text
			if nText.index(tk.SEL_FIRST) == nText.index(tk.SEL_LAST): return "break:seleq"
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
			nText.delete(tk.SEL_FIRST, tk.SEL_LAST)
		except tk.TclError as exc: print(f"[app][eCut] Can't cut: {exc}")
	def eFind_engene(self, s: str, w: str) -> list:
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
		nText = self.get_nPage().text
		if not nText: return
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
				nText.tag_configure(f"search", background=self.clr_ts, relief='raised')

		# Etc
	def altstream(self):
		self.mWin.after(100, self.altstream)
		self.mLblCheck = int(self.mLblCheck)
		if self.mNB.tabs() != ():
			nPage = self.get_nPage()
			if nPage.id[0] == "conf": nText = None
			else: nText = nPage.text
			if self.mLblCheck == 0:
				if nText:
					insLine, insCol = str.split(nText.index("insert"), ".")
					endLine = str(int(str.split(nText.index("end"), ".")[0]) - 1)
					endCol = str.split(nText.index(f"{insLine}.end"), ".")[1]
				else: insLine, insCol, endLine, endCol = [0 for i in " "*4]
				if nPage.id[0] == "file":
					self.mLbl["text"] = f"[File] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}  Path: {nPage.id[1]}"
				elif nPage.id[0] == "note":
					self.mLbl["text"] = f"[Note] Line: {insLine}/{endLine}  Col: {insCol}/{endCol}"
				elif nPage.id[0] == "conf":
					self.mLbl["text"] = f"[Config] Name: {nPage.id[1]}"
				else:
					self.mLbl["text"] = f"[Err] undifined type"
			elif self.mLblCheck > 0:
				self.mLblCheck -= 1
			if nPage.id[0] in ["file", "note"]:
				path = nPage.id[1]
				if nPage.id[0] == "note":
					tmp = f"New{['', f' ({path})'][bool(path)]}"
				else:
					if sys.platform == "win32": tmp = path.split("\\")[-1]
					else: tmp = path.split("/")[-1]
				if nText.edit_modified() == True: self.mNB.tab(self.mNB.select(), text=tmp+"*")
				else: self.mNB.tab(self.mNB.select(), text=tmp.rstrip("*"))

	def nExec(api, path=None):
		if not path:
			path = tkfd.askopenfilename(title="Exec ext-on", filetypes=api.fform)
			if not path: return
		with open(path) as modfile: exec(modfile.read())

if __name__ == "__main__": 
	app = App()
