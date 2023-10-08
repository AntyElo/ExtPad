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
	deps)
		nuitka3 `include_modules sourcelib widgetlib $@` extpad.py;;
	rmi|rmin|rmini|rminim|rminima|rminimal|run-minimal)
		nuitka3 --run `include_modules deps sourcelib widgetlib` extpad.py;;
	rf|rfu|rful|rfull|run-full)
		nuitka3 --run `include_modules deps sourcelib widgetlib pyshell ttkthemes` extpad.py;;
	m|mi|min|mini|minim|minima|minimal)
		nuitka3 `include_modules deps sourcelib widgetlib` extpad.py;;
	f|fu|ful|full)
		nuitka3 `include_modules deps sourcelib widgetlib pyshell ttkthemes` extpad.py;;
	h|he|hel|help|*)
#==HELP SOF===
cat << "===HELP EOF==="
$0 - Nuitka3-based build script

Usage:
help <subject> - read this note, or <subject>
full - compile full build (default command)
rfull, run - as 'full', and run
minimal - compile without pyshell.py and ttkthemes
rminimal - as 'minimal', and run
deps <list> - compile with <list>
===HELP EOF===
		exit 0;;
esac
rm -r extpad.build
