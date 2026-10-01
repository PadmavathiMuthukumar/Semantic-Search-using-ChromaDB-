import chromadb

# Connect to chroma Persistent storage
client = chromadb.PersistentClient(path="chroma/")

# create collection
collection=client.get_or_create_collection(name="vehicles")
print("Collection created successfully",collection.name)

# add data to the collection
collection.add(
documents=[
"Car runs on petrol",
"Bus carries passengers on road",
"Bicycle runs without fuel",
"Boat travels on water",
"Plane flies in the sky"
],
ids=["car1", "bus1", "bike1", "boat1", "plane1"]
)

print("Same Documents added to the collection",collection.name,"Successfully")