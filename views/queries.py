import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.query_object_type import get_object_type
from adapters.certuk_adhoc.query.file_hashes import get_file_hashes
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse

REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


def generate_matches_array(matches_cursor):
    matches = []
    for match_result in matches_cursor:
        matches.append({
            match_result['_id']: match_result['objects']
        })
    return matches

def plain_text_response(matches):
    plain_text = ""
    for x in matches:
        for query, ids in x.iteritems():
            items = plain_text + ("%s - %s" % (query, ", ".join(ids))) + "\n"
            plain_text = items
    return plain_text

def generate_response(matches, request, elapsed):
    if request.META.get('HTTP_ACCEPT') in {'application/json', 'text/json'}:
        return JsonResponse({
            'duration': '%.2f' % elapsed.ms(),
            'matches': matches,
            'state': 'success'
        }, status=200)
    else:
        plain_text = plain_text_response(matches)
        return HttpResponse(content=plain_text, content_type='text/plain')


def generate_error_response(method_name, elapsed, e):
    log_error(e, 'adapter' + method_name, method_name + ' search failed')
    return JsonResponse({
        'duration': '%.2f' % elapsed.ms(),
        'message': e.message,
        'state': 'error'
    }, status=500)


@csrf_exempt
def address(request):
    if not request.method == 'POST':
        return JsonResponse({"Request must be": "POST"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        addresses = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_object_type(cleanse_data_list(addresses), 'AddressObjectType')
        matches = generate_matches_array(matches_cursor)
        return generate_response(matches, request, elapsed)
    except Exception as e:
        return generate_error_response("address_search", elapsed, e)


@csrf_exempt
def domain_names(request):
    if not request.method == 'POST':
        return JsonResponse({"Request must be": "POST"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        names = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_object_type(cleanse_data_list(names), 'DomainNameObjectType')
        matches = generate_matches_array(matches_cursor)
        return generate_response(matches, request, elapsed)
    except Exception as e:
        return generate_error_response("domain_name", elapsed, e)

@csrf_exempt
def file_hashes(request):
    if not request.method == 'POST':
        return JsonResponse({'Request must be': 'POST'},status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        file_hashes = REGEX_ADDRESS_DELIMITER.split(raw_body)
        file_hashes_upper = [x.upper() for x in file_hashes]
        matches_cursor = get_file_hashes(cleanse_data_list(file_hashes_upper))
        matches = generate_matches_array(matches_cursor)
        return generate_response(matches, request, elapsed)
    except Exception as e:
        return generate_error_response("file_hash",elapsed,e)
