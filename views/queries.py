import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.socket_ip import partial_matches_on_ip
from adapters.certuk_adhoc.query.match_on_object_summary_value import matches_on_summary_value
from adapters.certuk_adhoc.query.file_hashes import get_file_hashes
from adapters.certuk_adhoc.query.email_address_field import matches_on_email_address_field, matches_on_email_address_from
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse

REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


def generate_matches_array(matches_cursor):
    matches = []
    for match_result in matches_cursor:
        if isinstance(match_result['_id'], list):
            list_id = " - ".join(match_result['_id'])
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
            plain_text += ("%s - %s" % (query, ", ".join(ids))) + "\n"
    return plain_text


def generate_response(request, matches, elapsed):
    if request.META.get('HTTP_ACCEPT') in {'application/json', 'text/json'}:
        return JsonResponse({
            'duration': '%.2f' % elapsed.ms(),
            'matches': matches,
            'state': 'success'
        }, status=200)
    else:
        plain_text = plain_text_response(matches)
        return HttpResponse(content=plain_text, content_type='text/plain')


def generate_error_response(type_of_search, elapsed, e):
    log_error(e, 'adapter' + type_of_search, type_of_search + ' search failed')
    return JsonResponse({
        'duration': '%.2f' % elapsed.ms(),
        'message': e.message,
        'state': 'error'
    }, status=500)


def response_from_bulk_search(request, object_type, query_function):
    if not request.method == 'POST':
        return JsonResponse({"Request must be": "POST"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        bulk_search = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = query_function(cleanse_data_list(bulk_search), object_type)
        matches = generate_matches_array(matches_cursor)
        return generate_response(request, matches, elapsed)
    except Exception as e:
        return generate_error_response(object_type, elapsed, e)

def email_address_helper(request, object_type, query_function):
    raw_body = request.body
    bulk_search = REGEX_ADDRESS_DELIMITER.split(raw_body)
    matches_cursor = query_function(cleanse_data_list(bulk_search), object_type)
    matches = generate_matches_array(matches_cursor)
    return matches

@csrf_exempt
def address(request):
    return response_from_bulk_search(request, 'AddressObjectType', matches_on_summary_value)

@csrf_exempt
def domain_names(request):
    return response_from_bulk_search(request, 'DomainNameObjectType', matches_on_summary_value)

@csrf_exempt
def file_names(request):
    return response_from_bulk_search(request, 'FileObjectType', matches_on_summary_value)

@csrf_exempt
def file_hashes(request):
    return response_from_bulk_search(request, 'FileObjectType', get_file_hashes)

@csrf_exempt
def email_subject(request):
    return response_from_bulk_search(request, 'EmailMessageObjectType', matches_on_summary_value)

@csrf_exempt
def email_address_from(request):
    return response_from_bulk_search(request,'EmailMessageObjectType', matches_on_email_address_from)

@csrf_exempt
def email_address_to(request):
    return response_from_bulk_search(request, 'to', matches_on_email_address_field)

@csrf_exempt
def email_address_cc(request):
    return response_from_bulk_search(request, 'cc', matches_on_email_address_field)

@csrf_exempt
def email_address_bcc(request):
    return response_from_bulk_search(request, 'bcc', matches_on_email_address_field)

@csrf_exempt
def email_address_all(request):
    if not request.method == 'POST':
        return JsonResponse({"Request must be": "POST"}, status=405)

    elapsed = StopWatch()
    try:
        address_from = email_address_helper(request, 'EmailMessageObjectType', matches_on_email_address_from)
        address_to = email_address_helper(request, 'to', matches_on_email_address_field)
        address_cc = email_address_helper(request, 'cc', matches_on_email_address_field)
        address_bcc = email_address_helper(request, 'bcc', matches_on_email_address_field)
        address_fields = [address_from, address_to, address_cc, address_bcc]

        def matcher(address_to_match, map_of_ids):
            for address_match in address_to_match:
                for match, ids in address_match.iteritems():
                    for id in ids:
                        map_of_ids.setdefault(match, []).append(id)

        map_ids={}
        for address_field in address_fields:
            matcher(address_field, map_ids)

        matches = []
        for address, ids in map_ids.iteritems():
            matches.append({
                address: ids
            })

        return generate_response(request, matches, elapsed)
    except Exception as e:
        return generate_error_response("All email address fields", elapsed, e)

@csrf_exempt
def uri(request):
    return response_from_bulk_search(request, 'URIObjectType', matches_on_summary_value)

@csrf_exempt
def socket_full(request):
    return response_from_bulk_search(request, 'SocketAddressObjectType', matches_on_summary_value)

@csrf_exempt
def socket_ip(request):
    return response_from_bulk_search(request, 'SocketAddressObjectType', partial_matches_on_ip)

