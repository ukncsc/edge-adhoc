from mongoengine.connection import get_db

def matches_on_email_address(data):
    if not data:
        raise Exception("No data supplied for email addreess search")
    matches_cursor = get_db().stix.aggregate([
        {
           '$match': {
               'data.summary.type': 'EmailMessageObjectType'
           }
        },
        {

        }

    ], cursor ={})
