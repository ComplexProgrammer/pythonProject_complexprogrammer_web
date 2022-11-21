from website import app, socketio

if __name__ == '__main__':
    app.run(debug=True, host='172.18.45.73', port=5000)
    socketio.run(app, host='172.18.45.73', port=5000)
