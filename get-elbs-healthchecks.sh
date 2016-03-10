#!/bin/bash
for i in `cat elb_dns_list.txt`
do
	ELB_NAME=$(aws elb describe-load-balancers | grep $i | awk '{print $5}')
	echo $i `aws elb describe-load-balancers --load-balancer-name $ELB_NAME --output text --query 'LoadBalancerDescriptions[].HealthCheck[].['Target']'`
done
