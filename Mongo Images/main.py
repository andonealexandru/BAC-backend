import base64
from pymongo import MongoClient

#LEGATURA CU MONGO
client = MongoClient("localhost", 27017)
db = client['marinel']
coll = db['user']

#DESCHIDEM IMAGINEA DORITA
#'rb' vine de la read bytes
with open("/home/istra/work/bac/test/Mongo Images/abc.jpg", "rb") as imageFile:
    #CONVERTIM IN BYTES
    string = base64.b64encode(imageFile.read())
    #INSERAM IN MONGO IMAGINEA CU BYTES
    coll.insert_one(
        {'img_as_bytes':string}
    )
    del string

#'wb' vine de la write bytes
with open("TEST.jpg", "wb") as fimage:
        #PRELUAM TOATE DOCUMENTELE DIN COLECTIE
        dictionar = coll.find()
        #cautam imaginea
        for w in dictionar:
            for key, value in w.items():
                if key == 'img_as_bytes':
                    string = value
        #VERIFICAM DACA MERGE TRASCRIIND INFORMATIA DIN IMAGINEA INCARCATA INTR-O IMAGINE NOUA
        fimage.write(base64.b64decode(string))
        