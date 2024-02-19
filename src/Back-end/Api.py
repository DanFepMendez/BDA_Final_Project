from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['local']
collection = db['egresados']

@app.get('/datos')
async def obtener_datos():
    # Consultar la colección en MongoDB
    resultados = list(collection.find({}))
    return resultados