from bottle import route, run

class index():
	@route('/', 'GET')
	def get():
		return '<h1>Hello!</h1>'

class greeter():
	@route('/greet/:name#.+#', 'GET')
	def get(name):
		return '<h1>Hello, %s!</h1>' % name.title()

run(host='localhost', port=8080)
