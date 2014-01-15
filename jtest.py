import json


json_db['Flags'].append( { 'FlagID': 2, 'FlagName': 'Flag2' } )



print ( json.dumps( json_db, sort_keys=True, indent=4, separators=(',', ': ')) )
