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
