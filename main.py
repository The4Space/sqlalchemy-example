from flask import Flask, request

from process import process


app = Flask(__name__)

@app.route('/', methods=["POST"])
def main():
    data = request.data
    return process.controller(data)

if __name__ == "__main__":
    app.run(port=9000, debug=True)