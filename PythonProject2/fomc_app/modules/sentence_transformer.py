from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Initialize embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# FAISS Index Initialization
dimension = 384  # Embedding size for the model
index = faiss.IndexFlatL2(dimension)  # Use L2 distance for similarity search
metadata = []  # To store corresponding metadata (e.g., paragraph ID or text)


def store_in_faiss(paragraphs, metadata_file="metadata.pkl", index_file="faiss_index"):
    """
    Generate embeddings for paragraphs and store them in FAISS along with metadata.
    """
    global metadata
    # Generate embeddings
    embeddings = model.encode(paragraphs)

    # Add embeddings to the FAISS index
    index.add(embeddings)

    # Attach metadata
    metadata.extend(paragraphs)

    # Save FAISS index and metadata
    faiss.write_index(index, f"{index_file}.index")
    with open(metadata_file, "wb") as f:
        pickle.dump(metadata, f)

    print(f"FAISS index saved to '{index_file}.index' and metadata saved to '{metadata_file}'.")


# Example usage:
paragraphs = [
    "The FOMC decided to maintain interest rates at 5.25%.",
    "Inflation expectations have declined compared to last quarter.",
    "GDP growth was revised downward due to tighter credit conditions.",
    "The Federal Reserve is monitoring labor market trends closely.",
]
store_in_faiss(paragraphs)


def query_faiss(query, metadata_file="metadata.pkl", index_file="faiss_index", top_k=5):
    """
    Query FAISS index to retrieve the most relevant paragraphs for a given query.
    """
    # Load FAISS index and metadata
    faiss_index = faiss.read_index(f"{index_file}.index")
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)

    # Generate query embedding
    query_embedding = model.encode([query])

    # Search FAISS index
    distances, indices = faiss_index.search(query_embedding, top_k)

    # Retrieve top-k results
    results = [{"text": metadata[idx], "distance": distances[0][i]} for i, idx in enumerate(indices[0])]
    return results


# Example query:
query = "What did the FOMC decide about interest rates?"
results = query_faiss(query)

# Print the results
print("\nTop Relevant Results:")
for result in results:
    print(f"Text: {result['text']} | Distance: {result['distance']:.4f}")

from openai import AzureOpenAI
from sentence_transformers import SentenceTransformer


class AzureOpenAIHelper:
    """
    Helper class for interacting with the Azure OpenAI service and integrating FAISS-based context retrieval.
    """

    AZURE_ENDPOINT = "https://hkust.azure-api.net"  # Replace with your endpoint
    API_VERSION = "2024-06-01"  # API version
    DEFAULT_MODEL = "gpt-4o-mini"  # Default model to use

    def __init__(self, api_key, faiss_index_path="faiss_index.index", metadata_path="metadata.pkl"):
        """
        Initialize the AzureOpenAIHelper instance.

        Args:
            api_key (str): Your Azure OpenAI API key.
            faiss_index_path (str): Path to the FAISS index file.
            metadata_path (str): Path to the metadata file.
        """
        self.client = AzureOpenAI(
            azure_endpoint=self.AZURE_ENDPOINT,
            api_version=self.API_VERSION,
            api_key=api_key
        )
        self.faiss_index_path = faiss_index_path
        self.metadata_path = metadata_path
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Load FAISS index and metadata
        self.index = faiss.read_index(self.faiss_index_path)
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def retrieve_context(self, query, top_k=5):
        """
        Retrieve relevant context from FAISS index based on the user's query.

        Args:
            query (str): User's query.
            top_k (int, optional): Number of top results to retrieve. Defaults to 5.

        Returns:
            str: Concatenated relevant paragraphs as context.
        """
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.metadata[idx] for idx in indices[0]]
        return "\n".join(results)

    def get_response(self, message, instruction, model=None, temperature=1.0, include_context=True):
        """
        Send a chat completion request to Azure OpenAI with optional FAISS-based context augmentation.

        Args:
            message (str): User's input message.
            instruction (str): System's role or guiding instruction.
            model (str, optional): Model to use. Defaults to DEFAULT_MODEL.
            temperature (float, optional): Sampling temperature. Defaults to 1.0.
            include_context (bool, optional): Whether to include FAISS-retrieved context. Defaults to True.

        Returns:
            str: AI-generated response.
        """
        model = model or self.DEFAULT_MODEL

        try:
            # Retrieve context if required
            context = self.retrieve_context(message) if include_context else ""

            # Combine instruction, context, and user message into the prompt
            prompt = (
                f"You are an assistant providing real-time updates on FOMC meetings. Use the context below to "
                f"answer the user's question accurately:\n\n"
                f"Context:\n{context}\n\n"
                f"User Query:\n{message}\n\n"
                f"Instruction:\n{instruction}"
            )

            # Send API request
            response = self.client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt}
                ]
            )
            # Print token usage
            print(f"Token Usage: {response.usage}")
            # Return the response content
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error during API call: {e}")
            return None


# Example usage
if __name__ == "__main__":
    PRIMARY_KEY = "198ee87d93034da5a0a72a684483c44e"  # Replace with your actual key

    # Initialize the helper with FAISS paths
    ai_helper = AzureOpenAIHelper(
        api_key=PRIMARY_KEY,
        faiss_index_path="faiss_index.index",
        metadata_path="metadata.pkl"
    )

    # FOMC-specific instruction
    instruction = (
        "You are an assistant providing real-time updates on FOMC meetings. "
        "Summarize key discussions, decisions, and macroeconomic implications."
    )

    # Get a response for a specific question
    response = ai_helper.get_response(
        message="What are the latest insights on interest rates?",
        instruction=instruction
    )

    # Print the AI's response
    if response:
        print(f"AI Response: {response}")
