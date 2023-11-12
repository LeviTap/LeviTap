from flask import Flask, render_template
from functions.touchless_mouse import touchless_mouse
from multiprocessing import Process

app = Flask("Touchless Mouse")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_function', methods=['POST'])
def run_function():
    # Your Python function logic goes here
    touchless_process = Process(target=touchless_mouse)
    touchless_process.start()
    return "Touchless Mouse function executed"


if __name__ == '__main__':
    app.run(debug=True)
