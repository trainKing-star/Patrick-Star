from flask import Flask,request,jsonify
import base64
app = Flask(__name__)


@app.route('/',methods=['POST'])
def hello_world():
    file=request.files['file']
    file = file.read()
    file = base64.b64encode(file)
    file = str(file, 'utf-8')
    return jsonify({'photo':file})

if __name__ == '__main__':
    app.run()
