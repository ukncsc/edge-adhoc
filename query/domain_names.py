from mongoengine.connection import get_db

def get_domain_names(data):
    if not data:
        raise Exception("No domain names supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'DomainNameObjectType',
                'data.summary.value': {
                    '$in': data
                }
            }
        },
        {
                '$group': {
                    '_id': '$data.summary.value',
                    'objects': {
                        '$push':'$_id'
                    }
                }
        },
        {
            '$sort': {'_id': 1}
        }
    ], cursor={})

    return matches_cursor
