#!/bin/bash

## media: ffmpeg


usage() {
cat 1>&2 <<EOF

./`basename $0` [CLIP_NAME] [TEMPO] <OUTPUT_DIR>

    The script encodes the CLIP file, changing its tempo by the TEMPO factor
    and putting the results to the current directory (./, or optionally to OUTPUT_DIR)

    Use JWFFKLIPARGSV and JWFFKLIPARGSA env vars for
    passing additional processing parameters:
    $ export JWFFKLIPARGSV="..."
    $ export JWFFKLIPARGSA="..."

EOF
}


if [ $# -ne 2 -a $# -ne 3 ]; then
	usage
	exit 1
fi

if [ $# -gt 0 ] && ([ "$1" == "-h" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]); then
	usage; exit 1
fi


# ========================================================================================

# relative include from the same directory
# [https://stackoverflow.com/a/12694189]
SCRIPTDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$SCRIPTDIR" ]]; then SCRIPTDIR="$PWD"; fi
. "$SCRIPTDIR/functions.sh"

# ----------------------------------------------------------------------------------------


CLIP_NAME=$1
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

name_in=$(echo $CLIP_NAME)
name_inter=$(echo $RANDOM.avi)
name_out=$(get_nazwa_out $CLIP_NAME $OUTPUT_DIR)

#~ echo "atempo     = $atempo"
#~ echo "vtempo     = $vtempo"
#~ echo "name_in    = $name_in"
#~ echo "name_inter = $name_inter"
#~ echo "name_out   = $name_out"

FILTER_COMPLEX=$(get_filter_complex $TEMPO)

# step 1
echo "ffmpeg -i $name_in $FILTER_COMPLEX -q:v 0 $JWFFKLIPARGSV -q:a 0 $JWFFKLIPARGSA $name_inter ;"
# step 2
echo "ffmpeg -i $name_inter -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 64k -ac 1 -sn -strict experimental $name_out ;"
# cleanup
echo "rm $name_inter ;"
