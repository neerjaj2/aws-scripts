#!/bin/bash
sudo apt-get install python
python --version
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
pip --version
pip install awscli
/usr/local/bin/aws --version
pip install --upgrade awscli
which aws_completer
complete -C '/usr/local/bin/aws_completer' aws
mkdir ~/.aws
cat <<EOF >> ~/.aws/config
[default]
output = json
region = ap-southeast-1
EOF

