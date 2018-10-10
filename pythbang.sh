#!/bin/bash


jak_uzywac() {
cat 1>&2 <<EOF

./`basename $0` nazwa

	Skrypt generuje szkielety skryptow Python o zadanej nazwie,
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
EXT=".py"
NAZWA_EXT=$NAZWA$EXT
if [ -a $NAZWA_EXT ]; then
	juz_istnieje $NAZWA_EXT
	exit 1
fi




echo "#!`which python`" > $NAZWA_EXT
echo -e "\n\n\n" >> $NAZWA_EXT
echo    "#~ import " >> $NAZWA_EXT
echo -e "\n\n\n" >> $NAZWA_EXT
echo    "#~ class Clazz:" >> $NAZWA_EXT
echo    "	#~ def __init__(self, _arg1, _arg2):" >> $NAZWA_EXT
echo    "	#~ def method(self, _arg1, _arg2):" >> $NAZWA_EXT
echo -e "\n\n" >> $NAZWA_EXT
echo    "#~ def function(_arg1, _arg2):" >> $NAZWA_EXT
echo -e "\n\n\n" >> $NAZWA_EXT
echo -en "if __name__ == '__main__':\n\t" >> $NAZWA_EXT



chmod u+x $NAZWA_EXT
geany $NAZWA_EXT &
