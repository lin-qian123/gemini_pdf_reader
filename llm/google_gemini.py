import os
import numpy as np
import google.generativeai as genai



def embed_fn(text):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.embed_content(model='models/embedding-001',
                              content=text,
                              task_type="retrieval_document"
                              )["embedding"]

def get_chunks_vec(chunks):
    embeddings = [embed_fn(chunk) for chunk in chunks]
    return embeddings

# # translate chinese to english
# def zh_to_en(text):
#    translator = Translator(service_urls=['translate.google.com'], proxies={'http': None, 'https': None})
#    translated = translator.translate(text, dest='en')
#    return translated.text

# translate chinese to english
def zh_to_en(text):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    prompt = '''Please convert the Chinese in the text below into English to form a complete word or sentence. \
    Only reply with the translated result, no other words or sentences.\
    WORDS OR SENTENCES:'{text}'

    ANSWER:  
    '''.format(text=text)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

def en_to_zh(text):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    prompt = '''Please convert the English in the text below into Chinese to form a complete word or sentence. \
    Only reply with the translated result, no other words or sentences.\
    WORDS OR SENTENCES:'{text}'

    ANSWER:  
    '''.format(text=text)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

# Query the DB
def get_relevant_passage(query, embedings):
    query_embedding = genai.embed_content(model='models/embedding-001',
                                        content=query,
                                        task_type="retrieval_query")["embedding"]
    dot_products = np.dot(np.stack(embedings), query_embedding)
    sorted_indices = np.argsort(-dot_products)
    idx = sorted_indices[:10]
    return idx

def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, You can answer with your own knowledge, but it can't be irrelevant to the article. \
  If you are asked about the overall content of the document, you need to find summary sentences to summarize, and you can't focus on details.\
  You must answer the question in Chinese. \
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:  
  """).format(query=query, relevant_passage=escaped)

  return prompt

def get_response(prompt):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text