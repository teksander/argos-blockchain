# ARGoS-Blockchain interface: Blockchain module

This blockchain module allows for creating an Ethereum network with several nodes using Docker containers.

Its goal is to be interfaced with robot controllers in the ARGoS simulator:
https://github.com/ilpincy/argos3

The interface of the Docker containers with ARGoS is done in Python, using the code in the following repository:
https://github.com/teksander/geth-argos


This module can also be used independently of ARGoS
- for debbuging
- playing around with an Ethereum network and Docker containers
- to interface with something other than ARGoS


## Setup

The very first time you run this code, it is required to create the
Docker image for the Ethereum nodes and initialize Docker Swarm as
follows:

```
cd geth/
docker build -t mygeth .
docker swarm init
```

Additionally, you have to set the variable `DOCKERFOLDER` in
the file `blockchainconfig` to the full path where this
repository is located on your computer, for example:

```
/<username>/repos/argos-blockchain/
```

This version is currently using Ethereum PoA. To use PoW, an different version is availiable at:
https://github.com/Pold87/blockchain-swarm-robotics


## Run

Usually, the network is created when a swarm robotics experiment is launched 
(see file: https://github.com/teksander/geth-argos/blob/latest/MarketForaging/reset-geth)

However, you can also start the Ethereum network without ARGoS, using
the following command:

```bash local/start_network.sh <number of nodes>```

That is, `bash local/start_network.sh 5`, would
create a private Ethereum network with 5 nodes.
