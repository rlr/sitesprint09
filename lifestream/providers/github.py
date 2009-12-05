from datetime import datetime
import dateutil
import logging

from django.conf import settings
from django.utils.encoding import smart_unicode

from lifestream.providers import utils

#
# API URLs
#

ATOM_URL = "https://github.com/%s.private.actor.atom?token=%s" % \
    (settings.GITHUB_USERNAME, settings.GITHUB_TOKEN)

#
# Public API
#
 
log = logging.getLogger("lifestream.providers.github")

def update():
    import feedparser
    d = feedparser.parse(ATOM_URL)
    
    for entry in map(dict, d['entries']):
        update = {
            'id': smart_unicode(entry['id']),
            'title': smart_unicode(entry['title']),
            'link': smart_unicode(entry['link']),
            'content': smart_unicode(entry['content'][0]['value']),
            'published': smart_unicode(entry['published']),
            'author': smart_unicode(entry['author'])
        }
        _save_update(update)


#
# Private junk
#

import lifestream.mongodb as mongodb
collection = mongodb.get_collection()

def _save_update(update):
    github_id = update["id"]
    src = u"github:user:%s" % settings.GITHUB_USERNAME

    # check that update isn't already stored
    if collection.find_one({"id":github_id, "lifestream:source":src}):
        log.debug("github update (%s) already saved" % update["title"])
        return
    
    # save to db
    update["lifestream:provider"] = "github"
    update["lifestream:source"] = src
    update["lifestream:timestamp"] = utils.parsedateutc(update['published'])
    update["lifestream:added"] = datetime.utcnow()
    
    collection.insert(update)