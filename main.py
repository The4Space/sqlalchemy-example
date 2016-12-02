# coding=utf-8
from flask import Flask, request

from process import process
from slack_handler import send_slack_message

app = Flask(__name__)


@app.route('/', methods=["POST"])
def main():
    try:
        data = dict(request.form)
        response = process.controller(data["text"][0][1:])
        send_slack_message(response)
    except Exception as e:
        response = str(e)
        print(e)
    return response


if __name__ == "__main__":
    app.run(port=9000, debug=True)
