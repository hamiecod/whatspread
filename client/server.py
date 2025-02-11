from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/begin', methods=['GET', 'POST'])
def begin():
    data = request.json

    start = data.get('start', '')
    end = data.get('end', '')
    message1 = data.get('message1', '')
    message2 = data.get('message2', '')
    message3 = data.get('message3', '')

    print(f"start: {start}")
    print(f"end: {end}")
    print(f"message1: {message1}")
    print(f"message2: {message2}")
    print(f"message3: {message3}")

    #saving messages
    with open('message1.txt', 'w') as f1:
        f1.write(message1)

    with open('message2.txt', 'w') as f2:
        f2.write(message2)

    with open('message3.txt', 'w') as f3:
        f3.write(message3)

    print("starting")
    result = run_gui_script(start, end)

    return result

def run_gui_script(start, end):
    result = subprocess.run(
        f"python3 gui-automate.py -s {start} -e {end} message1.txt message2.txt message3.txt > logs.txt",
        shell=True,
        capture_output=True,
        text=True
    )

    return jsonify({
        'status': 'success',
        'stdout': result.stdout,
        'stderr': result.stderr
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
