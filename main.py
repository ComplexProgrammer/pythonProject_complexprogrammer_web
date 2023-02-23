# from website import app, socketio
from waitress import serve
from website import app, socketio, mode

if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True)
    else:
        serve(app, threads=2)
    socketio.run(app)
