
from django.conf.urls import patterns, url

search_urls = [
    (r'^address/$', 'queries.address', None),
    (r'^domain_names/$', 'queries.domain_names',None),
    (r'^file_hashes/$','queries.file_hashes',None),
    (r'^file_names/$', 'queries.file_names', None),
    (r'^email/subject/$', 'queries.email_subject', None),
    (r'^email/address/from/$', 'queries.email_address_from', None),
    (r'^email/address/to/$', 'queries.email_address_to', None),
    (r'^email/address/cc/$', 'queries.email_address_cc', None),
    (r'^email/address/bcc/$', 'queries.email_address_bcc', None),
    (r'^email/address/$', 'queries.email_address_all', None),
    (r'^uri/$', 'queries.uri', None),
    (r'^socket/$', 'queries.socket_full', None),
    (r'^socket/ip/$', 'queries.socket_partial_on_ip', None)
]

search_url_patterns = [url(item[0], item[1], name=item[2]) for item in search_urls]

urlpatterns = patterns('adapters.certuk_adhoc.views', *search_url_patterns)

navitems = []
