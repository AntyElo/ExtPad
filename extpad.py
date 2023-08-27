#!/bin/python3 -B
from deps import *
imgCont = 0

from sourcelib import Source 
from widgetlib import *
# Source and widgets merged on new files

__doc__ = """EXTernal notePAD (main file)

 Options:

-n, --note
 Start with note page (default)

-c <file>, --config=<file>
 [Not implemented]

-w, --nocsd
 Start whitout window decorations (CSD)

"""
optargs = getopt.gnu_getopt(sys.argv[1:], OPT, OPTX)
print(f"[extpad] Run {sys.argv[0]} with: {sys.argv[1:]}")
print(f"[extpad] [ ] Getopt/cmn: {getopt.getopt(sys.argv[1:], OPT, OPTX)}")
print(f"[extpad] [x] Getopt/gnu: {optargs}")
class App():
	# Sourse
	IFrame = IFrame
	vkw = {
		"codename": "crypton", # Arch
		"build": 11, # Every update
		"path": 4, # Is path of version
		"channel": "beta", # Edge aka alpha / Beta / Candidate4Release aka rc / Release
	}
	def grc(main, row, column, *args): return {"row": row, "column": column}
	def __init__(self):
		global optargs
		self.ropt, self.rargs = ropt, rargs = self.optargs = optargs
		sourcekw = {}
		for key, word, *_ in ropt:
			match key:
				case "-h" | "--help":
					print(__doc__)
					exit()
				#case "-c" | "--config":
				#	self.openConfig(word)
				case "--tth" | "--ttkthemes":
					sourcekw["tth_future"] = True
				case "--notth" | "--nottkthemes":
					sourcekw["tth_future"] = False
				case "--deftc":
					sourcekw["deftc_ffuture"] = True
				case "--fquit" | "--fastquit":
					sourcekw["quit_ffuture"] = True
				case "-d":
					deps_test()
					sourcekw["tth_future"] = True
					sourcekw["quit_ffuture"] = True
		self.version = f'{self.vkw["build"]}{self.vkw["channel"][0:1]}{["", self.vkw.get("path", "")][bool(self.vkw.get("path", ""))]}'
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
		self.source = Source(**sourcekw)
		del sourcekw
		self.mWin = self.source.srcWin
		self.mWin.title(f"ExtPad {self.version}")
		self.mWin.geometry("400x300")
		self.is_topTk = tk.BooleanVar(value=False)
		self.isCSD = tk.BooleanVar(value=True)
		self.is_menubar = tk.BooleanVar(value=False)
		self.is_hotbar = tk.BooleanVar(value=True)
		self.is_apibar = tk.BooleanVar(value=True)
		self.wTk_float()
		self.titlem = 1 #Mod0: "%s"; Mod1: "ExtPad {V} - %s"; Mod1: "%s - ExtPad {V}"
		self.titler = ["", "", f" - ExtPad {self.version}"]
		self.titlel = ["", f"ExtPad {self.version} - ", ""]
		self.vInfo_hints = \
