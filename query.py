# Getting the user query 
import chromadb


query = input("Enter your query: ")

# handling the query request
if query:
    print("Query received:",query)
else:
    print("No query received. Please enter a valid query")

client = chromadb.PersistentClient(path="chroma/")
collection = client.get_collection(name="vehicles")

# add the query to the collection
result=collection.query(
    query_texts=[query],
    n_results=1
)

print("Query Results")
for doc,dist in zip(result["documents"][0], result["distances"][0]):
    print(f"- {doc} (Distance: {dist})")