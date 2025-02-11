from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/begin')
def start_task():

    start = request.args.get('start') # contacts starting from
    end = request.args.get('end') # contacts ending at
    # both inclusive

    print("starting")
    result = run_gui_script(start, end)

    return result

def run_gui_script(start, end):
    result = subprocess.run(
        f"python3 gui-automate.py -s {start} -e {end} message1.txt > logs.txt",
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
