#!/bin/bash  

# Change to this script's folder
cd $( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

source ../blockchainconfig

docker stack rm ethereum >/dev/null 2>&1

rm -f ${DOCKERBASE}/geth/my_enode.enode

sleep 1

docker stack deploy -c ${DOCKERBASE}/local/docker-compose.yml ethereum

docker service scale ethereum_eth=$1

docker ps -q

