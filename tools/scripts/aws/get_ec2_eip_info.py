#!/usr/bin/env python3


import argparse
import json 
import os, sys, traceback
import re
import boto3

from datetime import datetime

class UAEc2Eip(object):
    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--debug', default='store_false', action='store_true')
        parser.add_argument('--dryrun', default='store_false', action='store_true')
        parser.add_argument('--interface-type', dest='interface_type', default=None)
        parser.add_argument('-o', '--output-file', dest='ofile', default="eip_ofile.txt")
        parser.add_argument('-v', '--verbose', default='store_false', action='store_true')
        args = parser.parse_args()
        self.debug = args.debug
        self.dryrun = args.dryrun
        self.interface_type = args.interface_type
        self.ofile = args.ofile
        self.verbose = args.verbose

        self.total_pages = 0

        self.create_ofile()
        self.ec2_client = boto3.client('ec2')
        
        if args.debug is True:
            print('Debug: {0}'.format(self.debug))
            print('Dryrun: {0}'.format(self.dryrun))
            print('Interface type: {0}'.format(self.interface_type))
            print('Output file: {0}'.format(self.ofile))
            print('Verbose: {0}'.format(self.verbose))

    def append_to_file(self, write_data):
        try:
            with open(self.ofile, "a") as fd:
                fd.write(write_data)
        except IOError as error:
            print("File %s append failed: %s" % (self.ofile, error))
            traceback.print_exc(file=sys.stdout)

    def create_ofile(self):
        try:
            with open(self.ofile, "w") as fd:
                fd.write("%s" % datetime.now())
        except IOError as error:
            print("File %s creation failed: %s" % (self.ofile, error))
            traceback.print_exc(file=sys.stdout)

    def get_eips(self):
        try:
            itoken = None
            while True:
                paginator = self.ec2_client.get_paginator('describe_network_interfaces')
                page_iterator = paginator.paginate(
                    PaginationConfig={
                        'PageSize': 100,
                        'StartingToken': itoken
                    }
                )
                for response in page_iterator:
                    self.total_pages += 1

                    if self.verbose is True:
                        print("Network interfaces: %s" % response.get('NetworkInterfaces', None))
                
                    if self.debug is True:
                        print("\nNetwork interface entries (%s):" % len(response.get('NetworkInterfaces', None)))
                    for entry in response.get('NetworkInterfaces', None):
                        if entry.get('InterfaceType') is not None:
                            # if self.verbose is True:
                            #    print("Interface type: %s" % entry.get('InterfaceType', None))

                            if entry.get('Attachment', None) is not None:
                                instance_id = entry.get('Attachment').get('InstanceId', None)
                            else:
                                instance_id = None
                            owner_id = entry.get('OwnerId', None)
                            private_dns = entry.get('PrivateDnsName', None)
                            intfc_type = entry.get('InterfaceType', None)
                            
                            for address in entry.get('PrivateIpAddresses'):
                                if self.verbose is True:
                                    print("\tAddress: %s" % address)
                                    
                                if address.get('Association') is not None:
                                    print("\nInterface: owner-%s instance id:%s type-%s dns-%s" % (
                                            owner_id,
                                            instance_id,
                                            intfc_type,
                                            private_dns
                                        )
                                    )
                                    self.append_to_file("\n\nInterface:\n\towner: %s\n\tinstance id: %s\n\ttype: %s\n\tdns: %s" % (
                                            owner_id,
                                            instance_id,
                                            intfc_type,
                                            private_dns
                                        )
                                    )
                                    if address.get('PrivateIpAddress', None) is not None:
                                        self.append_to_file("\n\tPrivateIpAddress: %s" % address.get('PrivateIpAddress'))
                                        print("\tPrivateIpAddress: %s" % address.get('PrivateIpAddress'))
                                    if address.get('Association').get('PublicIp', None) is not None:
                                        self.append_to_file("\n\tPublicIp: %s" % address.get('Association').get('PublicIp'))
                                        print("\tPublicIp: %s" % address.get('Association').get('PublicIp'))
                                    if self.verbose is True:
                                        self.append_to_file("\n\tInterface association data: %s" % address.get('Association'))
                                        print("\tInterface association data: %s" % (
                                            address.get('Association')
                                            )
                                        )

                itoken = response.get('NextToken')
                print("\n\t\tNext token: %s" % itoken)
                self.append_to_file("\n\n\t\tNext token: %s" % itoken)
                if itoken is None:
                    break

        except Exception as error:
            print("Exception occurred: %s" % error)
            traceback.print_exc(file=sys.stdout)

#
# create and access objects
#
ec2_eip_object = UAEc2Eip()
ec2_eip_object.get_eips()
print("Handled %s total pages" % ec2_eip_object.total_pages)
