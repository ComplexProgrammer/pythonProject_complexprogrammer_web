from website import app, socketio

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.106', port=5000)
    socketio.run(app, host='192.168.1.106', port=5000)
