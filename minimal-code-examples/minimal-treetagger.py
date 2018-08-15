import pprint   # For proper print of sequences.
import treetaggerwrapper
#1) build a TreeTagger wrapper:
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
#2) tag your text.
tags = tagger.tag_text("This is a very short text to tag.")
#3) use the tags list... (list of string output from TreeTagger).
pprint.pprint(tags)