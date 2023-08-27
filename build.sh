#!/bin/sh
PYC=`which nuitka3`
test -z "$PYC" && { echo "[error] nuitka3 requited (which: \"$PYC\")"; \
exit 1; } || echo "[info] bilding extpad with $PYC"
include_modules() {
	for i in $@; do
		echo "--include-module=$i"
	done
}
case $1 in
	h|he|hel|help)
		cat << "===END OF HELP==="
$0 - Nuitka3-based build script

Usage:
help - read this note
full - compile full build (default command)
rfull - as 'full', and run
minimal - compile without pyshell.py and ttkthemes
rminimal - as 'minimal', and run
===END OF HELP===
		exit 0;;
	rmi|rmin|rmini|rminim|rminima|rminimal|run-minimal)
		nuitka3 --run `include_modules deps sourcelib widgetlib` extpad.py;;
	rf|rfu|rful|rfull|run-full)
		nuitka3 --run `include_modules deps sourcelib widgetlib pyshell ttkthemes` extpad.py;;
	m|mi|min|mini|minim|minima|minimal)
		nuitka3 `include_modules deps sourcelib widgetlib` extpad.py;;
	f|fu|ful|full|*)
		nuitka3 `include_modules deps sourcelib widgetlib pyshell ttkthemes` extpad.py;;
esac
rm -r extpad.build