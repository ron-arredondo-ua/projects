#!/usr/bin/env python

# from datadog import initialize, api
import argparse
import json 
# import time
import sys
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-n', '--namespace', default=None, required=True)
    parser.add_argument('-r', '--rule', default=None, required=True)
    parser.add_argument('-s', '--subrule', default=None, required=True)
    args = parser.parse_args()
    debug = args.debug
    namespace = args.namespace
    rule = args.rule
    subrule = args.subrule

    if args.debug is True:
        print('Debug: {0}'.format(debug))
        print('Namespace: {0}'.format(namespace))
        print('Rule: {0}'.format(rule))
        print('Subrule: {0}'.format(subrule))

    cmd = "kubectl get {0} {1} -n {2} -o yaml".format(rule, subrule, namespace)
    if debug is True:
        print('cmd: {0}'.format(cmd))

    try:
        rData = subprocess.check_output([cmd], shell=True)
        print('Returned output:\n{0}'.format(rData))
    except OSError as error:
        print('command {0} returned error {1}'.format(cmd, error))
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        print('command {0} returned error {1}'.format(cmd, error))
        sys.exit(1)

if __name__ == '__main__':
    main()
