from flask import Flask
from flask_mysqldb import MySQL
from flask_restful import Api,Resource
from flask_cors import CORS
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
        cur.execute('''SELECT * FROM anime_data ORDER BY score ASC LIMIT 5''')
        result = cur.fetchall()
        return result

api.add_resource(Anime,'/api')

if __name__ =="__main__":
    app.run(debug = True)
