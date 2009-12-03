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
    since_id = 1
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
    last_id = tweets[0]["id"]

#
# Private junk
#


# TODO - abstract out the mongodb specific stuff
from pymongo import Connection
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "lifestream_db"
MONGODB_LS_COLLECTION = "lifestream"
if hasattr(settings, "MONGODB_HOST"):
    MONGODB_HOST = settings.MONGODB_HOST
if hasattr(settings, "MONGODB_PORT"):
    MONGODB_PORT = settings.MONGODB_PORT
if hasattr(settings, "MONGODB_DB"):
    MONGODB_DB = settings.MONGODB_DB
if hasattr(settings, "MONGODB_LIFESTREAM_COLLECTION"):
    MONGODB_LS_COLLECTION = settings.MONGODB_LS_COLLECTION
connection = Connection(MONGODB_HOST, MONGODB_PORT)
db = connection[MONGODB_DB]
collection = db[MONGODB_LS_COLLECTION]
collection.create_index("lifestream:timestamp")
collection.create_index("id")
collection.create_index("lifestream:provider")
collection.create_index("lifestream:source")

def _fetch_tweets(since_id=1, page=1):
    log.debug("Fetching tweets... since id: %s, page: %s", (since_id, page))
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
        log.debug("weet (%s) already saved" % tweet["text"])
    
    # save to db
    tweet["lifestream:provider"] = "twitter"
    tweet["lifestream:source"] = src
    tweet["lifestream:timestamp"] = dateutil.parser.parse(tweet[u"created_at"])
    tweet["lifestream:added"] = datetime.utcnow()
    
    collection.insert(tweet)
    
    