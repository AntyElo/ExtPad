#!/bin/python3
""" extpad-hg random mod"""

def main(self):
	"""Main method"""
	if self.vkw["build"] < 2:
		return
	self.mNB.bind("<Enter>", lambda ev: self.nClose())

if __name__ == "__main__":
	try:
		api
		v = api
	except NameError:
		print("run ExtPad >=5 before")
		exit()
	main(v)
