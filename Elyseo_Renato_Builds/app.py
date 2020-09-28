from flask import Flask, jsonify, json, request, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap

app = Flask( __name__)

app_port = 5002

app.config['MYSQL_HOST'] = 'localhost'
# A PORTA APONTA PARA A BASE CORRETA ( BUILDINGS 3307 )
app.config['MYSQL_PORT'] = '3307'           
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sys'
app.config['MYSQL_CHARSET'] = 'utf8'

mysql = MySQL(app)
Bootstrap(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# @app.route("/")
# def hello():
#     return jsonify({"message":"HelloJson!"})
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def execsqlall(sql):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(str(sql))
    output  = cur.fetchall()
    cur.close()
    return json.dumps(output)

def execsqlone(sql):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(str(sql))
    output  = cur.fetchone()
    cur.close()
    return json.dumps(output)

def execsql(sql):
    cur = mysql.connection.cursor()
    cur.execute(str(sql))
    mysql.connection.commit()
    cur.close()    
    return "ok"

def next_id(table):
    SQL = "select coalesce(max(id)+1,1) id from sys.%s" % table 
    #print(SQL)
    newid = json.loads(execsqlone(SQL))
    #print(newid['id'])
    if newid:
       return newid['id']
    return -1

#-----------------------------------------------------------
#----------------------   BUILDS
#-----------------------------------------------------------

@app.route('/allbuilds', methods=['GET'])
def allbuilds():
    SQL = "select * from sys.builds"
    return execsqlall(SQL)

@app.route('/build/<id>', methods=['GET'])
def build(id):    
    SQL = "select * from sys.builds where id=%s and active = 1" % id 
    #print(SQL)
    user = json.loads(execsqlone(SQL))      
    #return str(user)
    print(user)
    if user:
        return user
    else:
        return str("BUILD NOT FOUND")

@app.route('/build/', methods=['POST'])
def insert():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        name = params['name']
        type = params['type']

        SQL = """insert into sys.builds (id, name, type, dtcreate)
        values(%s, '%s', '%s', now() ) """ % (next_id("builds"), name, type)
        return execsql(SQL)

    return "nops"

@app.route('/build/', methods=['PUT'])
def update():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        id = int(params['id'])
        name = params['name']
        type = params['type']
        dtcreate = params['dtcreate']        
        active = int(params['active'])
        SQL = """update sys.builds set 
        name = '%s',
        type = '%s',
        dtcreate = cast('%s' as datetime),       
        active = %s
        where id=%s """ % ( name, type, dtcreate, active, id)
        return execsql(SQL)

    return "nops"

@app.route('/build/<id>', methods=['DELETE'])
def delete(id):
    if (id):
        SQL = "delete from sys.builds where id=%s" % id
        return execsql(SQL)
    return "nops"

#-----------------------------------------------------------

#-----------------------------------------------------------
#----------------------   USER 
#-----------------------------------------------------------

@app.route('/user_builds', methods=['GET'])
def allusers():
    SQL = "select * from sys.users"
    return execsqlall(SQL)

@app.route('/user/<iduser>', methods=['GET'])
def user(iduser):    
    SQL = "select * from sys.users where iduser=%s and active=1" % iduser 
    user = json.loads(execsqlone(SQL))
    #return str(user)
    print(user)
    if user:
        return user
    else:
        return str("USER NOT FOUND")

@app.route('/user/', methods=['POST'])
def insert_user():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        iduser = int(params['iduser'])
        name = params['name']
        cpf = params['cpf']

        SQL = """insert into sys.users (id, iduser, name, cpf) 
        values(%s, '%s', '%s', now() ) """ % (next_id("users"), iduser, name, cpf)
        return execsql(SQL)

    return "nops"

@app.route('/user/', methods=['PUT'])
def update_user():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        iduser = int(params['iduser'])
        name = params['name']
        cpf = params['cpf']

        SQL = """update sys.users set 
        name = '%s',
        cpf = '%s',
        lastupd = now()
        where iduser=%s """ % ( name, cpf, iduser)
        return execsql(SQL)

    return "nops"

@app.route('/build/<iduser>', methods=['DELETE'])
def delete_user(iduser):
    if (id):
        SQL = "delete from sys.users where iduser=%s" % iduser
        return execsql(SQL)
    return "nops"

#-----------------------------------------------------------

#-----------------------------------------------------------
#----------------------   USER BUILDS
#-----------------------------------------------------------

@app.route('/user_builds', methods=['GET'])
def allusers():
    SQL = "select * from sys.user_builds"
    return execsqlall(SQL)

@app.route('/user/<iduser>', methods=['GET'])
def user(iduser):    
    SQL = "select * from sys.users where iduser=%s and active=1" % iduser 
    user = json.loads(execsqlone(SQL))
    #return str(user)
    print(user)
    if user:
        return user
    else:
        return str("USER NOT FOUND")

@app.route('/user/', methods=['POST'])
def insert_user():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        iduser = int(params['iduser'])
        name = params['name']
        cpf = params['cpf']

        SQL = """insert into sys.user_builds (id, iduser, name, cpf) 
        values(%s, '%s', '%s', now() ) """ % (next_id("user_builds"), iduser, name, cpf)
        return execsql(SQL)

    return "nops"

@app.route('/user/', methods=['PUT'])
def update_user():
    if (request.data):
        params = json.loads(request.data)
        print(params)
        iduser = int(params['iduser'])
        name = params['name']
        cpf = params['cpf']

        SQL = """update sys.user_builds set 
        name = '%s',
        cpf = '%s',
        lastupd = now()
        where iduser=%s """ % ( name, cpf, iduser)
        return execsql(SQL)

    return "nops"

@app.route('/build/<iduser>', methods=['DELETE'])
def delete_user(iduser):
    if (id):
        SQL = "delete from sys.user_builds where iduser=%s" % iduser
        return execsql(SQL)
    return "nops"

#-----------------------------------------------------------

if  __name__ == '__main__':
    # app.run()
    app.run(port=app_port)