"""WM: <C/S>SD = <Client/Server>-Side Decorartion
Use <Alt-B1> to move window
Use <Button-2> to call uMenu
Move window to take focus (On CSD mode)
Use <Button-2> on TextLN to take goto-hover
"""
		self.fform = self.source.fileforms
		self.style = self.source.srcStyle
		self.text_shared = SharedConf(tabs="0.5c", bd=0, highlightthickness=0, wrap="none")
		for clri in ["tw", "gw", "sb", "dsb", "lsb", "tkbg"]:
			exec(f"self.clr_{clri} = self.source.clr_{clri}", locals())
		self.clr_bg, self.clr_ts = self.clr_tw, self.clr_lsb
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
		self.mLblQ = []
		self.notec = 0
		self.eFind_str = tk.StringVar()
		self.theme_path_gw()

		# Title-Bar: wmButton, mainLabel, mainLabel
		self.tBar = tk.Frame(self.mWin, bg=self.clr_sb, highlightthickness=0, height=0)
		self.wmBtn = ttk.Button(self.tBar, style="Title.TButton", image=self.img_win)
		self.mMG = tk.Frame(self.tBar, bg=self.clr_sb, highlightthickness=0, height=0)
		self.mMGL = tk.Label(self.mMG, text=f"ExtPad {self.version}", bg=self.clr_sb, fg=self.clr_gw, height=0, width=0)
		self.mMGL.pack(fill="y", expand=1)
		for subelm in [self.mMG, self.mMGL]:
			subelm.bind('<Button-1>', self.wTk_point)
			subelm.bind('<B1-Motion>', self.wTk_move)
			subelm.bind('<Button-3>', lambda ev: self.pop_menu(ev, self.uMenu))
			subelm.bind('<Double-Button-1>', lambda ev: self.withDB1())
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
		self.uMenu =  tk.Menu(self.mWin) # Union(Wm also)
		self.wMenu =  tk.Menu(self.mWin, tearoff=0)
		self.fMenu =  tk.Menu(self.mWin, tearoff=0)
		self.fnMenu = tk.Menu(self.mWin, tearoff=0)
		self.eMenu =  tk.Menu(self.mWin, tearoff=0)
		self.vMenu =  tk.Menu(self.mWin, tearoff=0)

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
		], self.fnMenu: [
			["New file",         "Ctrl-N",       self.nNew], 
			["New note",         "Ctrl-Shift-N", self.nNewnote], 
			["New python shell", "F3",     self.vPyshell],
		], self.fMenu: [
			["Save file",   "Ctrl-S",       self.nSave],
			["Save as...",  "Ctrl-Shift-S", self.nSaveas], 
			["Open file",   "Ctrl-O",       self.nOpen],
			["New ...",                     self.fnMenu],
			["Close tab",   "Ctrl-Shift-D", self.nClose], 
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
			["Hotbar",        "",       self.is_hotbar,  lambda: self.iGrid(self.is_hotbar, self.hotBar)], 
			["Bottombar",     "",       self.is_apibar,  lambda: self.iGrid(self.is_apibar, self.apiBar)], 
			["Menubar",       "",       self.is_menubar, self.wTk_menubar], 
			["Swith pages >", "Ctrl->", self.mergeTab_left], 
			["Swith pages <", "Ctrl-<", self.mergeTab_right],
		]}
		
		for mmenu, mmenu_casc in self.mMTree.items():
			for mma in mmenu_casc:
				match len(mma):
					case 0: mmenu.add_separator()
					case 1: 
						t = mma[0] + " "
						if t[0] == " ": mmenu.add_command(accelerator=mma[0])
						else: mmenu.add_command(label=mma[0])
					case 2: mmenu.add_cascade(label=mma[0], menu=mma[1])
					case 3: mmenu.add_command(label=mma[0], accelerator=mma[1], command=mma[2])
					case 4: mmenu.add_checkbutton(label=mma[0], accelerator=mma[1], \
						variable=mma[2], offvalue=False, onvalue=True, command=mma[3])

			# Pack this
		self.mQuitBtn.pack(fill="both", side="right")
		self.mMaxBtn.pack(fill="both", side="right")
		self.mMinBtn.pack(fill="both", side="right")
		self.wmBtn.pack(fill="both", side="left")
		self.mMG.pack(fill="both", expand=True)
		self.tBar.grid(**grc(0, 0), columnspan=2, sticky="nswe")

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
		for i, hbe in enumerate(self.hotBtns):
			self.hotBtns[i].append(ttk.Button(self.hotBar, image=hbe[0], command=hbe[1]))
			hbe = self.hotBtns[i]
			hbe[3].bind("<Enter>", lambda ev, t=hbe[2]: self.hBar_tip_new(t))
			hbe[3].bind("<Leave>", lambda ev: self.hBar_tip_dispose())
			hbe[3].pack(fill="both", side="top", padx=2, pady=1)
		self.hotBar.grid(**grc(1, 0), rowspan=2, sticky="nswe")

		# api-Bar: -> mods
		self.apiBar  = ttk.Frame(self.mWin)
		self.gotofr = EntryToolFrame(self.apiBar, "goto:", self.tGoto, self.get_nPage)
		self.findfr = EntryToolFrame(self.apiBar, "find:", self.eFind, self.get_nPage)
		self.colorfr = ColorToolFrame(self.apiBar)
		self.gotofr.pack(fill="y", side="left", padx=1)
		self.findfr.pack(fill="y", side="left", padx=1)
		self.colorfr.pack(fill="y", side="left", padx=1)
		self.apiBar.grid(**grc(2, 1), sticky="nswe")

		# Help-Bar: mainSizegrip, tkhelpButton, mainLabel
		self.hBar = ttk.Frame(self.mWin)
		self.mSG = ttk.Sizegrip(self.hBar)
		self.mLbl = ttk.Label(self.hBar, text=f"Hello in ExtPad {self.version}")
			# Pack this
		self.mSG.pack(fill="both", side="right")
		self.mLbl.pack(fill="both", expand=True)
		self.hBar.grid(**grc(3, 0), columnspan=2, sticky="nswe")

		# mainNoteBook
		self.mNB = CNotebook(self.mWin, height=0, cstyle=self.style)
		if not rargs: self.nNewnote()
		for key, word, *_ in ropt:
			match key:
				case "-n" | "--note":
					self.nNewnote()
				case "-w" | "--nocsd":
					self.isCSD.set(False)
					self.wTk_float()
		for elm in rargs:
			self.nOpen(elm)
		self.mNB.bind("<<NotebookTabChanged>>", lambda ev: self.hBar_tip_dispose())
		self.mNB.bind("<<NotebookTabClosed>>", lambda ev: self.nClose(k=ev.x))
		self.mNB.grid(**grc(1, 1), sticky="nswe")
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
		self.mWin.bind("<F1>", lambda ev: self.vInfo())
		self.mWin.bind("<F2>", lambda ev: self.vThemes())
		self.mWin.bind("<F3>", lambda ev: self.vPyshell())
		self.mWin.update()
		self.mWin.after_idle(self.altstream)
		if sys.platform != "win32": self.mWin.after_idle(lambda: self.mWin.attributes('-type', "normal"))
		self.mWin.minsize(*self.mWin_min())
		self.mWin.mainloop()

	# Funcions
		# Tk
	def mWin_min_geth(self, w):
		'mWin minimal height'
		return w.winfo_height()*w.winfo_ismapped()
	def mWin_min_getw(self, w):
		'mWin minimal weight'
		return w.winfo_width()*w.winfo_ismapped()
	def mWin_min(self, i=None):
		'mWin minimal [height, weight]'
		tBarw = self.wmBtn.winfo_width()*4+self.mMGL.winfo_width()
		max_littlew = self.wmBtn.winfo_width()*10
		tBarcw = [max_littlew, tBarw][tBarw <= max_littlew]
		out = [tBarcw, sum(map(self.mWin_min_geth, (self.tBar, self.apiBar)))+self.hBar.winfo_height()]
		if i != None: return out[i]
		return out
	def mNB_addc(self, frame, text):
		'Add <frame> at main NoteBook'
		self.mNB.add(frame, image=self.img_mbrun, text=text, compound="left")
	def frame_get(self, frame, seq, default=None, prefix="_extpad_"):
		'''Requite attribute _extpad_<seq> from <frame>
		
		Options:
		<default> - default value (None) 
		<prefix> - prefix ("_extpad_")'''
		return getattr(frame, prefix+seq, default)
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
		self.themeChanged()
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
	def tGoto(self, get):
		if self.mNB.tabs() == (): return
		tab = self.get_nPage()
		if tab.id[0] not in ["file", "note"]: return
		if   get.isnumeric():
			get = int(get)
			if get < int(tab.text.index("end").split(".")[0]):
				tab.text.see(f"{get}.0")
		elif get.replace(".", "9").isnumeric():
			l = int(get.split(".")[0]) if get.split(".")[0] != "" else 1
			c = int(get.split(".")[1]) if get.split(".")[1] != "" else 0
			it = str.split(tab.text.index("insert"), ".")
			el = int(tab.text.index("end").split(".")[0])
			ec = int(str.split(tab.text.index(f"{it[0]}.end"), ".")[1])
			if l < el and c <= ec:
				tab.text.see(f"{l}.{c}")
		tab.lnw.redraw()
	def vThemes(self): self.mNB_addc(self.config_frames["root.theme"], text=f"Themes")
	def vInfo_text(self):
		self.config_frames["root.info"].text = self.mWin.nametowidget(self.infoNB.select()).text
	def vInfo(self): self.mNB_addc(self.config_frames["root.info"], text=f"Info")
	def vPyshell(self):
		try:
			from pyshell import TextConsole
		except ImportError:
			print("[extpad] pyshell unsupported")
			return
		frame = self.IFrame(dict(fid=["term", "pyshell"], name="Pyshell"), master=self.mNB)
		frame.text = TextConsole(frame, highlightthickness=0, bd=0)
		frame.text.pack(fill="both", expand="True")
		frame.api_on_hbar = lambda: \
