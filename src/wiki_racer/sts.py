from sentence_transformers import SentenceTransformer
from wikipedia import wiki_wiki
import nltk.data
import torch
import torch.nn.functional as F


model = SentenceTransformer("all-MiniLM-L6-v2")

start = 'Measure (mathematics)'
end = 'Ludwig Ahgren'

# Set up target page and encode its text
page_end = wiki_wiki.page(end)
page_end_title = page_end.title  # Canonical title (handles redirects)
page_end_text = page_end.text
page_end_text_sentences = nltk.tokenize.sent_tokenize(page_end_text)
page_end_text_embeddings = model.encode(page_end_text_sentences, convert_to_tensor=True)

# Initialize stack for DFS and seen set
seen = set()
k = 3

def get_page_similarity(page_title):
    """Calculate how similar a page is to the target page."""
    page = wiki_wiki.page(page_title)
    page_text = page.text
    page_text_sentences = nltk.tokenize.sent_tokenize(page_text)
    page_text_embeddings = model.encode(page_text_sentences, convert_to_tensor=True)

    similarities = model.similarity(page_text_embeddings, page_end_text_embeddings)
    softmax_similarities = F.softmax(similarities, dim=1)
    weighted_avg = (similarities * softmax_similarities).sum(dim=1).mean().item()

    return weighted_avg, page

def dfs(curr_title, path, parent_similarity):
    """DFS with backtracking when relevance decreases."""
    page_curr = wiki_wiki.page(curr_title)
    curr_page_title = page_curr.title

    # Debug: show if redirect occurred
    if curr_title != curr_page_title:
        print(f"\n  Redirect: '{curr_title}' -> '{curr_page_title}'")

    if curr_page_title in seen:
        print(f"  Already visited: {curr_page_title}")
        return None
    seen.add(curr_page_title)

    # Calculate current page similarity to target
    curr_similarity, _ = get_page_similarity(curr_page_title)

    print(f"\nProcessing: {curr_page_title} (similarity: {curr_similarity:.4f}, parent: {parent_similarity:.4f})")

    # Check if we reached the target
    if curr_page_title == page_end_title:
        print(f"Found target page! Path: {' -> '.join(path + [curr_page_title])}")
        return path + [curr_page_title]

    # Abandon path if we're getting further from target
    if curr_similarity < parent_similarity * 0.9:  # 10% tolerance
        print(f"  Abandoning path - similarity decreased too much")
        return None

    # Get links on current page
    page_curr_links = list(page_curr.links.keys())

    if not page_curr_links:
        print("  No links found")
        return None

    # Encode and compare links to target page
    page_curr_links_embeddings = model.encode(page_curr_links, convert_to_tensor=True)
    similarities = model.similarity(page_curr_links_embeddings, page_end_text_embeddings)

    # Apply softmax weighted average
    softmax_similarities = F.softmax(similarities, dim=1)
    weighted_avg_similarities = (similarities * softmax_similarities).sum(dim=1)

    # Get top k best links
    top_k = min(k, len(page_curr_links))
    page_curr_links_best = torch.topk(weighted_avg_similarities, top_k).indices

    # Try top k links in order (DFS)
    print(f"  Top {top_k} links:")
    for idx in page_curr_links_best:
        link = page_curr_links[idx]
        score = weighted_avg_similarities[idx].item()
        print(f"    {link}: {score:.4f}")

        result = dfs(link, path + [curr_page_title], curr_similarity)
        if result:
            return result

    return None

# Start DFS
result_path = dfs(start, [], float("-inf"))
if result_path:
    print(f"\n=== SUCCESS ===")
    print(f"Path length: {len(result_path)}")
    print(f"Path: {' -> '.join(result_path)}")
else:
    print("\n=== FAILED ===")
    print("Could not find a path to the target")
