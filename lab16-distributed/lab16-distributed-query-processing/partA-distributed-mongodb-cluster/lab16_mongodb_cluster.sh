#!/bin/bash

# Create data directories
mkdir -p ./data/rs1 ./data/rs2 ./data/rs3

# Start three mongod instances (in separate terminals)
# Terminal 1:
# mongod --replSet rs0 --port 27017 --dbpath ./data/rs1 --bind_ip localhost

# Terminal 2:
# mongod --replSet rs0 --port 27018 --dbpath ./data/rs2 --bind_ip localhost

# Terminal 3:
# mongod --replSet rs0 --port 27019 --dbpath ./data/rs3 --bind_ip localhost

# In a new terminal, connect and initiate replica set
# mongosh --port 27017

# In mongo shell:
# rs.initiate({
#   _id: "rs0",
#   members: [
#     { _id: 0, host: "localhost:27017" },
#     { _id: 1, host: "localhost:27018" },
#     { _id: 2, host: "localhost:27019" }
#   ]
# })

# Check status
# rs.status()

echo "To set up the cluster, uncomment and run the commands above in separate terminals."
