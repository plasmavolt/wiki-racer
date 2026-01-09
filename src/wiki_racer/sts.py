from sentence_transformers import SentenceTransformer
from wikipedia import wiki_wiki
import nltk.data
import torch
from collections import deque


model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up target page and encode its text
page_end = wiki_wiki.page('Gyros')
page_end_text = page_end.text
page_end_text_sentences = nltk.tokenize.sent_tokenize(page_end_text)
page_end_text_embeddings = model.encode(page_end_text_sentences, convert_to_tensor=True)

# Initialize queue and seen set
queue = deque()
seen = set()
k = 10

# Add starting page to queue
queue.append('Mathematics')

while queue:
    # Get current page from queue
    curr_page_title = queue.popleft()

    if curr_page_title in seen:
        continue
    seen.add(curr_page_title)

    print(f"\nProcessing: {curr_page_title}")

    # Check if we reached the target
    if curr_page_title == 'Greek alphabet':
        print("Found target page!")
        break

    # Get links on current page
    page_curr = wiki_wiki.page(curr_page_title)
    page_curr_links = list(page_curr.links.keys())

    if not page_curr_links:
        print("  No links found")
        continue

    # Encode and compare links to target page
    page_curr_links_embeddings = model.encode(page_curr_links, convert_to_tensor=True)
    similarities = model.similarity(page_curr_links_embeddings, page_end_text_embeddings)
    max_similarities = similarities.max(dim=1).values

    # Get top k best links
    top_k = min(k, len(page_curr_links))
    page_curr_links_best = torch.topk(max_similarities, top_k).indices

    # Print and add top k to queue
    print(f"  Top {top_k} links:")
    for idx in page_curr_links_best:
        link = page_curr_links[idx]
        score = max_similarities[idx].item()
        print(f"    {link}: {score:.4f}")
        queue.append(link)
