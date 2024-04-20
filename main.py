import os
from functions import pdf_read
from functions import text_split
from llm import google_gemini
import chromadb

# # 设置代理
# port = os.getenv('PORT')
# os.environ['HTTP_PROXY'] = f'http://localhost:{port}'
# os.environ['HTTPS_PROXY'] = f'http://localhost:{port}'

# 读取PDF
path = 'pdf/merge.pdf'
file_name = path.split('/')[-1]
file_name, extension = os.path.splitext(file_name)
text = pdf_read.get_pdf_text(path)

# 拆分文本
chunks = text_split.get_text_chunks(text)
 
# Set up the DB
db = google_gemini.get_chunks_vec(chunks, f"{file_name}")

query_zh = '玩具模型'
query = google_gemini.zh_to_en(query_zh)

passage = google_gemini.get_relevant_passage(query, db)
passage = ''.join(passage)
print(passage)
prompt = google_gemini.make_prompt(query, passage)
print(prompt)
answer = google_gemini.get_response(prompt)
print(answer)



# db_loaded = chromadb.PersistentClient(path='./chroma', database=db)

# print(type(db_loaded))
# print(pd.DataFrame(db_loaded.peek(len(chunks))))