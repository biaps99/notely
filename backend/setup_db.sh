#!/bin/bash

brew services start mongodb/brew/mongodb-community
echo "MongoDB service started."

code /opt/homebrew/etc/mongod.conf
echo "Will create a replica set. Please add the following to the config file and save it:"
echo "replication:"
echo "  replSetName: \"rs0\""

read -p "Press Enter after updating and saving the mongod.conf file."

brew services restart mongodb/brew/mongodb-community
echo "MongoDB service restarted with replication configuration."

echo "Initializing the replica set..."
mongosh --eval "rs.initiate()"
echo "Replica set initialized."

echo "Replica set status:"
mongosh --eval "rs.status()"

echo "Creating index on folder_id in the notes collection..."
mongosh --eval "db.notes.createIndex({ folder_id: 1 }, { name: 'folder_id_index' })"
echo "Index on folder_id created."