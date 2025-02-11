from flask import Flask, render_template, request
import requests

app = Flask(__name__)

SERVER_URLS = ['http://127.0.0.1:8080/begin']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        message1 = request.form['message1']
        message2 = request.form['message2']
        message3 = request.form['message3']

        data = {
            'start': start,
            'end': end,
            'message1': message1,
            'message2': message2,
            'message3': message3
        }

        request_status = ""
        for i in range(len(SERVER_URLS)):
            response = requests.post(SERVER_URLS[i], json=data)

            if response.status_code == 200:
                request_status += f"Server {i+1}: Messages send successfully\n"
            else:
                request_status += f"Server {i+1}: Failed to send messages. Status Code: {response.status_code}\n"
        return f'<h3>{request_status}</h3>'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
