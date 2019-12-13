#!/usr/bin/env python

from datadog import initialize, api
import time

options = {
    'api_key' : 'a58e6cfdb6b9607c508ce143e17a60cd',
    'app_key': '20afc3a55b81c93fdff5ceec5f2bc139167e5567' 
}

initialize(**options)

# Taking the last 24hours
from_time = int(time.time()) - 60 * 60 * 1 * 1

result = api.Metric.list(from_time)

f = open("metric_rlts.txt", "w")
print('Results ({0}):'.format(len(result['metrics'])))
print(result)
f.write('Results ({0}):\n'.format(len(result['metrics'])))

for entry in result['metrics']:
   print(entry)
   f.write('{0}\n'.format(entry))
   
f.close()
