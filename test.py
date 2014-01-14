import json

jsonobj = {'FlagIDs': {'1':     {
                                    'Flag': 'FlagName',
                                    'Points': '100',
                                 },
                       }
           }
print ( json.dumps(jsonobj, indent=4, separators=(',',':')))

jsonobj = {'2': {'Flag': 'FlagName2','Points': '200',},}

print ( json.dumps(jsonobj, indent=4, separators=(',',':')))
