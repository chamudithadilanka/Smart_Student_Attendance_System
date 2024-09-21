import os
import subprocess
import sys

from flask import Flask

app = Flask(__name__)


@app.route('/get_name')
def get_name():

    script_path = os.path.join(os.path.dirname(__file__), "system.py")
    subprocess.run([sys.executable, script_path])
    with open('output.txt', 'r') as file:
        name = file.read()
        print("Name read from file:", name)

    return 'Your name'


if __name__ == '__main__':
    app.run(debug=True)
