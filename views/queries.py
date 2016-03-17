import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.address import get_addresses
from adapters.certuk_adhoc.query.domain_names import get_domain_names
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse


REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


@csrf_exempt
def address(request):

    if not request.method == 'POST':
        return JsonResponse({}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        addresses = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_addresses(cleanse_data_list(addresses))
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


@csrf_exempt
def domain_names(request):

    if not request.method == 'POST':
        return JsonResponse({"Request must be post":"Post"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        names = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_domain_names(cleanse_data_list(names))
        matches = []
        for match_result in matches_cursor:
            matches.append({
                match_result['_id']: match_result['objects']
            })
        return JsonResponse({
            'duration': '%.2f' %elapsed.ms(),
            'matches': matches,
            'state': 'success'
        }, status = 200)
    except Exception as e:
        log_error(e, 'adapter/domain_names', 'Domain name search failed')
        return JsonResponse({
            'duration': '%.2f' %elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status = 500)

