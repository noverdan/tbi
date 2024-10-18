import re 
class InvertedIndex:
    def __init__(self):
        self.index ={}

    def add_document(self,doc_id,content):
        tokens = re.findall(r'\b\w+\b', content.lower())
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def search(self,query):
        tokens = re.findall(r'\W\w+\b', query.lower())
        tokens = sorted({elem.strip() for elem in tokens})

        results =set()
        for token in tokens:
            if self.index.get(token[1:]) is not None:
                if token.startswith('+'):
                    token = token[1:]
                    results = results.union(self.index[token])
                elif token.startswith('-'):
                    token = token[1:]
                    results = results.difference(self.index[token])
        return results


index = InvertedIndex()
index.add_document(1, "The quickly brown fox jumps over the lazy dog.")
index.add_document(2, "The five boxing wizards jumps quickly.")
index.add_document(3, "Pack my box with five dozen liquor jugs.")
index.add_document(4, "How quick daft jumping zebras vex.")
index.add_document(5, "Two driven jocks help fax my big quiz.")

print(index.search("+Quickly -fox +zebras +ada"))