from mongoengine.connection import get_db

def get_file_hashes(data):
    if not data:
        raise Exception("No file hashes supplied")
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'FileObjectType'
            }
        },
        {
            '$unwind': '$data.api.object.properties.hashes'
        },
        {
            '$match': {
                'data.api.object.properties.hashes.type': {
                    '$in': data
                }
            }
        },
        {
            '$group': {
                '_id': '$data.api.object.properties.hashes.type',
                'objects': {
                    '$push': {
                        'id':'$_id',
                        'hash value': '$data.api.object.properties.hashes.simple_hash_value'
                    }
                }
            }
        },
        {
            '$sort': {'_id':1}
        }
    ], cursor={})

    return matches_cursor
