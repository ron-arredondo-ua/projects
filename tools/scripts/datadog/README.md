This is the readme file for Datadog scripts:

# Prerequistes:
#
# Dataddog API and APP keys are required for using this script
#

# Retrieve all datadog monitors

./get_monitors.py -h

usage: get_monitors.py [-h] [--apikey APIKEY] [--appkey APPKEY] [-d]
                       [--monitor MONITOR] [-v]

optional arguments:
  -h, --help         show this help message and exit
  --apikey APIKEY
  --appkey APPKEY
  -d, --debug
  -v, --verbose

example: ./get_monitors.py --apikey ><aip key value> --applkey <app key value>

# Retrive datadog metrics

./get_dd_metrics.py -h

usage: get_dd_metrics.py [-h] [--apikey APIKEY] [--appkey APPKEY] [-d]
                         [-f TFILTER] [--hours HOURS] [-o OFILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --apikey APIKEY
  --appkey APPKEY
  -d, --debug
  -f TFILTER, --filter TFILTER [search filter: e.g. "aws"]
  --hours HOURS [number of hour: e.g. 1 (one hour)]
  -o OFILE, --output-file OFILE
  -v, --verbose

example: ./get_dd_metrics.py --apikey ><aip key value> --applkey <app key value> -h 1 -f "http"
