from flask import Flask
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


@app.route('/vk_id/<username>')
def index(username):
    if vk_id := db.get(username, None):
        return {'vk_id': vk_id}, 200
    return {}, 404


if __name__ == '__main__':
    run_app()
