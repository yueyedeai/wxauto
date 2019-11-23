#!usr/bin/env python
# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2019/9/28
"""
"""
import os
import time
import random
import json
import itchat
# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
from tuling import get_response

from utils import log

qalogger = log('qa')
msglogger = log('msg')
logger = log('log')

DOWNLOAD_DIR = '../downloads'
EMOJI_DIR = 'emojis'
EMOJI_DIR2 = 'emojis2'

for name in {'Picture', 'Recording', 'Attachment', 'Video'}:
    os.makedirs(os.path.join(DOWNLOAD_DIR, name), exist_ok=True)

MSGTYPES = ['Text'] + ['Picture', 'Recording', 'Attachment', 'Video'] + ['Map', 'Card', 'Note', 'Sharing']


def timesleep(text="1234567890", rate=0.5):
    time.sleep(len(text) * rate)


def emojichoice():
    d, e, e2 = DOWNLOAD_DIR, EMOJI_DIR, EMOJI_DIR2
    dirs = [d, d, e, e2, e2, e2, e2, e2, e2, e2]
    emoji_dir = random.choice(dirs)
    names = [w for w in os.listdir(emoji_dir) if w.endswith((".png", ".jpg"))]
    name = random.choice(names)
    emoji_path = os.path.join(emoji_dir, name)
    return emoji_path


def sendemoji(msg):
    path = emojichoice()
    logger.info('Send Picture: {}'.format(path))
    timesleep(rate=random.random() + 0.2)
    itchat.send(r'@img@{}'.format(path), msg['FromUserName'])


def sendfile(msg):
    path = r'E:\lab\wxauto\data\audios\000001.wav'
    itchat.send(r'@fil@{}'.format(path), msg['FromUserName'])


def msgdownload(msg):
    if msg['Type'] in {'Picture', 'Recording', 'Attachment', 'Video'}:
        path = os.path.join(DOWNLOAD_DIR, msg['Type'], msg.fileName)
        logger.info('Download {}: {}'.format(msg['Type'], path))
        msg.download(path)


def atreply(msg):
    if msg.isAt:
        out = get_response(msg['Text'])
        qalogger.info(json.dumps(dict(question=msg['Text'], answer=out), ensure_ascii=False))
        if out:
            timesleep(out, rate=random.random() + 0.5)
            text = '@%s %s' % (msg.actualNickName, out)
            msg.user.send(text)
            logger.info('Send Text: {}'.format(text))
        else:
            sendemoji(msg)


def normalreply(msg):
    if msg['Type'] == 'Text':
        if random.choice([0, 0, 0, 0, 1]):
            sendemoji(msg)
        out = get_response(msg['Text'])
        qalogger.info(json.dumps(dict(question=msg['Text'], answer=out), ensure_ascii=False))
        if out:
            logger.info('Send Text: {}'.format(out))
            timesleep(out, rate=random.random() + 0.5)
            return out
        else:
            sendemoji(msg)
    else:
        sendemoji(msg)


@itchat.msg_register(MSGTYPES, isGroupChat=False)
def one_reply(msg):
    msglogger.info(msg)
    msgdownload(msg)
    out = normalreply(msg)
    return out


# @itchat.msg_register(MSGTYPES, isGroupChat=True)
def group_reply(msg):
    msglogger.info(msg)
    msgdownload(msg)
    if msg.isAt:
        atreply(msg)
    else:
        if random.choice([0, 0, 0, 0, 1]):
            out = normalreply(msg)
            return out


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    out = '土豪，交个朋友呗！'
    timesleep(out, rate=random.random())
    itchat.send_msg(out, msg['RecommendInfo']['UserName'])


if __name__ == "__main__":
    from datetime import datetime

    itchat.auto_login()  # (hotReload=False, enableCmdQR=2)  # enableCmdQR=2
    itchat.send('来来来，现在时间是：{}！'.format(str(datetime.now())), toUserName='filehelper')
    itchat.run()
