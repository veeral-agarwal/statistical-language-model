import stanza


def get_dependencies(doc, n):
    """Get dependencies in the format of a list of
    (token, deprel, dependent_token) pairs- 
    for all 'n' sentences in doc"""

    def getdeps(i):
        deps = []
        for head, rel, dep in doc.sentences[i].dependencies:
            deps.append((head.text, rel, dep.text))
        return deps

    return [getdeps(i) for i in range(n)]


def get_pos_tags(doc, n):
    """Get POS-tagged tokens in the format of a list of 
    (token, POStag) pairs for all sentences in doc.
    Returns upos (Universal part-of-speech) tag only, not 
    xpos (treebank-specific part of speech)"""

    def getpos(i):
        tokens = []
        for token in doc.sentences[i].words:
            tokens.append((token.text, token.upos))
        return tokens

    return [getpos(i) for i in range(n)]

# ==== MAIN: English ====
# stanza.download('en')
nlp_en = stanza.Pipeline('en') # This sets up a default neural pipeline in English
doc = nlp_en("Barack Obama was born in Hawaii.  He was elected president in 2008.")

# this prints the dependencies in a human-readable format
print(get_dependencies(doc, 2))

# this prints the POS-tagged sentence in a human-readable format
print(get_pos_tags(doc, 2))

# ==== MAIN: Hindi ====

# this sets up a default neural pipeline for Hindi
# stanza.download('hi')
nlp_hi = stanza.Pipeline('hi')
doc_hi = nlp_hi("नमस्ते तुम कैसे हो")

# this accesses the list of Token objects in the sentence
# for more on the data structures in a Document, see here:
# https://stanfordnlp.github.io/stanza/data_objects.html

#
print(doc_hi.sentences[0].tokens)
#

# this prints the dependency tree in a human-readable format

#
doc_hi.sentences[0].print_dependencies()
#

# same set of functions as above- but for Hindi
print(get_dependencies(doc_hi, 1))
print(get_pos_tags(doc_hi, 1))

