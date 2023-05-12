from flask import Flask
from flask import jsonify
from flask import request, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='login',
                            user='postgres',
                            password='19042003')
    return conn

@app.route('/')
def homeLogin():
    return render_template('form.html')

@app.route('/login_form')
def loginForm():
    return render_template('form.html')

@app.route("/login_json", methods=["POST"])
def login():
	username = request.json.get('username')
	password = request.json.get('password')
	print('username: ', username)
	print('password: ', password)
	
	conn = get_db_connection()
	cur = conn.cursor()
	strQuery = "SELECT * FROM users where username='%s' and password='%s';" % (username, password)
	print('strQuery: ',strQuery)
	cur.execute(strQuery)
	user = cur.fetchall()
	
	count = len(user)
	print('count: ', count)
	
	if count > 0:
		access_token = create_access_token(identity=username)
		print('access_token: ', access_token)
		# ~ return jsonify(access_token=access_token)
		return jsonify({"msg": access_token, 'berhasil':1}), 200
		
		
	print('Failed...')
	return jsonify({"msg": "Bad username or password", 'success':0})

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected/", methods=["POST"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/data_user/", methods=["POST"])
@jwt_required()
def data_user():
	conn = get_db_connection()
	cur = conn.cursor()
	strQuery = "select * from users"
	print('strQuery: ',strQuery)
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(strQuery)
	users = cur.fetchall()
	
	print('users: ', users)
	count = len(users)
	print('count: ', count)
	cur.close()
	conn.close()
	
	data = {'data_users': users, 'success':1}
	print('data: ', data)
	return jsonify(data), 200

@app.route("/data_konser/", methods=["POST"])
@jwt_required()
def data_peminjam():
	conn = get_db_connection()
	cur = conn.cursor()
	strQuery = "select * from konser"
	print('strQuery: ',strQuery)
	cur = conn.cursor(cursor_factory=RealDictCursor)
	cur.execute(strQuery)
	users = cur.fetchall()
	
	print('konser: ', users)
	count = len(users)
	print('count: ', count)
	cur.close()
	conn.close()
	
	data = {'data_konser': users, 'success':1}
	print('data: ', data)
	return jsonify(data), 200




if __name__ == "_main_":
    app.run(host='0.0.0.0')