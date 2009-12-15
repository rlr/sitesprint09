"""
A management command which fetches the latest user activity
using the lifestream providers.
"""

from django.core.management.base import NoArgsCommand

from lifestream.providers import twitter, github, flickr, delicious


class Command(NoArgsCommand):
    help = "Fetch latest activity"

    def handle_noargs(self, **options):
        twitter.update()
        github.update()
        delicious.update()
        flickr.update()
        
