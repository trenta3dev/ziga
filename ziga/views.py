from flask import Response, json, render_template, jsonify, request

from ziga import app, redis


@app.route('/sse/', methods=['GET'])
def sse():
    from time import sleep

    def generate():
        while True:
            sleep(2)
            yield 'data: ' + json.dumps({'hello': 'world'}) + '\n\n'

    return Response(generate(), mimetype="text/event-stream")


@app.route('/<string:app_key>/<string:channel>/', methods=['GET'])
def sse(app_key, channel):
    def generate():
        pubsub = redis.pubsub()
        pubsub.subscribe('{}:{}'.format(app_key, channel))
        for data in pubsub.listen():
            print data

            if not data['type'] == 'message':
                continue

            out = {}
            json_ = json.loads(data['data'])
            out['data'] = json_['data']
            out['channel'] = data['channel']
            out['event'] = json_['event']
            yield 'data: ' + json.dumps(out) + '\n\n'

    return Response(generate(), mimetype="text/event-stream")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<string:app_key>/<string:channel>/', methods=['POST'])
def create_event(app_key, channel):
    print app_key, channel, request.json

    data = request.json

    event = data.get('event')

    if not event:
        return Response(status=400)

    redis.publish('{}:{}'.format(app_key, channel, event), json.dumps(data))

    return jsonify(success=True), 201
