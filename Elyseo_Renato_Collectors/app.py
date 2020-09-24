from flask import Flask, jsonify, json, request, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap

app = Flask( __name__)
app.config['MYSQL_HOST'] = 'localhost'
# A PORTA APONTA PARA A BASE CORRETA ( USERS 3308 )
app.config['MYSQL_PORT'] = '3308'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sys'
app.config['MYSQL_CHARSET'] = 'utf8'

mysql = MySQL(app)
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

def execsql(sql):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(str(sql))
    output  = cur.fetchall()
    cur.close()
    return json.dumps(str(output))

def execsqlone(sql):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(str(sql))
    output  = cur.fetchone()
    cur.close()
    return json.dumps(str(output))

@app.route('/collector/<id>', methods=['GET'])
def collector(id):    
    SQL = "select * from sys.collectors where id=%s and active = 1" % id 
    #print(SQL)
    user = json.loads(execsqlone(SQL))      
    #return str(user)
    print(user)
    if user:
        return user
    else:
        return str("USER NOT FOUND")
    #return str("USER NOT FOUND")

@app.route('/allcollectors', methods=['GET'])
def allcollectors():
    SQL = "select * from sys.collectors"
    return execsql(SQL)

if  __name__ == '__main__':
    # app.run()
    app.run(port=5002)