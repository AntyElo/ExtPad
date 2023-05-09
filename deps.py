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
import getopt
functype = type(lambda: "Hello world!")
OPT = "nc:w" #Global OPTion (eXternal)
OPTX = [
	"note",
	"config:",
	"nocsd",
	"tth", "ttkthemes",
	"notth", "nottkthemes",
	#"style:",
	"deftc",
	"fquit", "fastquit"
]
