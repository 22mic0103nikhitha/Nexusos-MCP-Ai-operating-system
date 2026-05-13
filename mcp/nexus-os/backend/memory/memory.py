import chromadb

client = chromadb.Client()

collection = client.create_collection(
    name="memory"
)

def store_memory(text):
    """Store a text snippet in ChromaDB memory."""
    collection.add(
        documents=[text],
        ids=[str(hash(text))]
    )

def search_memory(query):
    """Search for relevant memories using ChromaDB."""
    return collection.query(
        query_texts=[query],
        n_results=3
    )

if __name__ == "__main__":
    # Test memory store
    store_memory("The user's name is Krishna Koushik.")
    store_memory("NexusOS is an MCP-based agentic OS.")
    
    results = search_memory("Who is the user?")
    print("Search results:", results['documents'])
