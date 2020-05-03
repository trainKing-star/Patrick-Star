from flask import Flask,request,jsonify
import base64
app = Flask(__name__)


@app.route('/',methods=['POST'])
def hello_world():
    data=request.form.get('data')
    print(data)
    return jsonify({'AAB':'true'})

if __name__ == '__main__':
    app.run()
