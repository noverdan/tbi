from main import MyDocument
import re

class ModifBooleanRetrieval(MyDocument):
    
    def bool_retrieval_search(self, query):
        results = set() # Membuat set kosong untuk menampung hasil pencarian
        if "and" in query.lower(): # Mengecek apakah kata "and" ada di dalam query 
            tokens = re.findall(r'\b(?!and\b)\w+\b', query.lower()) # Jika "and" ada maka ambil term yang ada di dalam query
            for token in tokens:
                if self.index.get(token) is not None: # Mengecek apakah kata yang dicari ada di dalam index
                    if not results:
                        results = self.index[token] # Jika results masih kosong maka hasil pencarian akan di isi dengan index[token]
                    else:
                        results = results.intersection(self.index[token]) # Jika results sudah ada maka hasil pencarian akan di intersection dengan index[token]
        
        if "or" in query.lower(): # Mengecek apakah kata "or" ada di dalam query
            tokens = re.findall(r'\b(?!or\b)\w+\b', query.lower()) # Jika "or" ada maka ambil term yang ada di dalam query
            for token in tokens:
                if self.index.get(token) is not None: # Mengecek apakah kata yang dicari ada di dalam index
                    if not results:
                        results = self.index[token] # Jika results masih kosong maka hasil pencarian akan di isi dengan index[token]
                    else:
                        results = results.union(self.index[token]) # Jika results sudah ada maka hasil pencarian akan di union dengan index[token]
        
        return results

document = ModifBooleanRetrieval()

document.add_inverted_index_doc("Record_1", "Term_1 Term_2 Term_4")
document.add_inverted_index_doc("Record_2", "Term_2 Term_3 Term_4")
document.add_inverted_index_doc("Record_3", "Term_1 Term_3 Term_4")
document.add_inverted_index_doc("Record_4", "Term_3 Term_4")

and_logic = document.bool_retrieval_search("Term_1 AND Term_3")
or_logic = document.bool_retrieval_search("Term_1 OR Term_2")

print(f"Term_1 AND Term_3: {and_logic}")
print(f"Term_1 OR Term_2: {or_logic}")