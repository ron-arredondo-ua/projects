#!/usr/bin/env python3

import argparse
import json
import os, sys, time, traceback
import re
import boto3

from datetime import datetime

class UARoute53(object):
    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--debug', default='store_false', action='store_true')
        parser.add_argument('--dryrun', default='store_false', action='store_true')
        parser.add_argument('-o', '--output-file', dest='ofile', default="ofile_route53.txt")
        parser.add_argument('--record-type', dest='record_type', default=None)
        parser.add_argument('-v', '--verbose', default='store_false', action='store_true')
        args = parser.parse_args()
        self.debug = args.debug
        self.dryrun = args.dryrun
        self.ofile = args.ofile
        self.record_type = args.record_type
        self.verbose = args.verbose

        # create output file
        self.create_ofile()

        self.route53_client = boto3.client('route53')
        self.total_hz_pages = 0
        self.total_rs_pages = 0

        if args.debug is True:
            print('Debug: {0}'.format(self.debug))
            print('Dryrun: {0}'.format(self.dryrun))
            print('Output file: {0}'.format(self.ofile))
            print('Record type: {0}'.format(self.record_type))
            print('Verbose: {0}'.format(self.verbose))

    def append_to_file(self, write_data):
        try:
            with open(self.ofile, "a") as fd:
                fd.write(write_data)
        except IOError as error:
            print("File %s append failed: %s" % (self.ofile, error))

    def create_ofile(self):
        try:
            with open(self.ofile, "w") as fd:
                fd.write("%s\n" % datetime.now())
        except IOError as error:
            print("File %s opened failed: %s" % (self.ofile, error))

    def get_route53_zones(self):
        try:
            ztoken = None
            while True:
                paginator = self.route53_client.get_paginator('list_hosted_zones')
                page_iterator = paginator.paginate(
                    PaginationConfig={
                        'PageSize': 100,
                        'StartingToken': ztoken
                    }
                )
                for response in page_iterator:
                    self.total_hz_pages += 1

                    if self.verbose is True:
                        print("\nlist_hosted_zones: %s" % response.get('HostedZones'))
                    for entry in response.get('HostedZones'):
                        if self.verbose is True:
                            print("Entry id: %s" % entry.get('Id').split('/'))
                        if self.debug is True:
                            self.append_to_file("\n\nentry: %s" % entry)

                        print("Hosted zone: %s" % entry.get('Name'))
                        self.append_to_file("\n\nHosted zone: %s" % entry.get('Name'))
                        id = entry.get('Id').split('/')[2] 
                        if self.verbose is True:
                            print("Id: %s" % id)

                        rtoken = None
                        while True:  
                            paginator_lrrs = self.route53_client.get_paginator('list_resource_record_sets')
                            page_iterator_lrrs = paginator_lrrs.paginate(
                                    HostedZoneId=id,
                                    PaginationConfig={
                                        'PageSize': 100,
                                        'StartingToken': rtoken
                                    }
                                )
                            record_sets = 0
                            for record_page in page_iterator_lrrs:
                                self.total_rs_pages += 1
                                record_sets += 1
                                self.append_to_file("\nRecords (%s) for id %s" % (
                                        len(record_page.get('ResourceRecordSets')),
                                        id
                                    )
                                )
                                self.append_to_file("\n\tRecord id %s has type %s:" % (id, self.record_type))
                                record_count = 0
                                for rset in record_page.get('ResourceRecordSets'):
                                    record_count =+ 1
                                    if self.record_type is None:
                                        # print("\t\t%s set: %s" % (set.get('Name'), set))
                                        self.append_to_file("\n\t\t%s set: %s" % (rset.get('Name'), rset))
                                    else:
                                        if re.fullmatch(self.record_type, rset.get('Type')) != None:
                                            # print("\t\t%s set: %s" % (set.get('Name'), set))
                                            self.append_to_file("\n\t\t%s set: %s" % (rset.get('Name'), rset))

                            rtoken = record_page.get('NextToken')
                            if self.debug is True:
                                self.append_to_file("\n\t\tIstruncated flag: %s; NextToken: %s" % (record_page.get('IsTruncated'), rtoken))
                                self.append_to_file("\n\t\tRecord set pages=%s; sets=%s; count=%s; maker=%s)" % (
                                        self.total_rs_pages,
                                        record_sets,
                                        record_count,
                                        record_page.get('Marker')
                                    )
                                )
                            if record_page.get('IsTruncated') is False:
                                self.append_to_file("\n\t\tRecord set complete")
                                break

                ztoken = response.get('Marker')
                if self.debug is True:
                    print("\t\tResponse: IsTruncated-%s; Marker-%s" % (response.get('IsTruncated'), ztoken))
                    self.append_to_file("\n\t\tResponse: IsTruncated-%s; Marker-%s" % (response.get('IsTruncated'), ztoken))
                if response.get('IsTruncated') is False:
                    break
                
        except Exception as error:
            print("Exception occurred: %s" % error)
            traceback.print_exc(file=sys.stdout)


#
# create and access objects
#
route53_object = UARoute53()
route53_object.get_route53_zones()
print("\nHandled %s total hosted zones pages" % route53_object.total_hz_pages)
print("Handled %s total resource set pages" % route53_object.total_rs_pages)
