This is the readme file for Datadog scripts:


// Prerequistes
API and APP key for datadog#


// Retrieve all datadog monitors

./get_monitors.py -h

usage: get_monitors.py [-h] [--apikey APIKEY] [--appkey APPKEY] [-d]
                       [--monitor MONITOR] [-v]

optional arguments:
  -h, --help         show this help message and exit
  --apikey APIKEY
  --appkey APPKEY
  -d, --debug
  --monitor MONITOR
  -v, --verbose

// Retrive datadog metrics

./get_dd_metrics.py -h
usage: get_dd_metrics.py [-h] [--apikey APIKEY] [--appkey APPKEY] [-d]
                         [-f TFILTER] [--hours HOURS] [-o OFILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --apikey APIKEY
  --appkey APPKEY
  -d, --debug
  -f TFILTER, --filter TFILTER
  --hours HOURS
  -o OFILE, --output-file OFILE
  -v, --verbose
