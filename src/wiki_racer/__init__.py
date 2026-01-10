import nltk
import os

# Configure nltk data path
NLTK_DATA_PATH = "./.venv/share/nltk_data/"
nltk.data.path.insert(0, NLTK_DATA_PATH)

# Download if not already present
if not os.path.exists(os.path.join(NLTK_DATA_PATH, "tokenizers/punkt_tab")):
    nltk.download("punkt_tab", download_dir=NLTK_DATA_PATH)
