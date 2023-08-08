from flask import Flask, render_template, jsonify, request
import sqlite3
import sys

db_path = 'data.db'


app = Flask(__name__)

@app.route('/')
def home():
    return 'hola mundo desde mi broker simple'
@app.route('/borrardb')
def borrardb():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data (idsensor NUMERIC, timestamp DATETIME, temp NUMERIC)")
    con.commit()
    con.close()
    return 'base de datos borrada'

@app.route('/sensor_send_data', methods=['POST'])
def sensor_send():
    values = request.data
    print(values)
    a=str(request.values.get('id'))
    print(a.split(";")[0])
    print(a.split(";")[1].split("=")[1])
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO data VALUES(" + a.split(";")[0] + "," + "datetime('now')," + a.split(";")[1].split("=")[1] + "," + ")")
    con.commit()
    con.close()
    return "datos recibidos ok",201
@app.route('/consulardb')
def consulta():
     con = sqlite3.connect(db_path)
     cur = con.cursor()
     cur.execute("SELECT * from data;")
     lectura = cur.fetchall()
     con.commit()
     con.close()
     return str(lectura)

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0',port=80)
