
from django.conf.urls import patterns, url

search_urls = [
    (r'^address/$', 'address.search', None),
]

search_url_patterns = [url(item[0], item[1], name=item[2]) for item in search_urls]

urlpatterns = patterns('adapters.certuk_adhoc.views', *search_url_patterns)

navitems = []