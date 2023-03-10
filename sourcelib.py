#!/bin/python3
""" Part of extpad - Source"""
from deps import *
imgCont = 0

class Source():
	# So, source
	def __init__(self):
		self.srcWin = tk.Tk()
		self.Tk = "normal"
		self.future_tth = False # Toggle to get(1) ttkthemes - future
		self.future_fast_deftc = False # Toggle to get(1) deftc-first - future
		self.future_fast_quit = True # Toggle to fast(1) quit - future
		self.dbg = tk.BooleanVar(value=False) # App.nSel() req
		self.xTk, self.yTk, self.wrx, self.wry, self.sizeX, self.sizeY = [0, 0, 0, 0, 0, 0]
		self.ww, self.wh = [400, 300]
		global imgCont
		self.imgCont = imgCont
		self.fileforms = [("All formats", "*.*"), ("Text file", "*.txt"), ("Python file", "*.py")]
		self.tw_twst = tk.Entry(self.srcWin, name="__colorget_entry")
		self.clr_tkbg, self.clr_tw = [self.srcWin.cget('bg'), tk.Entry(self.srcWin).cget("bg")]
		self.clr_gw, self.clr_sb, self.clr_dsb, self.clr_lsb = ["ghostwhite", "steelblue", "darkslateblue", "lightsteelblue"]
		self.img_win3 = tk.PhotoImage(data=\
"""R0lGODlhEAAQAKEBAEg9i7DE3vj4/7DE3iH5BAEKAAMALAAAAAAQABAAAAIynI+pu+APEwi0WoCg
fjkAAYYgdkyfKHykYaJp2p2iGrt06bljDb3r0NL9gBsO44hcFAAAOw==""")
		self.img_win = self.Fimg("win", """#define win2_width 16
#define win2_height 16
static unsigned char win2_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x1f, 0x04, 0x20, 0xfc, 0x3f, 0x14, 0x20,
   0x14, 0x28, 0x14, 0x28, 0x14, 0x28, 0x14, 0x28, 0x14, 0x20, 0xd4, 0x2b,
   0x14, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_min = self.Fimg("min", """#define min_width 16
#define min_height 16
static unsigned char min_bits[] = {
    0x00, 0x00, 0x00, 0x00, 0xfc, 0x03, 0xfc, 0x03, 0xfc, 0x03, 0xfc, 0x03,
    0x0c, 0x3b, 0x0c, 0x3b, 0xfc, 0x3b, 0xfc, 0x3b, 0x00, 0x30, 0xc0, 0x30,
    0xc0, 0x3f, 0xc0, 0x3f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_max = self.Fimg("max", """#define max_width 16
#define max_height 16
static unsigned char max_bits[] = {
    0x00, 0x00, 0x00, 0x00, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f,
    0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30,
    0xfc, 0x3f, 0xfc, 0x3f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_run = self.Fimg("run", """#define run_width 16
#define run_height 16
static unsigned char run_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0x80, 0x01, 0x98, 0x19, 0xb8, 0x1d, 0xf0, 0x0f,
   0x60, 0x06, 0x3c, 0x3c, 0x3c, 0x3c, 0x60, 0x06, 0xf0, 0x0f, 0xb8, 0x1d,
   0x98, 0x19, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_close = self.Fimg("close", """#define close_width 16
#define close_height 16
static unsigned char close_bits[] = {
    0x00, 0x00, 0x00, 0x00, 0x0c, 0x30, 0x1c, 0x38, 0x38, 0x1c, 0x70, 0x0e,
    0xe0, 0x07, 0xc0, 0x03, 0xc0, 0x03, 0xe0, 0x07, 0x70, 0x0e, 0x38, 0x1c,
    0x1c, 0x38, 0x0c, 0x30, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_file = self.Fimg("file", """#define file_width 16
#define file_height 16
static unsigned char file_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x1f, 0x04, 0x20, 0x04, 0x20, 0xf4, 0x2f,
   0x04, 0x20, 0xf4, 0x2f, 0x04, 0x20, 0xf4, 0x2f, 0x04, 0x20, 0xf4, 0x2f,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_open = self.Fimg("open", """#define open_width 16
#define open_height 16
static unsigned char open_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x04, 0x1f, 0xfc, 0x20, 0x04, 0x20,
   0x04, 0x20, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_note = self.Fimg("note", """#define note_width 16
#define note_height 16
static unsigned char open16_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x0f, 0x04, 0x1c, 0x04, 0x3c, 0xf4, 0x3c,
   0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27, 0x04, 0x20, 0xf4, 0x27,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_save = self.Fimg("save", """#define save16_width 16
#define save16_height 16
static unsigned char save16_bits[] = {
    0x00, 0x00, 0x00, 0x00, 0xf8, 0x0f, 0x74, 0x14, 0x74, 0x24, 0x74, 0x24,
    0xf4, 0x27, 0x04, 0x20, 0x04, 0x20, 0xe4, 0x27, 0x14, 0x28, 0x14, 0x28,
    0x14, 0x28, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_saveas = self.Fimg("saveas", """#define saveas_width 16
#define saveas_height 16
static unsigned char saveas_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xfc, 0x1f, 0x3a, 0x2a, 0x3a, 0x52, 0x3a, 0x52,
   0xfa, 0x53, 0x02, 0x50, 0x02, 0x50, 0xf2, 0x53, 0x0a, 0x54, 0x0a, 0x54,
   0x0a, 0x54, 0xfc, 0x3f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.img_new = self.Fimg("new", """#define pkg_width 16
#define pkg_height 16
static unsigned char pkg_bits[] = {
   0x00, 0x00, 0x00, 0x00, 0xf8, 0x1f, 0x04, 0x20, 0xfc, 0x3f, 0x04, 0x20,
   0xfc, 0x3f, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20, 0x04, 0x20,
   0x04, 0x20, 0xf8, 0x1f, 0x00, 0x00, 0x00, 0x00 };""").fimg
		self.sbVT = tk.PhotoImage(data="""R0lGODlhEAAQAIABALDE3kaCtCH+CHNiVHJvdWdoACH5BAEKAAEALAAAAAAQABAAAAIgjI95wO28
lAKGSmTtrXx3vWXeNwbieHpp2KktWz1yqRQAOw==""")
		self.sbVH = tk.PhotoImage(data="""R0lGODlhEAAgAKEAAEaCtLDE3kaCtEaCtCH+BHNiVlQAIfkEAQoAAgAsAAAAABAAIAAAAkCUgKlo
Fw/jAwbIG6jDUVsOeWBYjVNpiik6qi0LujHMyTWN2Tl+6T0v8QWBHSJp80LOlDfmzvmDDqVF6vGw
yBoKADs=""")
		self.sbVG = tk.PhotoImage(data="""R0lGODlhCgAOAIAAAEaCtEaCtCH+BHNiVkcAIfkEAQoAAQAsAAAAAAoADgAAAhCEj5nB7f+UlLDW
iY/dLecCADs=""")
		self.sbHT = tk.PhotoImage(data="""R0lGODlhEAAQAIABALDE3kaCtCH+CHNiVHJvdWdoACH5BAEKAAEALAAAAAAQABAAAAIgjI95wO28
lAKGSmTtrXx3vWXeNwbieHpp2KktWz1yqRQAOw==""")
		self.sbHH = tk.PhotoImage(data="""R0lGODlhIAAQAKEAAEaCtLDE3kaCtEaCtCH+BHNiSEgAIfkEAQoAAgAsAAAAACAAEAAAAjOUj6mb
4A+jnE6AgLPevGPnhWIGjiZXnmqQrmbrinDszTR63XKu13yPA9YslKKxwkgqEwUAOw==""")
		self.sbHG = tk.PhotoImage(data="""R0lGODlhDgAKAIAAAEaCtEaCtCH+BHNiSEcAIfkEAQoAAQAsAAAAAA4ACgAAAhcEEoaadr2ekzSy
S3G0FTbtTVvojBiIFQA7""")
		self.sbUN = tk.PhotoImage(data="""R0lGODlhEAAQAIABAEaCtLDE3iH+BHNiVU4AIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGFO
YyV+23X6AZ/iVWDSbApCnaRoZmksw/VMW+t+FAA7""")
		self.sbUP = tk.PhotoImage(data="""R0lGODlhEAAQAIAAALDE3rDE3iH+BHNiVVAAIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGFO
YyV+23X6AZ/iVWDSbApCnaRoZmksw/VMW+t+FAA7""")
		self.sbDN = tk.PhotoImage(data="""R0lGODlhEAAQAIABAEaCtLDE3iH+BHNiRE4AIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGFO
YyUGClHaVZw4Ks0GRp/jseT5rhk8uzUcX+FeAAA7""")
		self.sbDP = tk.PhotoImage(data="""R0lGODlhEAAQAIAAALDE3rDE3iH+BHNiRFAAIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGFO
YyUGClHaVZw4Ks0GRp/jseT5rhk8uzUcX+FeAAA7""")
		self.sbLN = tk.PhotoImage(data="""R0lGODlhEAAQAIABAEaCtLDE3iH+BHNiTE4AIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGEC
47CMdPNbZYgojo1GmV2Jgl7bnnDokdbzWcqeFAA7""")
		self.sbLP = tk.PhotoImage(data="""R0lGODlhEAAQAIAAALDE3rDE3iH+BHNiTFAAIfkEAQoAAQAsAAAAABAAEAAAAiaMj3nA7byehGEC
47CMdPNbZYgojo1GmV2Jgl7bnnDokdbzWcqeFAA7""")
		self.sbRN = tk.PhotoImage(data="""R0lGODlhEAAQAIABAEaCtLDE3iH+BHNiUk4AIfkEAQoAAQAsAAAAABAAEAAAAieMj3nA7byehMGZ
CW6LT1O/VSFHWYlpIugIZuL3hukEtjLW2ZLCJwUAOw==""")
		self.sbRP = tk.PhotoImage(data="""R0lGODlhEAAQAIAAALDE3rDE3iH+BHNiUlAAIfkEAQoAAQAsAAAAABAAEAAAAieMj3nA7byehMGZ
CW6LT1O/VSFHWYlpIugIZuL3hukEtjLW2ZLCJwUAOw==""")
		self.bfg = [("active", self.clr_gw), ("", self.clr_gw)]
		self.bbg = [("active", self.clr_lsb), ("", self.clr_sb)]
		self.conf_vbar = {
			   "configure": {
				"relief": "flat",
				"highlightthickness": 0, 
				"borderwidth": 0,
				"troughborderwidth": 0,
				"background": self.clr_tw
			}, "layout": [
				("Vertical.Scrollbar.uparrow", {"side": "top", "sticky": ""}),
				("Vertical.Scrollbar.downarrow", {"side": "bottom", "sticky": ""}),
				("Vertical.Scrollbar.uparrow", {"side": "bottom", "sticky": ""}),
				("Vertical.Scrollbar.trough", {"sticky": "ns", "children": [
					("Vertical.Scrollbar.thumb", {"expand": 1, "unit": 1, "children": [
						("Vertical.Scrollbar.grip", {"sticky": ""})
					]})
				]})
			]
		}
		self.conf_hbar = {
			   "configure": {
				"relief": "flat", 
				"highlightthickness": 0, 
				"borderwidth": 0,
				"background": self.clr_tw
			}, "layout": [
				("Horizontal.Scrollbar.leftarrow", {"side": "left", "sticky": ""}),
				("Horizontal.Scrollbar.rightarrow", {"side": "right", "sticky": ""}),
				("Horizontal.Scrollbar.leftarrow", {"side": "right", "sticky": ""}),
				("Horizontal.Scrollbar.trough", {"sticky": "ew", "children": [
					("Horizontal.Scrollbar.thumb", {"expand": 1, "unit": 1, "children": [
						("Horizontal.Scrollbar.grip", {"sticky": ""})
					]})
				]})
			]
		}
		self.all_presets = {
			   "CNotebook": {
				   "configure": {
					"borderwidth": 0, 
					"tabmargins": [3, 4, 2, 0], 
					#"tabposition": "wn"
				}
			}, "CNotebook.Tab": {
				   "configure": {
					"borderwidth": 0, 
					"padding": [5, 3]
				}, "map": {
					"background": [("selected", self.clr_tw), ("", self.clr_tkbg)] 
				}
			}, "TNotebook": {
				   "configure": {
					"borderwidth": 0, 
					"tabmargins": [3, 4, 2, 0], 
					#"tabposition": "wn"
				}
			}, "TNotebook.Tab": {
				   "configure": {
					"borderwidth": 0, 
					"padding": [5, 3]
				}, "map": {
					"background": [("selected", self.clr_tw), ("", self.clr_tkbg)] 
				}
			}, "Vertical.TScrollbar": self.conf_vbar, "Horizontal.TScrollbar": self.conf_hbar
		}
		self.deftc_presets = {
			**(self.all_presets.copy()),
			   "TLabel": {
				   "map": {
					"background": [("", self.clr_tkbg)],
				}
			}, "Hotbar.TFrame": {
				   "configure": {
					"relief": "raised"
				}
			}, "Flat.TButton": {
				   "configure": {
					"padding": [4],
					"relief": "flat", 
					"highlightthickness": 0, 
				}
			}, "Togle.TButton": {
				   "configure": {
					"padding": [4],
					"relief": "raised", 
					"highlightthickness": 1, 
				}, "map": {
					"relief": [("active", "raised"), ("", "flat")], 
					"foreground": [("active", self.clr_gw), ("", self.clr_sb)], 
					"background": [("active", self.clr_lsb), ("", self.clr_tkbg)]
				}
			}, "Title.TButton": {
				   "configure": {
					"padding": [4],
					"highlightthickness": 0, 
					"borderwidth": 0,
					"font": 10
				}, "map": {
					"foreground": self.bfg, 
					"background": self.bbg
				}
			}, "TButton": {
				   "configure": {
					"padding": [3],
					"relief": "raised", 
					"highlightthickness": 1, 
					"borderwidth": 1,
					"background": self.clr_lsb
				}, "map": {
					"foreground": self.bfg, 
					"background": self.bbg
				}
			}
		}
		self.deft_presets = {
			**(self.all_presets.copy()),
			   "TLabel": {
				   "map": {
					"background": [("", self.clr_tkbg)]
				}
			}, "Flat.TButton": {
				   "configure": {
					"margins": [0],
					"padding": [3],
					"relief": "flat", 
					"highlightthickness": 0, 
					"borderwidth": 0
				}
			}, "Togle.TButton": {
				   "configure": {
					"margins": [0],
					"padding": [3],
					"relief": "raised", 
					"highlightthickness": 1, 
					"borderwidth": 1
				}, "map": {
					"relief": [("active", "raised"), ("", "flat")], 
					"foreground": [("active", self.clr_gw), ("", self.clr_sb)], 
					"background": [("active", self.clr_lsb), ("", self.clr_tkbg)]
				}
			}, "Title.TButton": {
				   "configure": {
					"margins": [0],
					"padding": [3],
					"relief": "flat", 
					"highlightthickness": 0, 
					"borderwidth": 0,
					"font": 10
				}, "map": {
					"foreground": self.bfg, 
					"background": self.bbg
				}
			}, "TButton": {
				   "configure": {
					"margins": [0],
					"padding": [3],
					"relief": "raised", 
					"highlightthickness": 1, 
					"borderwidth": 1,
					"background": self.clr_lsb
				}, "map": {
					"foreground": self.bfg, 
					"background": self.bbg
				}
			}
		}
		self._styling()

	def _tth_styling(self):
		try:
			import ttkthemes as tth
			self.srcStyle = tth.ThemedStyle()
			self.istth = True
		except ImportError:
			self.srcStyle = ttk.Style()
			self.istth = False
		
		if self.istth:
			print("[src] tth enabled")
			return 1
		else:
			print("[src] tth disabled")

	def _styling(self):
		if self.future_tth:
			if self._tth_styling(): return
		else:
			self.srcStyle = ttk.Style()
		if "deftc" not in self.srcStyle.theme_names():
			print("[src] create theme 'deftc' ... ", end="")
			self.srcStyle.theme_create("deftc", parent="clam", settings=self.deftc_presets)
			self.srcStyle.theme_use("deftc")
			self.srcStyle.element_create("Horizontal.Scrollbar.trough", "image", self.sbHT, border=2, sticky="ew")
			self.srcStyle.element_create("Horizontal.Scrollbar.thumb", "image", self.sbHH, border=1, sticky="ew")
			self.srcStyle.element_create("Horizontal.Scrollbar.grip", "image", self.sbHG)
			self.srcStyle.element_create("Vertical.Scrollbar.trough", "image", self.sbVT, border=2, sticky="ns")
			self.srcStyle.element_create("Vertical.Scrollbar.thumb", "image", self.sbVH, border=1, sticky="ns")
			self.srcStyle.element_create("Vertical.Scrollbar.grip", "image", self.sbVG)
			
			self.srcStyle.element_create("Scrollbar.uparrow", "image", self.sbUN, ("pressed", self.sbUP), sticky="")
			self.srcStyle.element_create("Scrollbar.downarrow", "image", self.sbDN, ("pressed", self.sbDP), sticky="")
			self.srcStyle.element_create("Scrollbar.leftarrow", "image", self.sbLN, ("pressed", self.sbLP), sticky="")
			self.srcStyle.element_create("Scrollbar.rightarrow", "image", self.sbRN, ("pressed", self.sbRP), sticky="")
			print("Done")
		else: print("[src] deftc done")

		if "deft" not in self.srcStyle.theme_names():
			print("[src] create theme 'deft' ... ", end="")
			self.srcStyle.theme_create("deft", parent="alt", settings=self.deft_presets)
			self.srcStyle.theme_use("deft")
			self.srcStyle.element_create("Horizontal.Scrollbar.trough", "image", self.sbHT, border=2, sticky="ew")
			self.srcStyle.element_create("Horizontal.Scrollbar.thumb", "image", self.sbHH, border=1, sticky="ew")
			self.srcStyle.element_create("Horizontal.Scrollbar.grip", "image", self.sbHG)
			self.srcStyle.element_create("Vertical.Scrollbar.trough", "image", self.sbVT, border=2, sticky="ns")
			self.srcStyle.element_create("Vertical.Scrollbar.thumb", "image", self.sbVH, border=1, sticky="ns")
			self.srcStyle.element_create("Vertical.Scrollbar.grip", "image", self.sbVG)
			
			self.srcStyle.element_create("Scrollbar.uparrow", "image", self.sbUN, ("pressed", self.sbUP), sticky="")
			self.srcStyle.element_create("Scrollbar.downarrow", "image", self.sbDN, ("pressed", self.sbDP), sticky="")
			self.srcStyle.element_create("Scrollbar.leftarrow", "image", self.sbLN, ("pressed", self.sbLP), sticky="")
			self.srcStyle.element_create("Scrollbar.rightarrow", "image", self.sbRN, ("pressed", self.sbRP), sticky="")
			print("Done")
		else: print("[src] deft done")
		if self.future_fast_deftc: self.srcStyle.theme_use("deftc")

	def clr_twx(self):
		return self.tw_twst.cget("bg")

	# Funcions
	def quit(self): self.srcWin.destroy()

	# Funcion-image (fimage, fimg)
	class Fimg():
		def __init__(main, fimgName, fimgData):
			main.fimgData = fimgData
			main.fimgName = str(fimgName)
		def fimg(main, fg, bg=None, **kw):
			from random import randint
			global imgCont
			imgCont += 1
			main.imgCont = imgCont
			name = f"bitmap:{main.fimgName}:{randint(0, 65545)}"
			img = {
				"name": name, 
				"imgtype": "bitmap", 
				"data": main.fimgData, 
				"foreground": fg
			}
			if bg: img["background"] = bg
			takename = kw.setdefault("takename", 0)
			if takename: return tk.Image(**img), name
			else: return tk.Image(**img)

if __name__ == "__main__":
	print("[slib] test: Source")
	s = Source()
	print(f"[slib] test: Source.Fimg: {s.img_save('blue')}")
	print(f"[slib] test done")
