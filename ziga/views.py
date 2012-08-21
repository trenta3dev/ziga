from flask import Response, json, render_template

from ziga import app


@app.route('/sse/', methods=['GET'])
def sse():
    from time import sleep
    def generate():
        while True:
            sleep(2)
            yield 'data: ' + json.dumps({'hello': 'world'}) + '\n\n'

    return Response(generate(), mimetype = "text/event-stream")


@app.route('/', methods=['GET'])
def index():
    return render_template('Index.html')
