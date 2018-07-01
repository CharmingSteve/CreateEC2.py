#!/usr/bin/env python3

import boto3
import sys
import os

# usage createec2.py <AWS-REGION> <IMAGE-ID>

region = sys.argv[1]

ec2 = boto3.client('ec2', region_name=(region))


#use the following from Ec2 to call the region from the script instead of typing in as arg.
#import urllib.request
#f = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone/')
#region = (f.read(100).decode('utf-8')[:-1])

# Create sec group
sec_group = ec2.create_security_group(GroupName=(region)+'-charming', Description='CharmingWebServer')

#Add rules to security Group
ec2.authorize_security_group_ingress(GroupName=(region)+'-charming' ,IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)

ec2.authorize_security_group_ingress(GroupName=(region)+'-charming' ,IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)

#Create a key with the same name as the Sec Group 
outfile = open((region)+'-charming.pem','w')
ec2 = boto3.client('ec2', region_name=(region))
keypair = ec2.create_key_pair(KeyName=(region)+'-charming')
i = keypair['KeyMaterial']
outfile.write(i)
outfile.close()
os.chmod((region)+'-charming.pem', 400)

#Create the instance using the key and putting it in the sec group
imageid = sys.argv[2]
instances = ec2.run_instances(
	ImageId=(imageid), 
	KeyName=(region)+'-charming',
	MinCount=1, 
	MaxCount=1,
	InstanceType="t2.micro",
	SecurityGroups=[(region)+'-charming',],
	)	
