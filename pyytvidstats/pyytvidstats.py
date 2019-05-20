#!/usr/bin/python3

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
import os

from ConfigParser import SafeConfigParser
#TODO SafeConfigParser in python3 ??


from enum import Enum

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pprint import pprint


URL_REGEX = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
BAREID_REGEX = '[A-Za-z0-9_-]{11}'

VIDEO_EXTS = ['mkv', 'mp4', 'webm', 'avi']


class BareIDParser(object):
    '''
    Does nothing. Needed for satifying corresponding input type.
    '''

    def parse(self, _arg):
        return _arg


class VideoURLParser(object):
    '''
    Gets a video ID from YT URL
    '''

    def parse(self, _arg):
        urlParamsList = _arg.split('?')[1].split('&')
        vParam = [i for i in urlParamsList if i.startswith('v=')][0]

        return vParam.split('=')[1]


class ListURLParser(object):
    '''
    Gets a list ID from YT URL
    '''

    def parse(self, _arg):
        urlParamsList = _arg.split('?')[1].split('&')
        vParam = [i for i in urlParamsList if i.startswith('list=')][0]

        return vParam.split('=')[1]


class FilenameParser(object):
    '''
    Gets a video ID from a file name.
    !!! Hopes that the ID is the last 11 characters before the extention !!!
    '''

    def parse(self, _arg):
        return os.path.splitext(_arg)[0][-11:]



class InputType(Enum):

    BAREID = 1
    URLVIDEO = 2
    URLLIST = 3
    FILENAME = 4


PARSERS_ASSOC = {
    InputType.BAREID : BareIDParser(),
    InputType.URLVIDEO : VideoURLParser(),
    InputType.URLLIST : ListURLParser(),
    InputType.FILENAME : FilenameParser()
}



class Validator():

    def isURL(self, _string):
        return bool(re.findall(URL_REGEX, _string))


    def isBareID(self, _string):
        '''
        This check is approximate. It actually checks if something looks like ID.
        If it doesn't - it isn't. If it does - it just might be.
        '''
        return bool(re.findall(BAREID_REGEX, _string)) and len(_string) == 11


    def isFileName(self, _string):

        ext_check_cond = any(_string.lower().endswith(ext) for ext in VIDEO_EXTS)
        preceding_id_cond = self.isBareID(os.path.splitext(_string)[0][-11:])

        return ext_check_cond and preceding_id_cond



def recognizeInputType(validator, _arg):

    if validator.isURL(_arg):

        if 'v='    in _arg: return InputType.URLVIDEO
        if 'list=' in _arg: return InputType.URLLIST

    if validator.isBareID(_arg):
        return InputType.BAREID

    if validator.isFileName(_arg):
        return InputType.FILENAME

    return None


def categorize(validator, _arglist):

    association = {}

    for arg in _arglist:
        itype = recognizeInputType(validator, arg)
        if itype: association[arg] = itype 

    return association


def extractIDs(_args_assoc):
    '''
    Note: Discards ordering, brings on its own (alphabetical)
    '''

    ids = []

    for arg in _args_assoc:
        parser = PARSERS_ASSOC[_args_assoc[arg]]
        ids.append(parser.parse(arg))

    return ids



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


# TODO deprecated
def isURL(_string):
    return bool(re.findall(URL_REGEX, _string))


# TODO deprecated
def findId(_videoArg):

    if not isURL(_videoArg):
        return _videoArg 

    urlParamsList = _videoArg.split('?')[1].split('&')
    vParam = [i for i in urlParamsList if i.startswith('v=')][0]

    return vParam.split('=')[1]


# TODO deprecated
def getIdsArg(_arglist):
    
    idsList = []

    for item in _arglist:
        idsList.append(findId(item))

    return ','.join(idsList)


def formatInfo(_id, _views, _like_prc, _votes_ttl):
    
    return '%s - %s%% (%s votes / %s views)' % (_id, _like_prc, _votes_ttl, _views)


def main(_args):

    # ids_arg = getIdsArg(_vidIdStrings)
    categorized = categorize(Validator(), _args)
    extracted = extractIDs(categorized)
    ids_arg = ','.join(extracted)


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
    except HttpError as e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
        # TODO only print?
        # missing proper 4xx handling

    videos_stats = scrape(videos_list)


    info = []

    for vidstat in videos_stats:
        likes_prc , votes_ttl = likesPercent(vidstat)
        info.append(formatInfo(vidstat['id'], vidstat['viewCount'], likes_prc, votes_ttl))

    print("")
    for i in info:
        print(i)
    print("")



if __name__ == "__main__":
    main(sys.argv[1:])
