import json

from flask import Flask, request
import threading


app = Flask(__name__)
db = {'oswalth': '1234'}


def run_app():
    server = threading.Thread(target=app.run, kwargs={
        "host": 'vk_api',
        "port": 5052
    })
    server.start()
    return server


@app.route('/vk_id/<username>', methods=['GET', 'POST'])
def index(username):
    if request.method == 'GET':
        if vk_id := db.get(username, None):
            return {'vk_id': vk_id}, 200
        return {}, 404
    elif request.method == 'POST':
        if db.get(username):
            return {}, 404
        else:
            db[username] = json.loads(request.data.decode()).get('vk_id', '2525')


if __name__ == '__main__':
    run_app()
