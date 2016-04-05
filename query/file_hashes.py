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
                '$or': [ {'data.api.object.properties.hashes.type.value': {
                    '$in': data }
                }, {'data.api.object.properties.hashes.type': {
                    '$in': data}
            }]
            }
        },
        {
            '$project': {
                'data.api.object.properties.hashes.type': '$data.api.object.properties.hashes.type.value'
            }
        },
        {
            '$group': {
                '_id': '$data.api.object.properties.hashes.type.value',
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
