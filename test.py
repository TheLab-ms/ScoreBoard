import json

f1 = 1
f2 = 2
jsonobj1 = []
jsonobj1['flags'] = [f1, {'Flag': 'FlagName','Points': 100,}]

sObj1 = str(jsonobj1)

print ('sObj1', sObj1 )

dumpObj1 = json.dumps(sObj1)

print ('dumpObj1', dumpObj1)

data  = json.loads(dumpObj1)

print ( 'data', data )

data['flags'] = [f2, {'Flag': 'FlagName2','Points': '200',}]

print ( 'data', data )



