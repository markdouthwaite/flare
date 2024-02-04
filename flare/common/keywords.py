MACHINE_LEARNING = [
    "machine learning",
    "artificial intelligence",
    "data science",
    "llm",
    "generative ai",
    "gen ai",
    "mlops",
    "pytorch",
    "neural network",
    "deep learning",
    "large language models",
    "time series",
    "self-supervised learning",
    "tensorflow",
    "hugging face",
    "transformer model",
    "gpt",
    "google gemini",
    "deepmind",
    "image classification",
    "reinforcement learning",
    "pre-trained model",
    "neural text",
    "open ai",
    "openai",
    "image recognition",
    "speech recognition",
    "cuda",
    "jax",
    "keras",
    "machine intelligence",
    "google brain",
    "numpy",
    "diffusion model",
    "transformer block",
    "convolution block",
    "attention layer",
    "feed-forward layer",
    "unet",
    "text-to-image",
    "stable diffusion",
    "autoencoder"
]


def count_unique_hits(text: str, keywords: list) -> int:
    count = 0
    for keyword in keywords:
        if keyword in text:
            count += 1
    return count


def count_total_hits(text: str, keywords: list) -> int:
    tokens = [_.strip() for _ in text.lower().split()]
    counts = sum(_ in keywords for _ in tokens)
    return counts
