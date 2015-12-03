from flask import Flask
from main import generateMystery
from werkzeug.debug import get_current_traceback

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        result = generateMystery()
        print(result)
    except Exception as e:
        track= get_current_traceback(skip=1, show_hidden_frames=True,
            ignore_system_exceptions=False)
        track.log()
        abort(500)
    return result

if __name__ == '__main__':
    app.run()
