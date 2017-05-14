# coding: utf-8
import requests
from pymongo import MongoClient

def twitterGetMessage(userText):

    client = MongoClient('localhost', 27017)

    #get data from mongoDB
    lastPostNum = client['test']['twitter'].find({'$text':{'$search': userText }}).count()
    if(lastPostNum == 0):
        twitterMessage = 'Can\'t find this Message,please try again!'
    else:
        cursor = client['test']['twitter'].find({'$text':{'$search': userText }})[lastPostNum-1]
        author = cursor['author']
        message = cursor['message']
        timeStamp = cursor['timeStamp']

        twitterMessage = ('Author: '+ author + '\n' +
                          '\n' +
                          message + '\n' +
                          '\n' +
                          'PostTime:' + timeStamp)
    return twitterMessage
