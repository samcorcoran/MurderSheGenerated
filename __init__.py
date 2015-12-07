import json
from flask import Flask
from werkzeug.debug import get_current_traceback
from main import generateMystery

app = Flask(__name__)

@app.route('/cast/<int:num_players>')
def mystery(num_players):
    try:
        cast, result = generateMystery(num_players)
        print(result)
        return json.dumps(cast.toDict())
    except Exception as e:
        print(e)
        track = get_current_traceback(skip=1, show_hidden_frames=True,
            ignore_system_exceptions=False)
        track.log()
        abort(500)

if __name__ == '__main__':
    app.run()
