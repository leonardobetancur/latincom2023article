from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'hola mundo desde mi broker simple'
@app.route('/sensor_send_data', methods=['POST'])
def sensor_send():
    values = request.data
    print(values)
    return "datos recibidos ok",201

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0',port=80)
