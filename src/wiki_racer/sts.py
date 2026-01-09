import sys
from sentence_transformers import SentenceTransformer
import wikipediaapi
import nltk.data
import torch
wikipediaapi.log.setLevel(level=wikipediaapi.logging.DEBUG)


model = SentenceTransformer("all-MiniLM-L6-v2")

# Set handler if you use Python in interactive mode
out_hdlr = wikipediaapi.logging.StreamHandler(sys.stderr)
out_hdlr.setFormatter(wikipediaapi.logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(wikipediaapi.logging.DEBUG)
wikipediaapi.log.addHandler(out_hdlr)

# get wikipedia summary
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='wiki-racer (https://github.com/plasmavolt/wiki-racer)',
    language='en',
    extra_api_params={'plnamespace': 0},
)
page_end = wiki_wiki.page('Gyros')
page_end_summary = page_end.summary
page_end_text = page_end.text
# print(page_end_summary)

# get links on curr page
page_curr = wiki_wiki.page('Mathematics')
page_curr_links = list(page_curr.links.keys())
# print(page_curr_links)

# tokenize wikipedia summary
page_end_summary_sentences = nltk.tokenize.sent_tokenize(page_end_summary)
page_end_text_sentences = nltk.tokenize.sent_tokenize(page_end_text)

# compare to wikipedia summary
page_end_summary_embeddings = model.encode(page_end_summary_sentences, convert_to_tensor=True)
page_end_text_embeddings = model.encode(page_end_text_sentences, convert_to_tensor=True)
page_curr_links_embeddings = model.encode(page_curr_links, convert_to_tensor=True)
similarities = model.similarity(page_curr_links_embeddings, page_end_text_embeddings)
avg_similarities = similarities.mean(dim=1)
max_similarities = similarities.max(dim=1).values

# get top k best links, k = 10
k = 10
page_curr_links_best = torch.topk(max_similarities, k).indices

# print top k best links
for idx in page_curr_links_best:
    link = page_curr_links[idx]
    score = max_similarities[idx].item()
    print(f"{link}: {score:.4f}")

# take top k and rank based on word similarity

    
# class PathOptimizer:
#     def __init__(self):
        