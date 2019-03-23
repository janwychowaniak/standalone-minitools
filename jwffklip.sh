#!/bin/bash

## media: ffmpeg


jak_uzywac() {
cat 1>&2 <<EOF

./`basename $0` [NAZWA_KLIPU] [TEMPO] <OUTPUT_DIR>

    Skrypt kompresuje KLIP
    popedzajac go jednoczesnie na zadane TEMPO
    pakujac rezultat do ./, ew. do OUTPUT_DIR

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

get_atempo () {
    local generaltempo=$(echo $1)
    local atempo=$(echo $generaltempo)
    echo "$atempo"
}

get_vtempo () {
    local generaltempo=$(echo $1)
    local vtempo=`python -c "import sys; INPUT=float(sys.argv[1]); print round(1/INPUT,5)" $generaltempo`
    echo "$vtempo"
}

get_nazwa_out () {
    local nazwa_in=$(echo $1)
    local output_dir=$(echo $2)
    local filename=$(basename "$nazwa_in")
    local filenamecore="${filename%.*}"
    echo "$output_dir/$filenamecore-crf.mp4"
}

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


atempo=$(get_atempo $TEMPO)
vtempo=$(get_vtempo $TEMPO)

nazwa_in=$(echo $NAZWA_KLIPU)
nazwa_inter=$(echo $$.avi)
nazwa_out=$(get_nazwa_out $NAZWA_KLIPU $OUTPUT_DIR)

#~ echo "atempo      = $atempo"
#~ echo "vtempo      = $vtempo"
#~ echo "nazwa_in    = $nazwa_in"
#~ echo "nazwa_inter = $nazwa_inter"
#~ echo "nazwa_out   = $nazwa_out"


# step 1
echo -n "step1: $nazwa_in -> $nazwa_inter ... "
ffmpeg -loglevel error -i $nazwa_in -filter_complex "[0:v]setpts=$vtempo*PTS[v];[0:a]atempo=$atempo[a]" -map "[v]" -map "[a]" -q:v 0 -q:a 0 $nazwa_inter
echo "done"
sleep 1
# step 2
echo -n "step2: $nazwa_inter -> $nazwa_out ... "
ffmpeg -loglevel error -i $nazwa_inter -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 64k -ac 1 -sn -strict experimental $nazwa_out
echo "done"
# cleanup
rm $nazwa_inter
