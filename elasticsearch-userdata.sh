#!/bin/bash

apt-get install software-properties-common python-software-properties -y
add-apt-repository ppa:webupd8team/java -y
apt-get update
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections
apt-get install oracle-java8-installer -y

wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.5/elasticsearch-2.3.5.deb
dpkg -i -E --force-confnew elasticsearch-2.3.5.deb

sudo update-rc.d elasticsearch defaults 95 10
cd /usr/share/elasticsearch/
#sudo bin/plugin install cloud-aws
sudo bin/plugin install lmenezes/elasticsearch-kopf/v2.1.1

cat >> /etc/default/elasticsearch << EOF
ES_HEAP_SIZE=4g
EOF

curl -sLo /usr/local/bin/ep https://github.com/kreuzwerker/envplate/releases/download/v0.0.8/ep-linux && chmod +x /usr/local/bin/ep

export HOSTNAME=$HOSTNAME
export IP=$(ec2metadata --local-ipv4)

cat >> /etc/elasticsearch/elasticsearch.yml  << EOF
  cluster.name: nb-stag-nile-elasticsearch-cluster
  node.name: ${HOSTNAME}
  network.host: ${IP}
  bootstrap.mlockall: true
  discovery.zen.ping.multicast.enabled: false
  discovery.zen.ping.unicast.hosts: ["Master1","Master2","Master3"]
  index.number_of_replicas: 2
  node.master: false
  node.data: true
  node.rack: ondemand
EOF

ep /etc/elasticsearch/elasticsearch.yml

service elasticsearch restart
