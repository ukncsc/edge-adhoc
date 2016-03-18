import re

from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.address import get_addresses
from adapters.certuk_adhoc.query.domain_names import get_domain_names
from adapters.certuk_adhoc.common.logger import log_error
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

from edge.tools import StopWatch
from django.http.response import HttpResponse, JsonResponse


REGEX_ADDRESS_DELIMITER = re.compile("[\n,]")


def generate_response(matches_cursor, request, elapsed):
        matches = []
        for match_result in matches_cursor:
            matches.append({
                match_result['_id']: match_result['objects']
            })
        if request.META.get('HTTP_ACCEPT') in {'application/json', 'text/json'}:
            return JsonResponse({
                'duration': '%.2f' % elapsed.ms(),
                'matches': matches,
                'state': 'success'
            }, status=200)
        else:
            plain_text = ""
            for x in matches:
                for query,ids in x.iteritems():
                    items = plain_text + ("%s - %s" % (query, ", ".join(ids)) ) + "\n"
                    plain_text = items
            return HttpResponse(content=plain_text, content_type='text/plain')


def generate_error_response(method_name, elapsed, e):
        log_error(e, 'adapter' + method_name, method_name + ' search failed')
        return JsonResponse({
            'duration': '%.2f' %elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status = 500)



@csrf_exempt
def address(request):

    if not request.method == 'POST':
        return JsonResponse({"Request must be":"POST"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        addresses = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_addresses(cleanse_data_list(addresses))
        return generate_response(matches_cursor, request, elapsed)
    except Exception as e:
        return generate_error_response("address_search", elapsed, e)


@csrf_exempt
def domain_names(request):

    if not request.method == 'POST':
        return JsonResponse({"Request must be":"POST"}, status=405)

    elapsed = StopWatch()
    try:
        raw_body = request.body
        names = REGEX_ADDRESS_DELIMITER.split(raw_body)
        matches_cursor = get_domain_names(cleanse_data_list(names))
        return generate_response(matches_cursor, request, elapsed)
    except Exception as e:
        return generate_error_response("domain_name", elapsed, e)

