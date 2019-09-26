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

get_nazwa_out () {   # get_nazwa_out $NAZWA_KLIPU $OUTPUT_DIR
    local nazwa_in=$(echo $1)
    local output_dir=$(echo $2)
    local filename=$(basename "$nazwa_in")
    local filenamecore="${filename%.*}"
    echo "$output_dir/$filenamecore-crf.mp4"
}

get_filter_complex ()
{
    local generaltempo=$1
    local atempo=$(get_atempo $generaltempo)
    local vtempo=$(get_vtempo $generaltempo)
    echo "-filter_complex \"[0:v]setpts=$vtempo*PTS[v];[0:a]atempo=$atempo[a]\" -map \"[v]\" -map \"[a]\""
}

get_filter_downscale ()
{
    local hlimit=$1
    echo "-filter:v \"scale='min($hlimit,iw)':-1\""
}
