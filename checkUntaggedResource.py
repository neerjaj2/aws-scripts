import sys
import boto
import smtplib
from email.mime.text import MIMEText
from boto import ec2
from boto import vpc 
import csv

with open('/tmp/resources.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [['Resource','ID', 'TAGS NOT DEFINED' ]]
    a.writerows(data)

connection=ec2.connect_to_region('ap-southeast-1')

sg_s = connection.get_all_security_groups()

#volumes = connection.get_all_volumes()

#images = connection.get_all_images(owners="")

#snapshots = connection.get_all_snapshots(owner="")

reservations = connection.get_all_instances()

vpc_conn = vpc.connect_to_region('ap-southeast-1')

subnet = vpc_conn.get_all_subnets()

VPC = vpc_conn.get_all_vpcs()

autoscaling = boto.connect_autoscale()

as_gs=autoscaling.get_all_groups()

user_tags = { 'Name', 'Environment' }

for sc in sg_s:
	sg_tag=sc.tags
	if bool(sg_tag) is True:
		for us_tag in user_tags:
			if us_tag not in sg_tag.keys():
				ID=sc.id
				with open('/tmp/resources.csv', 'a') as fp:
				    a = csv.writer(fp, delimiter=',')
    				    data = [['SecurityGroups',ID, us_tag ]]
   				    a.writerows(data)
	if bool(sg_tag) is False:
		ID=sc.id
                with open('/tmp/resources.csv', 'a') as fp:
        	        a = csv.writer(fp, delimiter=',')
                        data = [['SecurityGroups',ID, 'Tagless' ]]
                	a.writerows(data)

'''
for vol in volumes:
        vol_tag=vol.tags
        if bool(vol_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in vol_tag.keys():
                                ID=vol.id
                                with open('resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['Volume',ID, us_tag ]]
                                    a.writerows(data)
        if bool(vol_tag) is False:
		ID=vol.id
 	        with open('resources.csv', 'a') as fp:
        	        a = csv.writer(fp, delimiter=',')
                        data = [['Volume',ID, 'Tagless' ]]
                        a.writerows(data)
'''
'''
for img in images:
        img_tag=img.tags
        if bool(img_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in img_tag.keys():
                                ID=img.id
                                with open('resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['AMI',ID, us_tag ]]
                                    a.writerows(data)
        if bool(img_tag) is False:
		ID=img.id
                with open('resources.csv', 'a') as fp:
                        a = csv.writer(fp, delimiter=',')
                        data = [['AMI',ID, 'Tagless' ]]
                        a.writerows(data)
'''
'''
for snap in snapshots:
        snap_tag=snap.tags
        if bool(snap_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in snap_tag.keys():
                                ID=snap.id
				with open('resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['Snapshots',ID, us_tag ]]
                                    a.writerows(data)
        if bool(snap_tag) is False:
		ID=snap.id
                with open('resources.csv', 'a') as fp:
                        a = csv.writer(fp, delimiter=',')
                        data = [['Snapshots',ID, 'Tagless' ]]
                        a.writerows(data)
'''
user_tags = { 'Name', 'Environment', 'Role' }
for reservation in reservations:
	for instance in reservation.instances:
		if instance.state=="running":
        		instance_tag=instance.tags
       			if bool(instance_tag) is True:
        			for us_tag in user_tags:
                       			 if us_tag not in instance_tag.keys():
                               			ID=instance.id
                                		with open('/tmp/resources.csv', 'a') as fp:
                                	    		a = csv.writer(fp, delimiter=',')
                                    			data = [['Instances',ID, us_tag ]]
                                    			a.writerows(data)
        	
       			if bool(instance_tag) is False:
				ID=instance.id
              		  	with open('/tmp/resources.csv', 'a') as fp:
                        		a = csv.writer(fp, delimiter=',')
                        		data = [['Instances',ID, 'Tagless' ]]
                       			a.writerows(data)

user_tags = { 'Name', 'Environment' }

for sub in subnet:
        sub_tag=sub.tags
        if bool(sub_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in sub_tag.keys():
                                ID=sub.id
                                with open('/tmp/resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['Subnets',ID, us_tag ]]
                                    a.writerows(data)
        if bool(sub_tag) is False:
		ID=sub.id
                with open('/tmp/resources.csv', 'a') as fp:
                        a = csv.writer(fp, delimiter=',')
                        data = [['Subnets',ID, 'Tagless' ]]
                        a.writerows(data)


for vp in VPC:
        vp_tag=vp.tags
        if bool(vp_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in vp_tag.keys():
                                ID=vp.id
                                with open('/tmp/resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['VPC',ID, us_tag ]]
                                    a.writerows(data)
        if bool(vp_tag) is False:
		ID=vp.id
                with open('/tmp/resources.csv', 'a') as fp:
                        a = csv.writer(fp, delimiter=',')
                        data = [['VPC',ID, 'Tagless' ]]
                        a.writerows(data)


for auto in as_gs:
        auto_tag=auto.tags
        if bool(auto_tag) is True:
		for us_tag in user_tags:
                        if us_tag not in auto_tag.keys():
                                ID=auto.name
                                with open('/tmp/resources.csv', 'a') as fp:
                                    a = csv.writer(fp, delimiter=',')
                                    data = [['AutoScalingGroups',ID, us_tag ]]
                                    a.writerows(data)
        if bool(auto_tag) is False:
		ID=auto.name
                with open('/tmp/resources.csv', 'a') as fp:
                        a = csv.writer(fp, delimiter=',')
                        data = [['AutoScalingGroups',ID, 'Tagless' ]]
                        a.writerows(data)
with open('/tmp/resources.csv') as doc:
    line =  sum(1 for _ in doc)

if line != 1:

	sender = 'Utility@AmericanSwan'
	receivers = ['as-support@intelligrape.com']
	'''
	message = """From: Utility@AmericanSwan <utility@americanswan.com>
	To: NavjotSingh 
	Subject: SMTP e-mail test

	This is a test e-mail message.
	"""

	try:
	   smtpObj = smtplib.SMTP('localhost')
	   smtpObj.sendmail(sender, receivers, message)
	   print "Successfully sent email"
	except SMTPException:
	   print "Error: unable to send email"
	'''
	resourceFile = open("/tmp/resources.csv", 'rb')
	msg = MIMEText(resourceFile.read())
	resourceFile.close()
	msg['Subject'] = 'List of Untagged Resources in AmericanSwan\'s account'
	msg['From'] = "Utility@AmericanSwan <utility@americanswan.com>"
	msg['To'] = "as-support"

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	try:
	 s = smtplib.SMTP('localhost')
	 s.sendmail(sender, receivers, msg.as_string())
	 print "Successfully sent email"
	 s.quit()
	except SMTPException:
	 print "Error: unable to send email"
else :	 

	print "Nothing to do.Enjoy!!" 
