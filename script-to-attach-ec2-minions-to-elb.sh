#!/bin/bash
LOAD_BALANCER_NAME=$(aws elb describe-load-balancers --output text --query 'LoadBalancerDescriptions[].[LoadBalancerName]' | grep k8s)
for elb in $LOAD_BALANCER_NAME
do
	echo "Adding instances to:"$elb
	Instance_Ids=$(aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=kubernetes-qa-minion" --query 'Reservations[].Instances[].[InstanceId]' --output text)
	for instance in $Instance_Ids
	do
        	echo $instance
        	aws elb register-instances-with-load-balancer --load-balancer-name $LOAD_BALANCER_NAME --instances $instance
        	i=0
        	while [ $i -lt 30 ]
        	do
        		STATUS=$(aws elb describe-instance-health --load-balancer-name $LOAD_BALANCER_NAME | grep $instance | awk '{print $5}')
                	if [ "$STATUS" == "InService" ]
                	then
                        	echo "Inservice"
				break
                	else
                        	echo "Out of service"
                	fi
                	i=$(( $i + 1 ))
                	sleep 3
        	done
	done
done