f"[{frame.name}]  Line: {frame.text.index('current').split('.')[0]}" \
f"/{frame.text.index('end-1c').split('.')[0]}  " \
f"Col: {frame.text.index('current').split('.')[1]}" \
f"/{frame.text.index('{}.end'.format(frame.text.index('current').split('.')[0])).split('.')[1]}"
		frame.ikw["tid"] = self.text_shared.addw(frame.text)
		self.mNB_addc(frame, text=f"Python shell")
	def iGrid(self, var, w):
		if var.get(): w.grid()
		else: w.grid_remove()
	def iGrid_raw(self, var, w):
		if var: w.grid()
		else: w.grid_remove()
		return (not var)
	def theme_path_gw(self):
		is_customst = self.style.theme_use() in ["deft", "deftc"]
		if self.__dict__.get("mNB"):
			self.mNB.style.configure("CNotebook", background=self.mWin.cget("bg"))
			self.mNB.style.map("CNotebook", background = [("", self.mWin.cget("bg")), ("selected", self.clr_bg)])
		self.style.map("ghost.TLabel", background = [("", self.clr_bg)])
		self.style.map("ghost.TFrame", background = [("", self.clr_bg)])
		self.style.map("ghost.TSizegrip", background = [("", self.clr_bg)])
		self.style.map("CNotebook", background=[("selected", self.clr_bg)])
		self.style.map("CNotebook.Tab", background=[("selected", self.clr_bg)])
		self.style.map("TNotebook", background=[("selected", self.clr_bg)])
		self.style.map("TNotebook.Tab", background=[("selected", self.clr_bg)])
		if is_customst:
			self.style.map("TScrollbar", background = [("", self.clr_bg)])
	def wTk_force(self, *args):
		"Focus force"
		self.mWin.focus_force()
		self.mWin.grab_release()
	def wTk_top(self, bl=None, **kw): 
		"On top mode (is_topTk handler) (Use bl to override)"
		if bl == None: bl = self.is_topTk.get()
		kw.setdefault("win", self.mWin).attributes("-topmost", bl)
	def retitle(self, s=None): 
		""
		if not isinstance(self.titlem, int | bool): self.titlem = 1 # Is int!
		if not (0 <= self.titlem < 3): self.titlem = 1 # Is 0, 1, 2
		if not s: sx = f"ExtPad {self.version}"
		else: 
			s = str(s)
			if s[0].isdecimal(): 
				i = int(s[0]) # "2Title" -> [2, "Title"] format
				if i > 2: i = self.titlem
				s = s[1:]
			else: i = self.titlem
			sx = f"{self.titlel[i]}{s}{self.titler[i]}"
		self.mMGL["text"] = sx
		self.mWin.title(sx)
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
		"CSD/SSD mode (isCSD handler) (Use bl to override)"
		if bl == None: bl = self.isCSD.get()
		if sys.platform == "win32": self.mWin.overrideredirect(bl)
		else: self.mWin.attributes('-type', ["normal", "dock"][bl])
		if self.__dict__.get("tBar"):
			if bl: self.tBar.grid()
			else: self.tBar.grid_remove()
		self.mWin.wm_state("withdraw")
		self.mWin.wm_state("normal")
		self.mWin["takefocus"] = True
	def wTk_menubar(self, bl=None): 
		"Show menubar (is_menubar handler) (Use bl to override)"
		if bl == None: bl = self.is_menubar.get()
		if bl: self.mWin["menu"] = self.uMenu
		else:  self.mWin["menu"] = ["M", "E", "N", "U"] #Trash-data
	def wTk_point(self, event): 
		"Mouse handler on title - point"
		win_position = [int(coord) for coord in self.mWin.wm_geometry().split('+')[1:]]
		self.source.xTk, self.source.yTk = win_position[0] - event.x_root, win_position[1] - event.y_root
		self.wTk_force() # Take focus
	def wTk_move(self, event): 
		"Mouse handler on title - move"
		if self.source.Tk == "max": 
			self.withNormal()
			return
		self.mWin.wm_geometry(f"+{str(event.x_root+self.source.xTk)}+{str(event.y_root+self.source.yTk)}")
	def withNormal(self): 
		"[Normal]-button handler"
		if self.source.Tk == "normal": return
		self.iGrid(self.is_apibar, self.apiBar)
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
		"[Max]-button handler"
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
		"[Min]-button handler"
		if   not self.isCSD.get():
			self.mWin.state("icon")
			return
		if   self.source.Tk in ["min", "max"]:
			self.withNormal()
			return
		self.iGrid_raw(False, self.apiBar)
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
		"<Double-Button-1> handler"
		if   self.source.Tk in ["max", "min"]: self.withNormal()
		elif self.source.Tk == "normal": self.withMax()
	def withQuit(self): 
		"[Quit]-button handler"
		if self.mNB.tabs() != () and not self.source.future_fast_quit:
			if not tkmb.askokcancel("You sure?", "You may have unsaved changes"): return
		for i in range(len(self.mNB.tabs())): 
			if self.nClose(): return
		self.source.quit()
		# Menu
	def pop_menu(self, ev, menu, button=None): 
		"Draw any menu"
		try:
			menu.tk_popup(ev.x_root, ev.y_root, "none")
			if not button: menu.bind("<FocusOut>", lambda ev: menu.unpost())
		finally:
			menu.grab_release()
		if button: button["state"] = "!selected"
	def get_nPage(self): 
		"Simple funcion to get current-tab frame widget"
		if self.mNB.tabs() == (): return
		return self.mWin.nametowidget(self.mNB.select())
	def hBar_tip_new(self, tip: str, time=-1):
		"Add tip on Help-Bar (and queue) <time> tics"
		self.mLblQ.append([self.mLblCheck, self.mLbl["text"]])
		self.mLbl["text"] = tip
		self.mLblCheck = time
	def hBar_tip_dispose(self): 
		"Remove tip on Help-Bar (dispose queue[0])"
		if   self.mLblQ != []:
			self.mLblCheck, self.mLbl["text"] = self.mLblQ.pop(0)
		elif self.mNB.tabs() == ():
			self.mLbl["text"] = f" . . . "
			self.mLblCheck = -1
		elif self.mWin.nametowidget(self.mNB.select()).id == ["note", 0]:
			self.mLbl["text"] = f'Hello! You can sew first note tab on ExtPad {self.version}; press F1 key to take help/hints-pane'
			self.mLblCheck = -1
		else: self.mLblCheck = 0
	def nOpen(self, path=None): 
		"Open file or add new note; and create tab"
		# Input path, text
		if not path:
			path = tkfd.askopenfilename(
				title="Open file",
				filetypes=self.fform
			)
			self.wTk_force()
			if not path: return
		elif not os.path.isfile(path): return
		with open(str(path)) as nfile: text = nfile.read()
		# Controls
		ikw = dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["file", path], text=text)
		tab = NBFrame_Note(self, self.mNB, ikw=ikw, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"+{id(ikw)}')
		tab.filed()
		self.mNB.add(tab, image=self.img_mbfile, text=os.path.split(path)[-1], compound="left")
	def nSaveas(self): 
		"Save-as tab with tab.api_nsaveas funcion"
		tab = self.get_nPage()
		if not tab: return "cancel:notabs"
		method = tab.__dict__.get("api_nsaveas")
		if method: method()
		else: print("[App][nSaveas] Action undefined")
	def nSave(self): 
		"Save tab with tab.api_nsave funcion"
		tab = self.get_nPage()
		if not tab: return
		method = tab.__dict__.get("api_nsave")
		if method: method()
		else: print("[App][nSave] Action undefined")
	def nNew(self): 
		"New file tab"
		path = tkfd.asksaveasfilename(
			title="New file",
			defaultextension=".txt", 
			filetypes=self.fform
		)
		self.wTk_force()
		if not path: return
		# Controls
		ikw = dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["file", path])
		tab = NBFrame_Note(self, self.mNB, ikw=ikw, style="ghost.TFrame", name=f'file:"{path.replace(".", "%2E")}"')
		self.mNB.add(tab, image=self.img_mbfile, text=os.path.split(path)[-1], compound="left")
	def nNewnote(self): 
		"New note tab"
		ikw = dict(b3bind=lambda ev: self.pop_menu(ev, self.eMenu), fid=["note", self.notec])
		tab = NBFrame_Note(self, self.mNB, ikw=ikw, style="ghost.TFrame", name=f'note:"{self.notec}"')
		self.mNB.add(tab, image=self.img_mbnote, text=f"New{['', f' ({self.notec})'][bool(self.notec)]}", compound="left")
		self.notec += 1
	def nClose(self, **kw): 
		"Close tab with tab.api_nclose funcion"
		if self.mNB.tabs() == (): return
		tabid = kw.get("k", self.mNB.index("current"))
		tab = self.mWin.nametowidget(self.mNB.tabs()[tabid])
		try: return tab.api_nclose(tabid) # __dict__ not work
		except: pass
		if tab.id[0] == "conf":
			print(f"[app][nClose] Closing config: {tab.id[1]}")
		else: print("[app][nClose] Unknown type (fail)")
		tid = tab.ikw.get("tid")
		if   isinstance(tid, dict | type(None)): pass
		elif isinstance(tid, int): self.text_shared.rmw(tid)
		elif isinstance(tid, list | tuple): [self.text_shared.rmw(i) for i in tid]
		else: self.text_shared.rmw(int(tid))
		self.mNB.forget(tabid)
	def eUndo(self): 
		"Undo selected text"
		try: 
			self.get_nPage().text.edit_undo()
		except tk.TclError as exc: print(f"[app][eUndo] Can't undo: {exc}")
	def eRedo(self): 
		"Redo selected text"
		try: 
			self.get_nPage().text.edit_redo()
		except tk.TclError as exc: print(f"[app][eRedo] Can't redo: {exc}")
	def eCopy(self): 
		"Copy selected text"
		try: 
			nText = self.get_nPage().text
			if nText.index(tk.SEL_FIRST) == nText.index(tk.SEL_LAST): return "break:seleq"
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
		except tk.TclError as exc: print(f"[app][eCopy] Can't copy: {exc}")
	def ePaste(self): 
		"Paste selected text"
		tab = self.get_nPage()
		if not tab: return
		s = tab.text.clipboard_get()
		tab.text.insert("insert", s)
		if not tab.text.tag_ranges('sel'): return "seleq" 
		tab.text.selection_clear()
	def eCut(self): 
		"Cut selected text"
		try:
			nText = self.get_nPage().text
			if nText.index(tk.SEL_FIRST) == nText.index(tk.SEL_LAST): return "break:seleq"
			s = nText.selection_get()
			nText.clipboard_clear()
			nText.clipboard_append(s)
			nText.delete(tk.SEL_FIRST, tk.SEL_LAST)
		except tk.TclError as exc: print(f"[app][eCut] Can't cut: {exc}")
	def eFind_engene(self, s: str, w: str) -> list: 
		"Find engene"
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
	def eFind(self, word=None): 
		"Find text that selected"
		tab = self.get_nPage()
		if not tab: return
		tab.text.tag_remove("search", "1.0", "end")
		if not word:
			try: word = tab.text.selection_get()
			except tk.TclError: word = ""
		text = tab.text.get("1.0", "end")
		self.eFind_str.set(None)
		poss = self.eFind_engene(text, word)
		if poss:
			for i, f in poss:
				pos = f"{i}.{f}"
				tab.text.tag_add(f"search", pos, f"{pos} + {len(word)}c")
				tab.text.tag_configure(f"search", background=self.clr_ts, relief='raised')
		# Etc
	def altstream(self):
		self.mWin.after(100, self.altstream)
		self.mWin.minsize(*self.mWin_min())
		if self.mNB.tabs() == (): 
			self.retitle("")
			return
		tab = self.get_nPage()
		if tab.id[0] == "conf": nText = None
		else: nText = tab.text
		if self.mLblCheck == 0:
			self.mLbl["text"] = tab.api_on_hbar()
		elif self.mLblCheck > 0:
			self.mLblCheck -= 1
		if tab.id[0] in ["file", "note"]:
			if tab.id[0] == "note":
				tmp = f"New{['', f' ({tab.id[1]})'][bool(tab.id[1])]}"
			else:
				if sys.platform == "win32": tmp = tab.id[1].split("\\")[-1]
				else: tmp = tab.id[1].split("/")[-1]
			if nText.edit_modified() == True: self.mNB.tab(self.mNB.select(), text=tmp+"*")
			else: self.mNB.tab(self.mNB.select(), text=tmp.rstrip("*"))
		try: self.retitle(tab.api_on_tbar())
		except Exception as err:
			self.retitle("")

	def nExec(api, path=None): 
		"Exec module"
		if not path:
			path = tkfd.askopenfilename(title="Exec ext-on", filetypes=api.fform)
			if not path: return
		with open(path) as modfile: exec(modfile.read())

if __name__ == "__main__": 
	app = App()
