import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.address import get_matches
from adapters.certuk_adhoc.common.logger import log_error

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse


REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


@csrf_exempt
def search(request):
    def cleanse_address_list(raw_address_list):
        clean_address_list = []
        found_addresses = set()
        for raw_address in raw_address_list:
            if raw_address and (not raw_address.isspace()):
                clean_address = raw_address.strip()
                if clean_address not in found_addresses:
                    found_addresses.add(clean_address)
                    clean_address_list.append(clean_address)
        return clean_address_list

    if not request.method == 'POST':
        return JsonResponse({}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        addresses = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_matches(cleanse_address_list(addresses))
        matches = {}
        for match_result in matches_cursor:
            address = match_result['_id']
            matches[address] = match_result['objects']
        if request.META.get('HTTP_ACCEPT') in {'application/json', 'text/json'}:
            return JsonResponse({
                'duration': '%.2f' % elapsed.ms(),
                'matches': matches,
                'state': 'success'
            }, status=200)
        else:
            plain_text = "\n".join("%s - %s" % (address, ", ".join(ids)) for address, ids in matches.iteritems()) + "\n"
            return HttpResponse(content=plain_text, content_type='text/plain')
    except Exception as e:
        log_error(e, 'adapters/address_search', 'Bulk address search failed')
        return JsonResponse({
            'duration': '%.2f' % elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status=500)
