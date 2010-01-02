from datetime import datetime
import dateutil
import logging
import calendar

from django.conf import settings
from lifestream.providers import utils

#
# API URLs
#

JSON_URL = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=" + \
    settings.FLICKR_APIKEY + \
    "&user_id=" + settings.FLICKR_USERID + \
    "&tags=" + settings.FLICKR_TAGS + \
    "&extras=date_upload%2Cdate_taken%2Cgeo%2Curl_s&format=json&nojsoncallback=1"
 
#
# Public API
#
 
log = logging.getLogger("lifestream.providers.flickr")

def update():
    log.debug("Fetching flickr photos...")
    json =  utils.getjson(JSON_URL)
    if json.has_key('photos') and json["photos"].has_key('photo'):
        photos = json["photos"]["photo"]
        _save_pics(photos)
    

#
# Private junk
#

import pymongo
import lifestream.mongodb as mongodb
collection = mongodb.get_collection()

def _save_pics(photos):
    log.debug("Saving photos...")
    map(_save_pic, photos)

def _save_pic(photo):
    flickr_id = photo["id"]
    src = u"flickr:%s:%s" % (settings.FLICKR_USERID, settings.FLICKR_TAGS)

    # check that photo isn't already stored
    if collection.find_one({"id":flickr_id, "lifestream:source":src}):
        log.debug("photo (%s) already saved" % photo["title"])
        return
    
    # save to db
    photo["lifestream:provider"] = "flickr"
    photo["lifestream:source"] = src
    photo["lifestream:timestamp"] = utils.local_to_utc_datetime(utils.parsedate(photo["datetaken"]))
    photo["lifestream:added"] = datetime.utcnow()
    
    collection.insert(photo)
    
    