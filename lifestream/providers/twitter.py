from datetime import datetime
import dateutil
import logging
import calendar

from django.conf import settings
from lifestream.providers import utils

#
# API URLs
#

FETCH_COUNT = 200
MAX_PAGES = 16
USER_TIMELINE_URL = "http://twitter.com/statuses/user_timeline.json?count="+str(FETCH_COUNT)+"&page=%s&since_id=%s"
 
#
# Public API
#
 
log = logging.getLogger("lifestream.providers.twitter")

def update():
    since_id = _get_last_tweet_id()    
    page = 1
    tweets = []
    while True:
        more = _fetch_tweets(since_id, page)
        tweets += more
        if len(more) < FETCH_COUNT:
            break
        else:
            page += 1
            if page > MAX_PAGES:
                break
    _save_tweets(tweets)
    #last_id = tweets[0]["id"]

#
# Private junk
#

import pymongo
import lifestream.mongodb as mongodb
collection = mongodb.get_collection()

def _get_last_tweet_id():
    tweets = collection.find({
            "lifestream:source": u"twitter:user:%s" % settings.TWITTER_USERNAME}
        ).sort('id', pymongo.DESCENDING )
    if tweets.count() > 0:
        return tweets[0]["id"]
    else:
        return 1

def _fetch_tweets(since_id=1, page=1):
    log.debug("Fetching tweets... since id: %s, page: %s", (str(since_id), str(page)))
    tweets = utils.getjson(
            USER_TIMELINE_URL % (page, since_id),
            username=settings.TWITTER_USERNAME,
            password=settings.TWITTER_PASSWORD
        )
    return tweets

def _save_tweets(tweets):
    log.debug("Saving %s tweets...", str(len(tweets)))
    map(_save_tweet, tweets)

def _save_tweet(tweet):
    twitter_id = tweet["id"]
    src = u"twitter:user:%s" % settings.TWITTER_USERNAME

    # check that tweet isn't already stored
    if collection.find_one({"id":twitter_id, "lifestream:source":src}):
        log.debug("tweet (%s) already saved" % tweet["text"])
        return
    
    # save to db
    tweet["lifestream:provider"] = "twitter"
    tweet["lifestream:source"] = src
    tweet["lifestream:timestamp"] = dateutil.parser.parse(tweet["created_at"])
    tweet["lifestream:added"] = datetime.utcnow()
    
    collection.insert(tweet)
    
    