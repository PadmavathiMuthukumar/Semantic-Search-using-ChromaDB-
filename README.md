# Semantic-Search-using-ChromaDB-
A beginner-friendly semantic search project using Python and ChromaDB.

This project stores vehicle-related documents in a persistent ChromaDB collection and retrieves the most semantically relevant documents for a user's query.

## Project Overview

The project demonstrates the basic workflow of semantic search:

```text
Documents
   |
   v
Embedding Model
   |
   v
ChromaDB
   |
   v
Stored Embeddings
   |
   v
User Query
   |
   v
Query Embedding
   |
   v
Similarity / Distance Search
   |
   v
Top Relevant Documents
```

Unlike traditional keyword search, semantic search uses embeddings to compare the meaning of the query with the meaning of stored documents.

## Technologies Used

- Python
- ChromaDB
- NumPy
- Virtual Environment

## Project Structure

```text
semantic-chromadb/
|
├── venv/
|
├── chroma/
|   └── Persistent ChromaDB storage
|
├── add_data.py
├── query.py
├── requirements.txt
└── README.md
```

The exact file names may vary depending on how the project is organized.

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install chromadb numpy
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

## Storing Documents

The project creates a persistent ChromaDB client:

```python
import chromadb

client = chromadb.PersistentClient(path="chroma/")

collection = client.get_or_create_collection(name="vehicles")
```

The following documents are added:

```text
Car runs on petrol
Bus carries passengers on road
Bicycle runs without fuel
Boat travels on water
Plane flies in the sky
```

Each document is given a unique ID:

```text
car1
bus1
bike1
boat1
plane1
```

Example:

```python
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
```

## Querying the Collection

The user enters a natural-language query:

```python
query = input("Enter your query: ")
```

The query is sent to ChromaDB:

```python
result = collection.query(
    query_texts=[query],
    n_results=3
)
```

`n_results=3` tells ChromaDB to return the three closest matching documents.

## Example

Input:

```text
how does the car runs
```

Example output:

```text
Query Results
- Car runs on petrol (Distance: 0.8821218609809875)
- Bicycle runs without fuel (Distance: 1.4333001375198364)
- Bus carries passengers on road (Distance: 1.5820622444152832)
```

## Understanding the Result

ChromaDB converts the stored documents and the query into numerical vectors called embeddings.

For example:

```text
"Car runs on petrol"
        |
        v
[embedding vector]

"how does the car runs"
        |
        v
[query embedding]
```

ChromaDB compares the query embedding with the stored document embeddings and retrieves the closest documents.

For the example above:

```text
Car runs on petrol          -> 0.882
Bicycle runs without fuel   -> 1.433
Bus carries passengers      -> 1.582
```

For this distance metric:

```text
Lower distance = more similar
Higher distance = less similar
```

Therefore, `Car runs on petrol` is the closest result to the query.

The distance value should not be interpreted as a percentage.

For example:

```text
0.882 does not mean 88.2% similarity.
```

It is a distance value produced by the configured vector distance metric.

## How ChromaDB Handles Embeddings

The project does not manually create embeddings using a separate `model.encode()` call.

ChromaDB handles the embedding generation through its configured embedding function.

The general process is:

```text
Document
   |
   v
Embedding Function
   |
   v
Document Embedding
   |
   v
Stored in ChromaDB
```

When a query is submitted:

```text
User Query
   |
   v
Embedding Function
   |
   v
Query Embedding
   |
   v
Compare with Stored Embeddings
   |
   v
Rank Results
   |
   v
Return Top Results
```

## Why Manual Cosine Similarity Is Not Required

A separate experiment may manually calculate cosine similarity:

```python
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
```

This is useful for understanding how vector similarity works.

However, the current project uses:

```python
collection.query(
    query_texts=[query],
    n_results=3
)
```

ChromaDB performs the retrieval process internally.

The difference is:

```text
Manual cosine similarity:

Embedding A
     |
     v
cosine_similarity()
     ^
     |
Embedding B


ChromaDB semantic search:

User Query
     |
     v
Embedding
     |
     v
ChromaDB
     |
     v
Vector Search
     |
     v
Top Relevant Documents
```

Manual cosine similarity is useful for learning and experimentation, while ChromaDB provides the higher-level vector search functionality needed for a semantic search application.

## Semantic Search vs Keyword Search

Traditional keyword search primarily looks for matching words.

For example:

```text
Query:
What fuel does an automobile use?
```

A keyword-based system may not find:

```text
Car runs on petrol
```

because the query uses `automobile` and `fuel`, while the document uses `car` and `petrol`.

Semantic search converts the text into embeddings and compares their meaning.

Conceptually:

```text
automobile -> car
fuel       -> petrol
```

This allows semantically related content to be retrieved even when the exact words are different.

## Persistent Storage

The project uses:

```python
client = chromadb.PersistentClient(path="chroma/")
```

This means ChromaDB stores its data persistently inside the `chroma/` directory.

The collection can therefore be accessed again when the application is run later.

## Running the Project

First activate the virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

Run the script that creates the collection and adds the documents:

```powershell
python add_data.py
```

Then run the query script:

```powershell
python query.py
```

Enter a query when prompted:

```text
Enter your query: how does the car runs
```

## Learning Outcomes

This project demonstrates:

- What embeddings are
- How semantic search works
- How ChromaDB stores embeddings
- How a text query is converted into a vector representation
- How vector distance is used to retrieve relevant documents
- The difference between manual cosine similarity and database-level vector search
- How persistent vector storage works
- The basic retrieval stage used in a RAG application

## Future Improvements

The project can be extended by:

1. Allowing users to upload PDF or text files.
2. Splitting large documents into smaller chunks.
3. Generating embeddings for each chunk.
4. Storing the chunks in ChromaDB.
5. Searching the collection using natural-language questions.
6. Returning the most relevant chunks.
7. Connecting the retrieved chunks to an LLM.
8. Building a complete Retrieval-Augmented Generation (RAG) application.

## RAG Connection

This project currently focuses on the retrieval part of a RAG pipeline.

```text
User Question
      |
      v
Query Embedding
      |
      v
ChromaDB
      |
      v
Relevant Document Chunks
      |
      v
LLM
      |
      v
Final Answer
```

At the current stage, ChromaDB retrieves the relevant documents. An LLM can be added later to generate a natural-language answer using those retrieved documents as context.
