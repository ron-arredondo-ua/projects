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
    parser.add_argument('-d', '--debug', default='store_false', action='store_true')
    parser.add_argument('--dryrun', default='store_false', action='store_true')
    parser.add_argument('-n', '--namespace', default=None, required=True)
    parser.add_argument('-r', '--rule', default=None, required=True)
    parser.add_argument('-v', '--verbose', default='store_false', action='store_true')
    args = parser.parse_args()
    debug = args.debug
    dryrun = args.dryrun
    namespace = args.namespace
    rule = args.rule
    verbose = args.verbose

    if args.debug is True:
        print('Debug: {0}'.format(debug))
        print('Dryrun: {0}'.format(dryrun))
        print('Namespace: {0}'.format(namespace))
        print('Rule: {0}'.format(rule))
        print('Verbose: {0}'.format(verbose))

    cmd = "kubectl get {0} -n {1} -o name".format(rule, namespace)
    if verbose is True:
        print('cmd: {0}'.format(cmd))

    try:
        rules = subprocess.check_output([cmd], shell=True)
        if debug is True:
            print('Returned output:', rules.decode('utf-8'))
    except OSError as error:
        print('command {0} returned error {1}'.format(cmd, error))
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        print('command {0} returned error {1}'.format(cmd, error))
        sys.exit(1)

    rules_list = rules.split('\n')
    if debug is True:
        print('Data:', rules_list)

    print('\nAlerts for rule {0} using name space {1}:'.format( rule, namespace))

    for rule_name in rules_list:
        if args.debug is True:
            print('{0}'.format(rule_name))
        if rule in rule_name:
            rule_only = rule_name.split('/')
            cmd = 'kubectl get {0} {1} -n {2} -o json'.format(rule, rule_only[1], namespace)
            if verbose is True:
                print('cmd: {0}'.format(cmd))
            try:
                data = subprocess.check_output([cmd], shell=True)
                rdata = json.loads(data)
                if debug is True:
                    print('rule json data: {0}'.format(rdata))
            except OSError as error:
                print('command {0} returned error {1}'.format(cmd, error))
            except subprocess.CalledProcessError as error:
                print('command {0} returned error {1}'.format(cmd, error))

            if rdata.get('spec') is not None:
                if rdata.get('spec').get('groups') is not None:
                    gdata = rdata.get('spec').get('groups')
                    if debug is True:
                        print('\ngdata: {0}'.format(gdata))
                    for gentry in gdata:
                        if debug is True:
                            print('\nrule entry: {0}'.format(gentry))
                        print('\n{0} alerts:'.format(rdata.get('metadata').get('name')))
                        if gentry.get('rules') is not None:
                            for rentry in gentry.get('rules'):
                                if debug is True:
                                    print('\nrule value: {0}'.format(rentry))
                                if rentry.get('alert') is not None:
                                    print('{0}'.format(rentry.get('alert')))


if __name__ == '__main__':
    main()
