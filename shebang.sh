#!/bin/bash


jak_uzywac() {
cat 1>&2 <<EOF

./`basename $0` nazwa

	Skrypt generuje szkielety mniejszych skryptow (sam goly shebang) o zadanej nazwie,
	majac za zadanie zapobiec kazdorazowemu nudnemu klepaniu ich od zera.
	
EOF
}

juz_istnieje() {
	echo "*** $1 juz tu istnieje. Wybierz inna nazwe." 1>&2
}



if [ $# -ne 1 ]; then
	jak_uzywac
	exit 1
fi

if [ $# -gt 0 ] && ([ $1 == "-h" ] || [ $1 == "-help" ] || [ $1 == "--help" ]); then
	jak_uzywac; exit 1
fi


NAZWA=$1
if [ -a $NAZWA ]; then
	juz_istnieje $NAZWA
	exit 1
fi




echo "#!$SHELL" > $NAZWA
echo -e "\n\n" >> $NAZWA



chmod u+x $NAZWA
geany $NAZWA &
