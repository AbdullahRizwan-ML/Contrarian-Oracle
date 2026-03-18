import os
from src.rag.vector_store import VectorStore

def main():
    store = VectorStore()
    ticker = "TSLA"
    
    # 1. UPDATED THE FILE NAME HERE
    file_path = "data/sample_transcripts/TSLA_Q4_2025.txt" 
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}. Please check the folder!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. UPDATED THE DATE HERE
    metadata = {"source": "Q4 Earnings Call", "date": "2025"}
    
    print(f"Chunking and uploading {ticker} transcript into local Vector Database...")
    chunks_created = store.ingest_transcript(ticker, text, metadata)
    print(f"✅ Success! Created {chunks_created} chunks in ChromaDB.")

if __name__ == "__main__":
    main()