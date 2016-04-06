import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.query_object_type import get_object_type
from adapters.certuk_adhoc.query.file_hashes import get_file_hashes_xsi, get_file_hashes_no_xsi
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse

REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


def group_matches_array(xsi, no_xsi):
    matches = []
    hashes = {}
    for hash_ in xsi:
        id = hash_['_id']
        if id in hashes.keys():
            for values in hash_['objects']:
                hashes[id].append(values)
        else:
            hashes[id] = hash_['objects']
    matches.append(hashes)
    return matches

def generate_matches_array(matches_cursor):
    matches = []
    for match_result in matches_cursor:
        if isinstance(match_result['_id'], list):
            list_id = ""
            for match in match_result['_id']:
                list_id += match
                list_id += " - "
            list_id = list_id[0:-3]
            matches.append({
                list_id: match_result['objects']
            })
        else:
            matches.append({
                match_result['_id']: match_result['objects']
            })
    return matches

def plain_text_response(matches):
    plain_text = ""
    for file_info in matches:
        for query, ids in file_info.iteritems():
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
        matches_cursor_xsi = get_file_hashes_xsi(cleanse_data_list(file_hashes))
        matches_cursor_no_xsi = get_file_hashes_no_xsi(cleanse_data_list(file_hashes))
        matches_xsi = generate_matches_array(matches_cursor_xsi)
        matches_no_xsi = generate_matches_array(matches_cursor_no_xsi)
        # group_matches = group_matches_array(matches_xsi, matches_no_xsi)
        return generate_response(matches_no_xsi, request, elapsed)
    except Exception as e:
        return generate_error_response("file_hash", elapsed, e)
