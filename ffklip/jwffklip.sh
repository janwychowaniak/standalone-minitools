#!/bin/bash

## media: ffmpeg


usage() {
cat 1>&2 <<EOF

./`basename $0` [CLIP_NAME] [TEMPO] [OUTPUT_DIR] <HDIM_LIMIT>

    The script encodes the CLIP file, changing its tempo by the TEMPO factor
    and putting the results to OUTPUT_DIR

    Use JWFFKLIPARGSV and JWFFKLIPARGSA env vars for
    passing additional processing parameters:
    $ export JWFFKLIPARGSV="..."
    $ export JWFFKLIPARGSA="..."

EOF
}


# is ffprobe installed?
hash ffprobe 2> /dev/null
if [ $? -ne 0 ]; then
    echo " *** ffprobe (ffmpeg) required" >&2
    exit 2
fi


if [ $# -ne 3 -a $# -ne 4 ]; then
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

# get horizontal dimension
get_hdim () {
    echo $(ffprobe -v quiet -print_format csv -show_streams -select_streams v $1 | awk -F "," '{print $10}')
}

# ----------------------------------------------------------------------------------------

CLIP_NAME=$1
TEMPO=$(echo "$2" | tr "," ".")
OUTPUT_DIR=$(echo "$3")
if [ $# -eq 4 ]; then HDIM_LIMIT=$(echo "$4"); fi

HDIM=$(get_hdim $CLIP_NAME)

# atempo=$(get_atempo $TEMPO)
# vtempo=$(get_vtempo $TEMPO)

name_in=$(echo $CLIP_NAME)
name_inter1=$(echo $RANDOM.avi)
name_inter2=$(echo $RANDOM.avi)
name_out=$(get_nazwa_out $CLIP_NAME $OUTPUT_DIR)

#~ echo "atempo      = $atempo"
#~ echo "vtempo      = $vtempo"
#~ echo "name_in     = $name_in"
#~ echo "name_inter1 = $name_inter1"
#~ echo "name_out    = $name_out"

FILTER_DOWNSCALE=$(get_filter_downscale $HDIM_LIMIT)
FILTER_COMPLEX=$(get_filter_complex $TEMPO)

# step 1
echo "ffmpeg -i $name_in $FILTER_COMPLEX -q:v 0 $JWFFKLIPARGSV -q:a 0 $JWFFKLIPARGSA $name_inter1 ;"
# step 2
echo "ffmpeg -i $name_inter1 -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 64k -ac 1 -sn -strict experimental $name_out ;"
# cleanup
echo "rm $name_inter1 ;"
