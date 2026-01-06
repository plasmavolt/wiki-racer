from sentence_transformers import SentenceTransformer
import wikipediaapi
import nltk.data

nltk.download('punkt_tab', download_dir='./.venv/share/nltk_data/')

model = SentenceTransformer("all-MiniLM-L6-v2")

# get wikipedia summary
wiki_wiki = wikipediaapi.Wikipedia(user_agent='wiki-racer (https://github.com/plasmavolt/wiki-racer)', language='en')
page_end = wiki_wiki.page('Ludwig_Ahgren')
page_end_summary = page_end.summary

# tokenize wikipedia summary
page_end_summary_sentences = nltk.tokenize.sent_tokenize(page_end_summary)


# compare to wikipedia summary
embeddings = model.encode(page_end_summary_sentences)
word_embedding = model.encode(["My name is Ludwig Ahgren"])
print(embeddings.shape)