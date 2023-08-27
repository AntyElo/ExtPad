#!/bin/sh
USEDHELP=
PYC=`which nuitka3`
test -z "$PYC" && { echo "[error] nuitka3 requited (which: \"$PYC\")"; \
exit 1; } || echo "[info] bilding extpad with $PYC"
case $1 in
	h|he|hel|help)
		echo "$0 - Nuitka3-based build script"; USEDHELP=y;;
	r|ru|run)
		nuitka3 --run --include-module=deps --include-module=sourcelib \
		--include-module=widgetlib --include-module=pyshell extpad.py;;
	m|mi|min|mini|minim|minima|minimal)
		nuitka3 --include-module=deps --include-module=sourcelib \
		--include-module=widgetlib extpad.py;;
	f|fu|ful|full|*)
		nuitka3 --include-module=deps --include-module=sourcelib \
		--include-module=widgetlib --include-module=pyshell extpad.py;;
esac
if [ -z "$USEDHELP" ]; then
	rm -r extpad.build
fi
