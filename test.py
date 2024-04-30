from llm import google_gemini
import os
print(os.getenv('GOOGLE_API_KEY'))

ss = google_gemini.zh_to_en('你好')
print(ss)