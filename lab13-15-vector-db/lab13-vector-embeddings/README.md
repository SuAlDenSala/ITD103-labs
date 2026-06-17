# Lab 13: Vector Embeddings

This lab demonstrates how to generate vector embeddings for text using two different approaches:
1. **OpenAI API**: Uses the cloud-based `text-embedding-ada-002` model (requires a valid, funded API key).
2. **Sentence Transformers**: Uses a free, open-source model (`all-MiniLM-L6-v2`) that runs entirely on your local machine.

## Prerequisites
Make sure your environment is activated and dependencies are installed. Also, ensure the `datasets/articles.csv` file is present in the `lab13-15-vector-db/datasets/` directory.

## How to Run

### Option 1: Local Sentence Transformers (Free & Recommended)
To run the free, local implementation, run the following command from the `lab13-15-vector-db` directory:

```bash
python lab13-vector-embeddings/partB-generate-embeddings/lab13_sentence_transformers.py
```
*Note: The first time you run this, it will take a moment to download the local model weights.*

### Option 2: OpenAI API
To run the OpenAI version, first ensure you have added a valid API key to your `.env` file (`OPENAI_API_KEY="sk-..."`). Then run:

```bash
python lab13-vector-embeddings/partB-generate-embeddings/lab13_openai_embeddings.py
```
