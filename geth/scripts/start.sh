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

echo "Starting analytics logging"
python3 /root/python_scripts/analytics.py $SLOT&

echo "Starting buffer for w3 interactions"
python3 /root/python_scripts/buffer.py&

echo "Starting web3 wrapper hosting"
python3 /root/python_scripts/wrapper.py&


tail -f /dev/null


