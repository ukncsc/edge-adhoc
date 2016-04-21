from mongoengine.connection import get_db

def matches_on_email_address_field(data, addressField):
    if not data:
        raise Exception("No data supplied for email addreess search")
    query_address = 'data.api.object.properties.header.' + addressField
    address_value = query_address + '.address_value'
    matches_cursor = get_db().stix.aggregate([
        {
            '$match': {
                'data.summary.type': 'EmailMessageObjectType'
            }
        },
        {
            '$unwind': '$' + query_address
        },
        {
            '$match': {
                address_value:{
                    '$in': data
                }
            }
        },
        {
            '$group': {
                '_id': '$' + address_value,
                'objects':{
                    '$push': '$_id'
                }
            }
        },
        {
            '$sort': {'_id':1}
        }
    ], cursor={})

    return matches_cursor
