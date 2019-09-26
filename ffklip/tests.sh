
# shunit2

. ./functions.sh

test_get_atempo ()
{
    assertEquals  $(get_atempo 1)  1
    assertEquals  $(get_atempo 2)  2
}


test_get_vtempo ()
{
    assertEquals  $(get_vtempo   1)  1.0
    assertEquals  $(get_vtempo 0.5)  2.0
    assertEquals  $(get_vtempo   2)  0.5
}


test_get_nazwa_out ()
{
    assertEquals  $(get_nazwa_out input.avi .)     "./input-crf.mp4"
    assertEquals  $(get_nazwa_out input.mp4 .)     "./input-crf.mp4"
    assertEquals  $(get_nazwa_out input.mp4 dest)  "dest/input-crf.mp4"
    assertEquals  $(get_nazwa_out input.avi dest)  "dest/input-crf.mp4"
}


test_get_filter_downscale ()
{
    assertEquals  "$(get_filter_downscale 1280)"     "-filter:v \"scale='min(1280,iw)':-1\""
    assertEquals  "$(get_filter_downscale 6400)"     "-filter:v \"scale='min(6400,iw)':-1\""
}

# test_get_filter_complex ()
# {
    # TODO: fix the """"""""""""
    # assertEquals  $(get_filter_complex 1.25)  '-filter_complex "[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]" -map "[v]" -map "[a]"'
    # assertEquals  $(get_filter_complex 1.6)   "-filter_complex \"[0:v]setpts=0.625*PTS[v];[0:a]atempo=1.6[a]\" -map \"[v]\" -map \"[a]\""
    # assertEquals  $(get_filter_complex 2)     "-filter_complex \"[0:v]setpts=0.5*PTS[v];[0:a]atempo=2[a]\" -map \"[v]\" -map \"[a]\""
# }
