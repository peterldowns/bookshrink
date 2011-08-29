from bottle import route, run, view

class index():
	@route('/', 'GET')
	@route('/:name#.+#', 'GET')
	@view('index')
	def get(name="Stranger"):
		return dict(name=name)

run(host='localhost', port=8080)
