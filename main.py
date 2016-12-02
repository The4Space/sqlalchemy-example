# coding=utf-8
import simplejson as json

from flask import Flask, request

from process import process
from slack_handler import send_slack_message

app = Flask(__name__)

@app.route('/', methods=["POST"])
def main():
    data = request.data
    if type(data) == str:
        data = json.loads(data)
    response = process.controller(data["text"][0])
    send_slack_message(response)
    return response

if __name__ == "__main__":
    app.run(port=9000, debug=True)