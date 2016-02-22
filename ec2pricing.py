#!/usr/bin/python
# Description: An instance had 10% or less daily average CPU utilization and 5 MB or less network I/O on at least 4 of the previous 14 days.

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
import dateutil
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
import csv
import urllib2
import json

with open('ec2pricing.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(['Region','Instance ID', 'Instance Type', 'Instance Pricing'])


# Using depreciated AWS pricing json
url = "https://a0.awsstatic.com/pricing/1/deprecated/ec2/pricing-on-demand-instances.json"
response = urllib2.urlopen(url).read()
extractjson = json.loads(response)

# Below mentioned js is extracted from AWS EC2 Pricing page, And below mentioned commands are extracting required information
#getjs = urllib2.urlopen('http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js')
#html = getjs.read()
#search = "callback"
#print html.index(search)
#extractjson = html[201:-2]

jsontoec2 = {
    "us-east" : "us-east-1",
    "us-east-1" : "us-east-1",
    "us-west" : "us-west-1",
    "us-west-1" : "us-west-1",
    "us-west-2" : "us-west-2",
    "eu-ireland" : "eu-west-1",
    "eu-west-1" : "eu-west-1",
    "eu-central-1" : "eu-central-1",
    "apac-sin" : "ap-southeast-1",
    "ap-southeast-1" : "ap-southeast-1",
    "ap-southeast-2" : "ap-southeast-2",
    "apac-syd" : "ap-southeast-2",
    "apac-tokyo" : "ap-northeast-1",
    "ap-northeast-1" : "ap-northeast-1",
    "sa-east-1" : "sa-east-1",
    "us-gov-west-1" : "us-gov-west-1"
}


default_instances={}

for i in extractjson['config']['regions']:
    print i['region']
    defaultinstances={}
    for z in i['instanceTypes']:
        j=0
        print len(z['sizes'])
        while j < len(z['sizes']):
            instancetype = z['sizes'][j]['size']
            instanceprice = z['sizes'][j]['valueColumns'][0]['prices']['USD']
            #print instancetype, instanceprice
            defaultinstances[str(instancetype)]= str(instanceprice)
            #default_instances.update({'instancetype':'instanceprice'})
            j = j + 1
    #print defaultinstances

    print "************************************************************************************************************"

    print jsontoec2[i['region']]
    ec2conn = ec2.connect_to_region(jsontoec2[i['region']])
    instances=[]
    #print ec2conn
    reservations = ec2conn.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            print instance, instance.instance_type
            if instance.instance_type in defaultinstances:
                #print instance.instance_type, defaultinstances[instance.instance_type]
                with open('ec2pricing.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter='\t')
                    writer.writerow([jsontoec2[i['region']],instance.id,instance.instance_type,defaultinstances[instance.instance_type]])
