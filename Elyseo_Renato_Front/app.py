from flask import Flask, jsonify, json, request, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
# from flask_mysql_connector import MySQL

app = Flask( __name__)
# FRONT PORTA 5000
CORS(app, resources={r"/*": {"origins": "*"}})

Bootstrap(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route("/")
# def hello():
#df = mysql.execute_sql(SQL, to_pandas=True)
    #return str(df.to_dict())
    #return jsonify({"message":"HelloJson!"})
    
    #df = mysql.execute_sql(SQL, to_pandas=True)
    #user = df.to_dict()

@app.route('/user/<id>', methods=['GET'])
def user(id):    
    SQL = "select * from sys.users where id=%s and active = 1" % id 
    #print(SQL)
    return str("USER NOT FOUND") 

@app.route('/allusers', methods=['GET'])
def allusers():
    SQL = "select * from sys.users"
    return SQL

@app.route('/auth', methods=['POST'])
def autenticate():
    return str("AUTH FAIL")

if  __name__ == '__main__':
    # app.run()
    app.run(port=5000)