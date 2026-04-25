DOCUMENTS = [
    {
        "id": 1,
        "title": "Introduction to Neural Networks",
        "content": (
            "Neural networks are computing systems inspired by biological neural networks in animal brains. "
            "They consist of layers of interconnected nodes or 'neurons' that process information using connectionist "
            "approaches to computation. A neural network learns by adjusting the weights of connections between neurons "
            "based on training data. Deep learning refers to neural networks with many layers (deep architectures), "
            "which can learn increasingly abstract representations of data."
        ),
        "category": "deep_learning",
    },
    {
        "id": 2,
        "title": "Transformer Architecture",
        "content": (
            "The Transformer architecture, introduced in the 2017 paper 'Attention Is All You Need', revolutionized "
            "natural language processing. Unlike recurrent neural networks, Transformers use self-attention mechanisms "
            "to process all tokens in a sequence simultaneously, enabling much more efficient parallelization. "
            "The architecture consists of an encoder and decoder, each made up of multiple layers of multi-head "
            "attention and feed-forward networks. Positional encodings are added to give the model information "
            "about the order of tokens."
        ),
        "category": "nlp",
    },
    {
        "id": 3,
        "title": "Retrieval-Augmented Generation (RAG)",
        "content": (
            "RAG is a technique that enhances large language model outputs by retrieving relevant information "
            "from an external knowledge base before generating a response. Instead of relying solely on parametric "
            "knowledge stored in model weights, RAG systems dynamically fetch pertinent documents at inference time. "
            "This approach reduces hallucinations, enables up-to-date information access, and provides verifiable "
            "sources. A typical RAG pipeline involves: (1) indexing documents into a vector store, (2) retrieving "
            "top-k similar chunks for a query, and (3) passing retrieved context to an LLM for answer generation."
        ),
        "category": "rag",
    },
    {
        "id": 4,
        "title": "Vector Databases Explained",
        "content": (
            "Vector databases are purpose-built data stores that index and search high-dimensional vector embeddings. "
            "They are the backbone of semantic search and RAG systems. Unlike traditional databases that match exact "
            "values, vector databases use approximate nearest neighbor (ANN) algorithms like HNSW (Hierarchical "
            "Navigable Small World) to find semantically similar items quickly. Popular vector databases include "
            "Qdrant, Pinecone, Weaviate, and Chroma. Qdrant is an open-source, Rust-based vector database known "
            "for its performance and rich filtering capabilities."
        ),
        "category": "databases",
    },
    {
        "id": 5,
        "title": "Embeddings and Semantic Search",
        "content": (
            "Embeddings are dense vector representations of data (text, images, etc.) in a continuous vector space, "
            "where semantically similar items are geometrically close. Text embedding models like Google's "
            "text-embedding-004 convert sentences or paragraphs into fixed-size vectors (e.g., 768 or 1536 dimensions). "
            "Semantic search uses these embeddings to find results based on meaning rather than keyword overlap. "
            "Cosine similarity and dot product are common metrics for measuring vector similarity. High-quality "
            "embeddings are critical for effective RAG systems."
        ),
        "category": "embeddings",
    },
    {
        "id": 6,
        "title": "Reinforcement Learning from Human Feedback (RLHF)",
        "content": (
            "RLHF is a training technique used to align large language models with human preferences. "
            "The process involves three stages: (1) supervised fine-tuning on demonstration data, "
            "(2) training a reward model on human preference comparisons, and (3) optimizing the LLM "
            "using reinforcement learning (typically PPO) against the reward model. RLHF was key to "
            "the success of ChatGPT and Claude. It helps models become more helpful, harmless, and honest. "
            "Variants include DPO (Direct Preference Optimization), which skips the reward model entirely."
        ),
        "category": "alignment",
    },
    {
        "id": 7,
        "title": "Large Language Models and Prompt Engineering",
        "content": (
            "Large Language Models (LLMs) like GPT-4, Claude, and Gemini are trained on vast corpora of text "
            "to predict the next token. Prompt engineering is the practice of crafting inputs to elicit desired "
            "outputs from LLMs. Key techniques include: zero-shot prompting (direct instruction), few-shot "
            "prompting (providing examples), chain-of-thought prompting (asking for step-by-step reasoning), "
            "and system prompts (setting context and persona). Well-designed prompts significantly improve "
            "output quality, accuracy, and adherence to format requirements."
        ),
        "category": "llm",
    },
    {
        "id": 8,
        "title": "Fine-Tuning vs RAG: When to Use Each",
        "content": (
            "Fine-tuning and RAG are complementary techniques for adapting LLMs to specific tasks. "
            "Fine-tuning updates model weights on domain-specific data, making it ideal when you need "
            "a specific writing style, specialized vocabulary, or consistent behavior. However, it is "
            "expensive and the knowledge is static after training. RAG, on the other hand, retrieves "
            "live information at inference time — ideal for frequently updated knowledge bases, "
            "proprietary documents, or when source attribution is required. Many production systems "
            "combine both: a fine-tuned model with a RAG retrieval layer."
        ),
        "category": "rag",
    },
    {
        "id": 9,
        "title": "Attention Mechanisms in Deep Learning",
        "content": (
            "Attention mechanisms allow neural networks to dynamically focus on relevant parts of the input "
            "when producing an output. In sequence models, attention computes a weighted sum of values based "
            "on the compatibility between a query and a set of keys. Multi-head attention, used in Transformers, "
            "runs several attention operations in parallel (each 'head') and concatenates the results. "
            "Self-attention relates different positions within the same sequence, enabling the model to capture "
            "long-range dependencies that RNNs struggle with. Cross-attention allows the decoder to attend "
            "to encoder outputs."
        ),
        "category": "deep_learning",
    },
    {
        "id": 10,
        "title": "Chunking Strategies for RAG",
        "content": (
            "Effective chunking is critical for RAG performance. Documents must be split into chunks "
            "that are small enough to be precise but large enough to be semantically complete. Common "
            "strategies include: fixed-size chunking (splitting at a set token count), sentence-based "
            "chunking (splitting on sentence boundaries), recursive character splitting (splitting on "
            "paragraph then sentence boundaries), and semantic chunking (splitting at natural topic shifts "
            "using embedding similarity). Chunk overlap (e.g., 10-20%) between adjacent chunks helps "
            "preserve context across boundaries. The optimal chunk size depends on the embedding model "
            "and the nature of the content."
        ),
        "category": "rag",
    },
]
