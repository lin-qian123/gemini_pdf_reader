import chromadb


db_loaded = chromadb.PersistentClient(path='chroma/chroma.sqlite3')

print(type(db_loaded))