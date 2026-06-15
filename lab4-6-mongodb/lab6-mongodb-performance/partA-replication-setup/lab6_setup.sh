#!/bin/bash

# Setup directories
mkdir -p ./data/rs1 ./data/rs2 ./data/rs3
mkdir -p ./data/shard1 ./data/shard2 ./data/config

# Replica set
# mongod --port 27017 --dbpath ./data/rs1 --replSet rs0 &
# mongod --port 27018 --dbpath ./data/rs2 --replSet rs0 &
# mongod --port 27019 --dbpath ./data/rs3 --replSet rs0 &

# Sharding
# mongod --port 27020 --dbpath ./data/shard1 --shardsvr &
# mongod --port 27021 --dbpath ./data/shard2 --shardsvr &
# mongod --port 27022 --dbpath ./data/config --configsvr &
# mongos --port 27023 --configdb localhost:27022 &
