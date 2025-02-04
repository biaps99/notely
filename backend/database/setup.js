print("Initializing replica set...");
try {
    rs.initiate();
}
catch (e) {
    print("Replica set already initialized.");
}

// Wait for the primary node to be elected
sleep(6000);

print("Checking if index on folder_id already exists...");

var db = db.getSiblingDB("development");
var indexes = db.notes.getIndexes();
var indexExists = indexes.some(index => index.name === "folder_id_index");

if (!indexExists) {
    print("Creating index on folder_id in the notes collection...");
    db.notes.createIndex({ folder_id: 1 }, { name: "folder_id_index" });
}
