#handle a POST request
from flask import Flask, render_template, request, url_for, jsonify
app = Flask(__name__)

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    print (request.headers)
    token = request.headers.get('Authorization')
    input_json = request.get_json(force=True) 
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print ('[MSG] Request header token:', token)
    print ('[MSG] Request json body:', input_json)
    return jsonify('Message Received')

if __name__ == '__main__':
    app.run(debug=True, port='8002')

