import os
import textwrap
import chromadb
import numpy as np

import google.generativeai as genai
import google.ai.generativelanguage as glm

from IPython.display import Markdown
from chromadb import Documents, EmbeddingFunction, Embeddings

# from googletrans import Translator


def get_chunks_vec(chunks, name):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    documents = chunks
    class GeminiEmbeddingFunction(EmbeddingFunction):
        def __call__(self, input: Documents) -> Embeddings:
            model = 'models/embedding-001'
            title = "Custom query"
            return genai.embed_content(model=model,
                                        content=input,
                                        task_type="retrieval_document",
                                        title=title)["embedding"]
    
    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    for i, d in enumerate(documents):
        db.add(
        documents=[d],
        ids=[str(i)]
        )
    return db

# # translate chinese to english
# def zh_to_en(text):
#    translator = Translator(service_urls=['translate.google.com'], proxies={'http': None, 'https': None})
#    translated = translator.translate(text, dest='en')
#    return translated.text

# translate chinese to english
def zh_to_en(text):
    prompt = '''Please convert the Chinese in the text below into English to form a complete word or sentence. \
    Only reply with the translated result, no other words or sentences.\
    WORDS OR SENTENCES:'{text}'

    ANSWER:  
    '''.format(text=text)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

# Query the DB
def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=3)['documents'][0][0:2]
  return passage

def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it. \
  You must answer the question in Chinese. \
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:  
  """).format(query=query, relevant_passage=escaped)

  return prompt

def get_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text