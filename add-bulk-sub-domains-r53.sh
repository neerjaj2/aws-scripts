#!/bin/bash
# Prerequisite: cli53 it can be downloaded from https://github.com/barnybug/cli53

cli53 export your-domain.com > .existing_records
for i in `cat sub-domain-list.txt`
do
	echo $i
	if grep $i existing_enteries.txt >> /dev/null
	then
		echo "Domain Exist"
	else
		echo "Create Sub Domain"
		cli53 rrcreate nbtools.com "$i CNAME `cat qa-elb-list.txt | grep $i`".""
	fi
done
