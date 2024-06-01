from flask import Flask, jsonify,Response, request
from flasgger import Swagger
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import json
import bz2
import pymongo
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

def get_tokenized_list(doc_text):
    tokens = nltk.word_tokenize(doc_text)
    return tokens

def word_stemmer(token_list):
  ps = nltk.stem.PorterStemmer()
  stemmed = []
  for words in token_list:
    stemmed.append(ps.stem(words))
  return stemmed

def remove_stopwords(doc_text):
  cleaned_text = []
  for words in doc_text:
    if words not in stop_words:
      cleaned_text.append(words)
  return cleaned_text

app = Flask(__name__)
swagger = Swagger(app)

# Importamos el Dataset de la base de Datos
mongodb_host = "mongodb://localhost:27017/"
mongodb_dbname = "fhiudshfihdsf"
myclient = pymongo.MongoClient(mongodb_host)
mydb = myclient[mongodb_dbname]
df=pd.DataFrame(columns=['descripcion'])

df_imput=[]
for documento in mydb['publicacion'].find():
    # Añadir Cada Documento al la lista a usar en el df
    df_imput.append(documento['descripcion'])

#Añadimos al df a analizar
df.descripcion=df_imput


corpus = df.loc[0:1000,'descripcion'] # ['documento1', 'documento2', 'documento3',...'documento_']
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

vector = X
df1 = pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names_out())

stop_words = set(stopwords.words('english'))

cleaned_corpus = []
for doc in corpus:
  tokens = get_tokenized_list(doc)
  doc_text = remove_stopwords(tokens)
  doc_text  = word_stemmer(doc_text)
  doc_text = ' '.join(doc_text)
  cleaned_corpus.append(doc_text)

vectorizerX = TfidfVectorizer()
vectorizerX.fit(cleaned_corpus)
doc_vector = vectorizerX.transform(cleaned_corpus)

df1 = pd.DataFrame(doc_vector.toarray(), columns=vectorizerX.get_feature_names_out())

query = "Friend mission wear success"


@app.route('/get_RelatedDocs_data')
def get_RelatedDocs_data():
    """
    Obtener datos de phishing.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: La consulta de búsqueda para los datos de phishing.
    responses:
      200:
        description: Datos de phishing obtenidos correctamente
      500:
        description: Error al obtener los datos de phishing
    """
    try:
    # Definir la URL del servicio con el token incluido
      query = request.args.get('query')

      query = get_tokenized_list(query)
      query = remove_stopwords(query)
      q = []
      for w in word_stemmer(query):
        q.append(w)
      q = ' '.join(q)
      q
      query_vector = vectorizerX.transform([q])

      cosineSimilarities = cosine_similarity(doc_vector,query_vector).flatten()
      related_docs_indices = cosineSimilarities.argsort()[:-6:-1]

      data=[]
      for i in related_docs_indices:
          data.append({
              "similarity": cosineSimilarities[i],
              "title": df.loc[i, 'descripcion']
          })

          return jsonify(data), 200

    except Exception as e:
          return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
