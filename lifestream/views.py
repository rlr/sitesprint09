from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import pymongo
import lifestream.mongodb as mongodb

PAGE_SIZE = 50

def activity_list(request, page=1, template='lifestream/activity_list.html', **kwargs):
    collection = mongodb.get_collection()
    object_list = collection.find().sort('lifestream:timestamp', pymongo.DESCENDING ).limit(PAGE_SIZE).skip((page-1)*PAGE_SIZE)
    return render_to_response(
            template,
            {
                'object_list': list(object_list)
            },
            context_instance=RequestContext(request),
        )