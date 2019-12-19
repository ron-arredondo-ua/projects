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
    parser.add_argument('--monitor', dest='monitor', default='all')
    # parser.add_argument('-f', '--filter', dest='tfilter', default=None)
    # parser.add_argument('--hours', dest='hours', type=int, default=1)
    # parser.add_argument('-o', '--output-file', dest='ofile', default="metric_rlts.txt")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    # print('Args: {0}'.format(args))
    debug = args.debug
    # tfilter = args.tfilter
    # hours = args.hours
    # output_file = args.ofile
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
        # print('Filter: {0}'.format(tfilter))
        # print('Hour(s): {0}'.format(hours))
        # print('Output file: {0}'.format(output_file))
        print('Verbose: {0}'.format(verbose))

    try:
        initialize(**options)
    except:
        print('Datadog initialize failed')
        sys.exit(1)

    try:
        # Get all monitor details
        monitors = api.Monitor.get_all()
        if args.debug is True:
            print(monitors)
        for entry in monitors:
            if args.debug is True:
                print(entry)
            print('Monitor: {0}'.format(entry['name']))
    except:
        print('Monitor retrieval failed')
        

if __name__ == '__main__':
    main()
