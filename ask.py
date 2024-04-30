import os
from functions import save_and_load
from llm import google_gemini


# # 设置代理
# port = os.getenv('PORT')
# os.environ['HTTP_PROXY'] = f'http://localhost:{port}'
# os.environ['HTTPS_PROXY'] = f'http://localhost:{port}'

# 读取PDF
path = 'pdf/PhysRevE.106.014302.pdf'
file_name = path.split('/')[-1]
file_name, extension = os.path.splitext(file_name)


# load
loaded_em = save_and_load.load_vec(file_name)

query_zh = '本文创新点是什么'
query = google_gemini.zh_to_en(query_zh)

idx = google_gemini.get_relevant_passage(query, loaded_em)
passage = save_and_load.extract_text_from_pickle(file_name, idx)

prompt = google_gemini.make_prompt(query, passage)

answer = google_gemini.get_response(prompt)
print(answer)