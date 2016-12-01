from flask import Flask, request

from process import process
from slack_handler import send_slack_message

app = Flask(__name__)

@app.route('/', methods=["POST"])
def main():
    data = request.data
    response = process.controller(data)
    send_slack_message(response)
    return response

if __name__ == "__main__":
    app.run(port=9000, debug=True)