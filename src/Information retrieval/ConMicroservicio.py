from flask import Flask, jsonify,Response, request, send_file
from flasgger import Swagger
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import json
import bz2
import os
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
mongodb_host = "mongodb://localhost:11111/"
mongodb_dbname = "project_test"
myclient = pymongo.MongoClient(mongodb_host)
mydb = myclient[mongodb_dbname]
df=pd.DataFrame(columns=['idx', 'descripcion'])

# df_imput=[]
for i, documento in enumerate(mydb['publicacion'].find().sort([("ano_publiacion", pymongo.DESCENDING)])):
    # Añadir Cada Documento al la lista a usar en el df
    df.loc[i] = [documento['publicacion_id'],documento['descripcion']]
    # if i < 10:
      # print(documento)
    # df_imput.append([documento['publicacion_id'],documento['descripcion']])

#Añadimos al df a analizar
# df.descripcion=df_imput


corpus = df['descripcion'] # ['documento1', 'documento2', 'documento3',...'documento_']
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

vector = X
# df1 = pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names())

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

# df1 = pd.DataFrame(doc_vector.toarray(), columns=vectorizerX.get_feature_names())

# print(df.iloc[[1,2]]['idx'])

def fromDocToResult(doc):
  result = {
    'registration_id': doc['registration_id'],
    'publicacion_id': doc['publicacion_id'],
    'egresado_id': {
      'egresado_id': doc['egresado_id']['egresado_id'],
      'egresado_names': doc['egresado_id']['egresado_names'],
      'egresado_firstlastname': doc['egresado_id']['egresado_firstlastname']
    },
    'revista_id': doc['revista_id'],
    'institucion_id' : doc['institucion_id'],
    'date_id': doc['date_id'],
  }
  
  if 'similitud' in doc:
    result['similitud'] = doc['similitud']

  return result

@app.route('/get_RelatedDocs_data')
def get_RelatedDocs_data():
    """
    Obtener datos de IR en lista.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: false
        description: La consulta de búsqueda para los datos.
      - name: page
        in: query
        type: int
        required: false
        description: La página de resultados
    responses:
      200:
        description: Datos obtenidos correctamente
      500:
        description: Error al obtener los datos.
    """
    try:
    # Definir la URL del servicio con el token incluido
      query = request.args.get('query')
      currentPage = request.args.get('page', default=1, type=int)
      RESULTS_PER_PAGE = 10


      if not query:
        results = df.iloc[(currentPage-1)*RESULTS_PER_PAGE:currentPage*RESULTS_PER_PAGE]["idx"].values.tolist()
        data = []
        
        for doc in mydb['registro_publicaciones'].find({'publicacion_id.publicacion_id': {'$in': results}},{'_id': 0}).sort([("data_id", pymongo.DESCENDING)]):
          data.append(fromDocToResult(doc))
        
        return jsonify(data)

      query = get_tokenized_list(query)
      query = remove_stopwords(query)
      q = []
      for w in word_stemmer(query):
        q.append(w)
      q = ' '.join(q)
      query_vector = vectorizerX.transform([q])

      cosineSimilarities = cosine_similarity(doc_vector,query_vector).flatten()

      if currentPage == 1:
        related_docs_indices = cosineSimilarities.argsort()[-RESULTS_PER_PAGE * currentPage:]
      elif currentPage > 1:
        related_docs_indices = cosineSimilarities.argsort()[-RESULTS_PER_PAGE * currentPage:-RESULTS_PER_PAGE * (currentPage - 1)]
        
      numberResults = (cosineSimilarities > 0).sum()
      print("Number results: ", numberResults)

      data=[]

      # for i in related_docs_indices:
      #     data.append({
      #         "similarity": cosineSimilarities[i],
      #         "title": df.loc[i, 'descripcion']
      #     })

      # for publicacion in mydb['registro_publicaciones'].find({'publicacion_id.publicacion_id': {'$in': df.iloc[related_docs_indices]['idx'].values.tolist()}}, {'_id': 0}):
      #   publicacion["similarity"] = cosineSimilarities[df.loc[df['idx'] == publicacion['publicacion_id']['publicacion_id']].index[0]]
      #   print(df.loc[df['idx'] == publicacion['publicacion_id']['publicacion_id']].index[0])
      #   # print(related_docs_indices)
      #   data.append(publicacion)

      # print(df.iloc[568]["idx"])

      for i in related_docs_indices:
        if cosineSimilarities[i] == 0:
          continue
        doc = next(mydb['registro_publicaciones'].find({'publicacion_id.publicacion_id': df.iloc[i]["idx"]}, {'_id': 0}),None)
        if not doc:
          print("Doc with id", df.iloc[i]["idx"], "not found...")
          continue
        doc["similitud"] = cosineSimilarities[i]
                   
        data.append(fromDocToResult(doc))

      # print(len(data))
      # print(df.iloc[related_docs_indices]["idx"].values.tolist())

      #   print(related_docs_indices)
      #   print(df.iloc[i]['idx'])
      #   #   print(doc)
        
      # print(df.iloc[related_docs_indices[0]]['descripcion'])

      return jsonify(sorted(data, key=lambda x: x["similitud"], reverse=True)), 200

    except Exception as e:
          return jsonify({"error": str(e)}), 500

@app.route('/get_RelatedDocs_size')
def get_RelatedDocs_size():
    """
    Obtener numero de resultados de IR en lista.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: false
        description: La consulta de búsqueda para los datos.
    responses:
      200:
        description: Datos obtenidos correctamente
      500:
        description: Error al obtener los datos.
    """
    try:
    # Definir la URL del servicio con el token incluido
      query = request.args.get('query')

      if not query:
        return jsonify({'results_size': int(df.shape[0])})

      query = get_tokenized_list(query)
      query = remove_stopwords(query)
      q = []
      for w in word_stemmer(query):
        q.append(w)
      q = ' '.join(q)
      query_vector = vectorizerX.transform([q])

      cosineSimilarities = cosine_similarity(doc_vector,query_vector).flatten()
      return jsonify({'results_size': int((cosineSimilarities > 0).sum())})

    except Exception as e:
          return jsonify({"error": str(e)}), 500

@app.route('/download_RelatedDocs_data')
def download_RelatedDocs_data():
    """
    Descargar datos del IR en formato JSON.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: La consulta de búsqueda para los datos.
    responses:
      200:
        description: Archivo JSON de datos descargado correctamente
        schema:
          type: file
      500:
        description: Error al obtener los datos
    """
    try:
        # Obtener el parámetro query de la solicitud
        query = request.args.get('query')

        # Procesar la query
        query = get_tokenized_list(query)
        query = remove_stopwords(query)
        q=[]
        for w in word_stemmer(query):
          q.append(w)  # Asegúrate de que word sea una cadena
        q = ' '.join(q)  # Unir la lista de palabras en una sola cadena
        # Vectorizar la query
        query_vector = vectorizerX.transform([q])

        # Calcular la similaridad del coseno
        cosineSimilarities = cosine_similarity(doc_vector, query_vector).flatten()
        related_docs_indices = cosineSimilarities.argsort()[:-6:-1]  # Ajuste para obtener los 5 primeros documentos

        # Construir la respuesta con los datos similares
        data = []
        for i in related_docs_indices:
            data.append({
                "similarity": cosineSimilarities[i],
                "title": df.loc[i, 'descripcion']
            })

        # Crear el directorio si no existe
        output_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Definir la ruta del archivo JSON
        output_file = os.path.join(output_dir, 'related_docs.json')

        # Guardar los datos en el archivo JSON
        with open(output_file, 'w') as f:
            json.dump(data, f)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
