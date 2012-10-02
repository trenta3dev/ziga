from flask import Response, json, render_template, jsonify, request

from ziga import app, redis


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

    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Credentials'] = 'true'
#    headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
#    headers["Access-Control-Allow-Headers"] = "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control"

    return Response(generate(), mimetype="text/event-stream", headers=headers)


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
