import json
from flask import Flask
from werkzeug.debug import get_current_traceback
from main import generateMystery

app = Flask(__name__, static_url_path='')

@app.route('/players/male/<int:num_male>/female/<int:num_female>')
def specific_mystery(num_male, num_female):
    try:
        cast, title, location, scene = generateMystery(num_male=num_male, num_female=num_female)
        return json.dumps({
            "cast": cast.toDict(),
            "title": title,
            "location": location,
            "scene": scene
            })
    except Exception as e:
        print(e)
        track = get_current_traceback(skip=1, show_hidden_frames=True,
            ignore_system_exceptions=False)
        track.log()
        abort(500)


@app.route('/players/<int:num_players>')
def random_mystery(num_players):
    try:
        cast, title, location, scene = generateMystery(num_players=num_players)
        return json.dumps({
            "cast": cast.toDict(),
            "title": title,
            "location": location,
            "scene": scene
            })
    except Exception as e:
        print(e)
        track = get_current_traceback(skip=1, show_hidden_frames=True,
            ignore_system_exceptions=False)
        track.log()
        abort(500)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
