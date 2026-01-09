import sys
import wikipediaapi

wikipediaapi.log.setLevel(level=wikipediaapi.logging.DEBUG)
# Set handler if you use Python in interactive mode
out_hdlr = wikipediaapi.logging.StreamHandler(sys.stderr)
out_hdlr.setFormatter(wikipediaapi.logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(wikipediaapi.logging.DEBUG)
wikipediaapi.log.addHandler(out_hdlr)

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='wiki-racer (https://github.com/plasmavolt/wiki-racer)',
    language='en',
    extra_api_params={'plnamespace': 0},
)
