from datetime import datetime
import dateutil
import logging
import calendar

from django.conf import settings
from lifestream.providers import utils

#
# API URLs
#

JSON_URL = "http://feeds.delicious.com/v2/json/%s" % settings.DELICIOUS_USERNAME
 
#
# Public API
#
 
log = logging.getLogger("lifestream.providers.delicious")

def update():
    log.debug("Fetching delicious updates...")
    updates = utils.getjson(JSON_URL)
    _save_updates(updates)
    

#
# Private junk
#

import pymongo
import lifestream.mongodb as mongodb
collection = mongodb.get_collection()

def _save_updates(updates):
    log.debug("Saving updates...")
    map(_save_update, updates)

def _save_update(update):
    delicious_id = update["u"]
    src = u"delicious:%s" % settings.DELICIOUS_USERNAME

    # check that tweet isn't already stored
    if collection.find_one({"u":delicious_id, "lifestream:source":src}):
        log.debug("update (%s) already saved" % update["u"])
        return
    
    # save to db
    update["lifestream:provider"] = "delicious"
    update["lifestream:source"] = src
    update["lifestream:timestamp"] = utils.parsedateutc(update["dt"])
    update["lifestream:added"] = datetime.utcnow()
    
    collection.insert(update)
    
    