from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__, template_folder='Templates')
context_set = ""  # Use '=' for assignment, not ':'

@app.route('/', methods=['POST', 'GET'])  # Use '=' for assignment, not ':'
def index():
    if request.method == 'GET':
        val = request.args.get('text')  # Use '=' for assignment, not ':'
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}  # Use '=' for assignment, not ':'
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        response_data = res.json()  # Correct variable name from 'res' to 'response_data'
        #val = response_data[0]['text']  # Correct variable name from 'val' to 'response_data'
        if response_data:
         val = response_data[0]['text']
        else:
         val = "No response from the chatbot"

        return render_template('index.html', val=val)

if __name__ == '__main__':
    app.run(debug=True)
