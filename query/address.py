
from mongoengine.connection import get_db


def get_matches(addresses):
    if not addresses:
        raise Exception("No addresses supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'AddressObjectType',
                'data.summary.value': {
                    '$in': addresses
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
