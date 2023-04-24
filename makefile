
install: package
	mv out/cal.py ~/Scripts/cal.py
	chmod u+x ~/Scripts/cal.py

dirs:
	mkdir -p out

package: dirs
	cd src && zip ../out/cal.zip *.py 
	echo '#!/usr/bin/env python3' | cat - out/cal.zip > out/cal.py

