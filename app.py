from flask import Flask,request
from flask_mysqldb import MySQL
from flask_restful import Api,Resource
from flask_cors import CORS
from model import model
app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'League123!'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] ='anime'
app.config['MYSQL_CURSORCLASS'] ='DictCursor'

mysql =  MySQL(app)
api = Api(app)
CORS(app)
class Anime(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM anime_data ORDER BY Rating DESC LIMIT 10''')
        result = cur.fetchall()
        return result
class Recommendation(Resource):
    def get(self,name,genre,episodes,producer,studio):
        kmeans = model(5)
        animes = kmeans.predict([name,genre,episodes,producer,studio])
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM anime_data WHERE Name = %s or Name = %s or Name = %s or Name = %s or Name = %s"
        val = animes["Names"].values.tolist()
        print(val)
        cur.execute(sql,tuple(val))
        result = cur.fetchall()
        return result
        
api.add_resource(Anime,'/api/anime')
api.add_resource(Recommendation,'/api/recommendation/<string:name>/<string:genre>/<string:episodes>/<string:producer>/<string:studio>')
if __name__ =="__main__":
    app.run(debug = True)
