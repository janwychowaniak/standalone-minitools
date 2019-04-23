#!/bin/bash

## media: ffmpeg


jak_uzywac() {
cat 1>&2 <<EOF

./`basename $0` [NAZWA_KLIPU] [TEMPO] <OUTPUT_DIR>

    Skrypt kompresuje KLIP
    popedzajac go jednoczesnie na zadane TEMPO
    pakujac rezultat do ./, ew. do OUTPUT_DIR

    Use JWFFKLIPARGSV and JWFFKLIPARGSA env vars for
    passing additional processing parameters:
    $ export JWFFKLIPARGSV="..."
    $ export JWFFKLIPARGSA="..."

EOF
}


if [ $# -ne 2 -a $# -ne 3 ]; then
	jak_uzywac
	exit 1
fi

if [ $# -gt 0 ] && ([ "$1" == "-h" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]); then
	jak_uzywac; exit 1
fi


# ========================================================================================

# relative include from the same directory
# [https://stackoverflow.com/a/12694189]
SCRIPTDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$SCRIPTDIR" ]]; then SCRIPTDIR="$PWD"; fi
. "$SCRIPTDIR/functions.sh"

# ----------------------------------------------------------------------------------------


NAZWA_KLIPU=$1
TEMPO=$(echo "$2" | tr "," ".")

if [ $# -eq 3 ]; then
    OUTPUT_DIR=$(echo "$3")
    if ! [ -d $OUTPUT_DIR ]; then
        echo " *** $OUTPUT_DIR nie istnieje"
        exit 2
    fi
else
    OUTPUT_DIR=$(echo ".")
fi


# atempo=$(get_atempo $TEMPO)
# vtempo=$(get_vtempo $TEMPO)

nazwa_in=$(echo $NAZWA_KLIPU)
nazwa_inter=$(echo $RANDOM.avi)
nazwa_out=$(get_nazwa_out $NAZWA_KLIPU $OUTPUT_DIR)

#~ echo "atempo      = $atempo"
#~ echo "vtempo      = $vtempo"
#~ echo "nazwa_in    = $nazwa_in"
#~ echo "nazwa_inter = $nazwa_inter"
#~ echo "nazwa_out   = $nazwa_out"

FILTER_COMPLEX=$(get_filter_complex $TEMPO)

# step 1
echo "ffmpeg -i $nazwa_in $FILTER_COMPLEX -q:v 0 $JWFFKLIPARGSV -q:a 0 $JWFFKLIPARGSA $nazwa_inter ;"
# step 2
echo "ffmpeg -i $nazwa_inter -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 64k -ac 1 -sn -strict experimental $nazwa_out ;"
# cleanup
echo "rm $nazwa_inter ;"