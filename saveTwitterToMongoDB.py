import tweepy
import os, sys
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
from pymongo import MongoClient
from http.client import IncompleteRead

consumer_key = "yourkey"
consumer_secret = "yourkey"
access_token = "yourkey"
access_token_secret = "yourkey"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)



languages_option = ['en']
track_keywords = ['Taiwan', 'Taiwan Straits', 'Xi Jinping', 'finance in Taiwan', 'banking in Taiwan', 'Taiwan Economy',
                  'Taiwanese Economy', 'TWSE', 'TAIEX', 'Tsai Ing-Wen']
follow_users_ids = ['759251', '20402945', '2768501', '15012486', '1367531', '34713362']
# @cnn => 759251
# @cnbc => 20402945
# @abcnews => 2768501
# @cbsnews => 15012486
# @foxnews => 1367531
# @business => 34713362



class TweetStreamListener(StreamListener):
    def on_data(self, data):
        #if  not decoded[`text`].startswith('RT'):
        try:
            dict_data = json.loads(data)

            author = dict_data["user"]["screen_name"]
            timestamp = datetime.strptime(dict_data["created_at"].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y").isoformat(' ')
            message = dict_data["text"]

            print(author)
            print(timestamp)
            print(message)



            #save message to MongoDB
            client = MongoClient('localhost', 27017)
            db = client.test
            collection = db.twitter

            client['test']['twitter'].insert({'author':author,'timeStamp':timestamp,'message':message})

            #con = lite.connect('test.sqlite')
            #cur = con.cursor()
            #cur.execute('insert into twitter(timestamp, message) values(?, ?)', [timestamp, message])
            # cur.execute('insert into twitter(timestamp, author, message) values(?, ?, ?)', [timestamp, author, message])
            #con.commit()
            #con.close()

        except:
            print ("processing exception")

        return True

    # on failure
    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    listener = TweetStreamListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    while True:
        try:
            stream = Stream(auth, listener)
            stream.filter(track= track_keywords, languages = languages_option)
            # stream.filter(track = ['Jennifer Lopez'], languages = ['en'])
            # stream.filter(follow = follow_users_ids, languages = ['en'])

        except IncompleteRead:
            pass
        except KeyboardInterrupt:
            stream.disconnect()
            break
