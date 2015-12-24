from inplace import app

app.run(host=app.config['LISTEN_HOST'], port=app.config['LISTEN_PORT'])
