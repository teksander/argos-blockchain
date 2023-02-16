#!/bin/bash
set -e

geth --datadir=~/.ethereum/devchain init "/root/files/genesis_poa.json"
ip=`hostname -i`
GETH_OPTS=${@/KEYSTORE/$SLOT}
GETH_OPTS=${GETH_OPTS/IPADDRESS/$ip}

echo "Starting geth with options:"
echo "$GETH_OPTS"
geth $GETH_OPTS&

echo "Removing previous log files"
rm -rf root/logs/*

[ -f /root/python_scripts/on-start ] || bash /root/python_scripts/on-start

tail -f /dev/null


