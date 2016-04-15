
from mongoengine.connection import get_db


def matches_on_object_type(data, objectType):
    if not data:
        raise Exception("No addresses supplied for: " + objectType)
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type':objectType,
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
        },
        {
            '$sort': {'_id':1}
        }
    ], cursor={})

    return matches_cursor
