from django.views.decorators.csrf import csrf_exempt

from adapters.certuk_adhoc.query.address import get_matches
from adapters.certuk_adhoc.common.logger import log_error

from edge.tools import StopWatch
from django.http.response import JsonResponse


@csrf_exempt
def search(request):
    if not request.method == 'POST':
        return JsonResponse({}, status=405)

    elapsed = StopWatch()
    try:
        addresses = request.body.split("\n")
        matches_cursor = get_matches(addresses)
        response = {
            'state': 'success',
            'matches': {}
        }
        for match_result in matches_cursor:
            address = match_result['_id']
            response['matches'][address] = match_result['objects']
        return JsonResponse(response, status=200)
    except Exception as e:
        log_error(e, 'adapters/address_search', 'Bulk address search failed')
        return JsonResponse({
            'duration': '%.2f' % elapsed.ms(),
            'message': e.message,
            'state': 'error'
        }, status=500)
