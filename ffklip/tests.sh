
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