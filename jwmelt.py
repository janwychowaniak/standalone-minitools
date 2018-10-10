#!/usr/bin/python

# media


import sys

if __name__ == '__main__':

    if len(sys.argv) < 5:
        sys.stderr.write('Usage:')                                                           ; sys.stderr.flush()
        sys.stderr.write('  %s   out   mix   file1   file2   [file3   [...]]' % sys.argv[0]) ; sys.stderr.flush()
        sys.stderr.write('\n')                                                               ; sys.stderr.flush()
        sys.exit(1)

    PARAM_OUT = sys.argv[1]
    PARAM_MIX = sys.argv[2]
    FILES_LIST = sys.argv[3:]

    print
    print "## [https://superuser.com/questions/833232/create-video-with-5-images-with-fadein-out-effect-in-ffmpeg]"
    print

    print "# out =", PARAM_OUT
    print "# mix =", PARAM_MIX

    for p in FILES_LIST:
        print "# file =", p

    print
    print

    print " # [no fades]"
    print "melt -verbose -profile atsc_720p_30 \\"
    for p in FILES_LIST:
        print "%s out=%s \\" % (p, PARAM_OUT)
    print "-consumer avformat:output__atsc_720p_30.mp4 vcodec=libx264 an=1"
    print

    print " # [OR with fades]"
    print "melt -verbose -profile atsc_720p_30 \\"
    print "%s out=%s \\" % (FILES_LIST[0], PARAM_OUT)
    for p in FILES_LIST[1:]:
        print "%s out=%s -mix %s -mixer luma \\" % (p, PARAM_OUT, PARAM_MIX)
    print "-consumer avformat:output__atsc_720p_30.mp4 vcodec=libx264 an=1"
    print

    print " # [finishing (->AVI)]"
    print "ffmpeg -i output__atsc_720p_30.mp4 -q:v 0 -vf scale=960:-1 output__atsc_720p_30.avi"
    print "rm output__atsc_720p_30.mp4"

    print
