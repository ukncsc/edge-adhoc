import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.address import get_addresses
from adapters.certuk_adhoc.query.domain_names import get_domain_names
from adapters.certuk_adhoc.query.file_hashes import get_file_hashes
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse


REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


def generateResponse(matches_cursor, request, elapsed):
        matches = []
        for match_result in matches_cursor:
            match_result['_id']=match_result['objects']
        if request.META.get('HTTP_ACCEPT') in {'application/json', 'text/json'}:
            return JsonResponse({
                'duration': '%.2f' % elapsed.ms(),
                'matches': matches,
                'state': 'success'
            }, status=200)
        else:
            plain_text = "\n".join("%s - %s" % (address, ", ".join(ids)) for address, ids in matches.iteritems()) + "\n"
            return HttpResponse(content=plain_text, content_type='text/plain')



@csrf_exempt
def address(request):

    if not request.method == 'POST':
        return JsonResponse({}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        addresses = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_addresses(cleanse_data_list(addresses))
        generateResponse(matches_cursor, request, elapsed)
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



@csrf_exempt
def file_hashes(request):

    if not request.method == 'POST':
        return JsonResponse({'Request must be': 'POST'}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        hashes = REGEX_ADDRESS_DELIMITER.split(raw_body)
        hashes_raw = cleanse_data_list(hashes)
        hashes_upper = [x.upper() for x in hashes_raw]
        matches_cursor = get_file_hashes(hashes_upper)
        matches = []
        for match_result in matches_cursor:
            print match_result
        return JsonResponse({
            'duration': '$.2sf' %elapsed.ms(),
            'matches': matches,
            'state': 'success'
        })
    except Exception as e:
        log_error(e, 'adapter/file_hashes', 'File hash search failed')
        return JsonResponse({
            'duration': '%.2f' %elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status = 500)


def generateErrorResponse(method_name, elapsed, e):
        log_error(e, 'adapter' + method_name, method_name + ' search failed')
        return JsonResponse({
            'duration': '%.2f' %elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status = 500)

