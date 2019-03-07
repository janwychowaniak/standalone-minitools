#!/usr/bin/python

# deps:
#   pip install --upgrade google-api-python-client
# 
# resources:
#   https://developers.google.com/youtube/v3/getting-started
#   https://developers.google.com/youtube/v3/docs/videos
#   https://github.com/youtube/api-samples/tree/master/python
# 
# examples:
#   https://github.com/youtube/api-samples/blob/master/python/search.py
#   https://github.com/youtube/api-samples/blob/master/python/like_video.py
#   https://github.com/youtube/api-samples/blob/master/python/update_video.py

import argparse
import re
import sys

from ConfigParser import SafeConfigParser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pprint import pprint


URL_REGEX = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'


def scrape(_videoInfo):
    '''
    Digs video id, viewCount, likeCount and dislikeCount and discards the rest.
    '''

    items = _videoInfo['items']
    output = []

    for item in items:

        itemStats = item['statistics']

        portion = {
            u'id': item['id'],
            u'viewCount': int(itemStats['viewCount']),
            u'likeCount': int(itemStats['likeCount']),
            u'dislikeCount': int(itemStats['dislikeCount'])
        }

        output.append(portion)

    return output


def likesPercent(_arg):

    likes = _arg['likeCount']
    dislikes = _arg['dislikeCount']
    votesTotal = likes + dislikes

    likes_prc = likes * 100 // votesTotal

    return (likes_prc, votesTotal)


def isURL(_string):
    return bool(re.findall(URL_REGEX, _string))


def findId(_videoArg):

    if not isURL(_videoArg):
        return _videoArg 

    urlParamsList = _videoArg.split('?')[1].split('&')
    vParam = [i for i in urlParamsList if i.startswith('v=')][0]

    return vParam.split('=')[1]


def getIdsArg(_arglist):
    
    idsList = []

    for item in _arglist:
        idsList.append(findId(item))

    return ','.join(idsList)


def formatInfo(_id, _views, _like_prc, _votes_ttl):
    
    return '%s - %s%% (%s votes / %s views)' % (_id, _like_prc, _votes_ttl, _views)


def main(_vidIdStrings):

    ids_arg = getIdsArg(_vidIdStrings)


    config = SafeConfigParser()
    config.read('config.ini')
    config_dict = {}
    config_dict["developer_key"] = config.get('main', 'developer_key')

    DEVELOPER_KEY = config_dict["developer_key"]
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'


    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    try:
        videos_list = youtube.videos().list(id=ids_arg, part='statistics').execute()
    except HttpError, e:
        print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)

    videos_stats = scrape(videos_list)


    info = []

    for vidstat in videos_stats:
        likes_prc , votes_ttl = likesPercent(vidstat)
        info.append(formatInfo(vidstat['id'], vidstat['viewCount'], likes_prc, votes_ttl))

    for i in info:
        print i



if __name__ == "__main__":
    main(sys.argv[1:])
