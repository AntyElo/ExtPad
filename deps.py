#!/bin/python3
#import time
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd
import tkinter.messagebox as tkmb
import tkinter.colorchooser as tkcc
import getopt #main
import asyncio #main
functype_custom = type(lambda: "Hello world!")
functype_builtin = type(print)
functype = functype_custom | functype_builtin
VERBOSE=True
OPT = "hnc:wd" #Global OPTion (eXternal)
OPTX = [
	"help-py", "help"
	"note",
	"config:",
	"nocsd",
	"tth", "ttkthemes",
	"notth", "nottkthemes",
	#"style:",
	"deftc",
	"fquit", "fastquit"
]
def name4argv(argv): return f"{argv[0]}.".split(".")[0]
def deps_test(): print(\
f"""[deps] Test begin: [<type> ->] <name> - <return> (<correct>)
├─┬──isinstance 
│ ├─┬──print
│ │ ├────func '{functype}' - {isinstance(print, functype)} (True)
│ │ ├────custom '{functype_custom}' - {isinstance(print, functype_custom)} (False)
│ │ └────built-in '{functype_builtin}' - {isinstance(print, functype_builtin)} (True)
│ └─┬──lambda
│   ├────func '{functype}' - {isinstance(lambda: "LOL", functype)} (True)
│   ├────custom '{functype_custom}' - {isinstance(lambda: "LOL", functype_custom)} (True)
│   └────built-in '{functype_builtin}' - {isinstance(lambda: "LOL", functype_builtin)} (False)
└──[deps] end""")
if __name__ == "__main__": deps_test()
