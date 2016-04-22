from mongoengine.connection import get_db

def partial_matches_on_ip(data, objectType):
    if not data:
        raise Exception("No file hash types supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {'$and': [{
                'data.summary.type': objectType
            }, {'data.api.object.properties.ip_address': {
                '$exists': 'true'
            }}]
            }
        },
        {
            '$match': {
                'data.api.object.properties.ip_address.address_value': {
                    '$in': data}
            }
        },
        {
            '$group': {
                '_id': '$data.summary.value',
                'objects': {
                    '$push': '$_id'
                }
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ], cursor={})

    return matches_cursor
