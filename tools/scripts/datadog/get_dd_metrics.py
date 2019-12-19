#!/usr/bin/env python

from datadog import initialize, api
import argparse
import re
import time
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', dest='apikey', default=None)
    parser.add_argument('--appkey', dest='appkey', default=None)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-f', '--filter', dest='tfilter', default=None)
    parser.add_argument('--hours', dest='hours', type=int, default=1)
    parser.add_argument('-o', '--output-file', dest='ofile', default="metric_rlts.txt")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    # print('Args: {0}'.format(args))
    debug = args.debug
    tfilter = args.tfilter
    hours = args.hours
    output_file = args.ofile
    verbose = args.verbose

    if args.apikey is None or args.appkey is None:
        print('Api or App key missing')
        sys.exit(1)
    
    options = {
        'api_key' : '{0}'.format(args.apikey),
        'app_key' : '{0}'.format(args.appkey)
    }

    if args.debug is True:
        print('Debug: {0}'.format(debug))
        print('Filter: {0}'.format(tfilter))
        print('Hour(s): {0}'.format(hours))
        print('Output file: {0}'.format(output_file))
        print('Verbose: {0}'.format(verbose))

    try:
        initialize(**options)
    except:
        print('Datadog initialize failed')
        sys.exit(1)

    try:
        # Taking the last 'hours' of metrics
        from_time = int(time.time()) - 60 * 60 * hours * 1
        result = api.Metric.list(from_time)
        if verbose is True:
            print('Total results: ({0})'.format(len(result['metrics'])))
            # print(result)

        f = open('{0}'.format(output_file), "w")
        f.write('Total results: ({0})\n'.format(len(result['metrics'])))

        ndex = 1
        for entry in result['metrics']: 
            if tfilter is not None:
                if re.search('{0}'.format(tfilter), entry) is not None:
                    if verbose is True:
                        print(entry)
                    f.write('{0}) {1}\n'.format(ndex, entry))
                    ndex += 1
            else:
                if verbose is True:
                    print(entry)
                f.write('{0}) {1}\n'.format(ndex, entry))
                ndex += 1

        f.close()
    except:
        print('Metric retrieval failed')
        

if __name__ == '__main__':
    main()
