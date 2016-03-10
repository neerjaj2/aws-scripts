et our home directory which holds our ip file
WORKDIR=/home/ubuntu/scripts/neeraj/apache-url-monitor

# set the name of the security group as show in aws console
SEC_GROUP_ID1="sg-9d47baf9"
SEC_GROUP_ID2="sg-f7a95593"

##### END VARIABLES TO SET ######################


# first we check for existing file
if [ -f ${WORKDIR}/.newrelicip ]; then
	# if it exists, we create a backup for comparison
	cp ${WORKDIR}/.newrelicip ${WORKDIR}/.newrelicip.old
	# then grab the current ip
	WAN=`curl -s https://s3.amazonaws.com/nr-synthetics-assets/nat-ip-dnsname/production/ip.json | jq .[][] -r`
	# and populate the new file
	echo ${WAN} > ${WORKDIR}/.newrelicip

	# here we need to check if the files differ
	diff ${WORKDIR}/.newrelicip ${WORKDIR}/.newrelicip.old
		if [ $? = 0 ]; then
			echo "no update required"
			exit 1
		else
			echo "update required....stand by"
			# here we get the value to revoke
			REVOKE=`cat ${WORKDIR}/.newrelicip.old`
			# then revoke the old ip
			for i in $REVOKE
			do
				aws ec2 describe-security-groups --group-id ${SEC_GROUP_ID1} | grep IPRANGES | awk '{print $2}' > .sg1.txt
				if  grep $i .sg1.txt >> /dev/null
				then
					echo ${SEC_GROUP_ID1} "urlmonitoring" $i
					aws ec2 revoke-security-group-ingress --group-id ${SEC_GROUP_ID1} --protocol tcp --port 80 --cidr $i/32
				else
					echo ${SEC_GROUP_ID2} "urlmonitoring2" $i
					aws ec2 revoke-security-group-ingress --group-id ${SEC_GROUP_ID2} --protocol tcp --port 80 --cidr $i/32
				fi
				sleep 1
			done
			NUMBER=`curl -s https://s3.amazonaws.com/nr-synthetics-assets/nat-ip-dnsname/production/ip.json | jq .[][] -r | wc -l`
        		NEWIP=`cat ${WORKDIR}/.newrelicip`
        		count=0
        		for i in $NEWIP
        		do
                		echo $i $count adding rule
                		if [ $count -lt 40 ]
                		then
                        		aws ec2 authorize-security-group-ingress --group-id ${SEC_GROUP_ID1}  --protocol tcp --port 80 --cidr $i/32
                		elif [ $count -lt $NUMBER ]
                		then
                        		aws ec2 authorize-security-group-ingress --group-id ${SEC_GROUP_ID2}  --protocol tcp --port 80 --cidr $i/32
                		else
                        		exit 1
                		fi
                		count=$(( $count + 1 ))
				sleep 1
			done
		fi
else

	WAN=`curl -s https://s3.amazonaws.com/nr-synthetics-assets/nat-ip-dnsname/production/ip.json | jq .[][] -r`
	NUMBER=`curl -s https://s3.amazonaws.com/nr-synthetics-assets/nat-ip-dnsname/production/ip.json | jq .[][] -r | wc -l`
	# create the file
	echo ${WAN} > ${WORKDIR}/.newrelicip
	# set the variable so we can add the ip to the systems security group
	NEWIP=`cat ${WORKDIR}/.newrelicip`
	# and set the new ip address for ssh access
	count=0
	for i in $NEWIP
	do
        	echo $i $count adding rule
        	if [ $count -lt 40 ]
        	then
                	aws ec2 authorize-security-group-ingress --group-id ${SEC_GROUP_ID1}  --protocol tcp --port 80 --cidr $i/32
        	elif [ $count -lt $NUMBER ]
        	then
                	aws ec2 authorize-security-group-ingress --group-id ${SEC_GROUP_ID2}  --protocol tcp --port 80 --cidr $i/32
        	else
                	exit 1
        	fi
		count=$(( $count + 1 ))
		sleep 1
	done
fi
