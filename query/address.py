
from mongoengine.connection import get_db


def get_addresses(data):
    if not data:
        raise Exception("No addresses supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'AddressObjectType',
                'data.summary.value': {
                    '$in': data
                }
            }
        },
        {
            '$group': {
                '_id': '$data.summary.value',
                'objects': {
                    '$push': '$_id'
                }
            }
        }
    ], cursor={})

    return matches_cursor
