from bottle import route, run
import pystache


class index():
	@route('/', 'GET')
	def get(self):
		return render.index()

class greeter():
	@route('/greet/:name#.+#', 'GET')
	def get(name):
		return pystache.render('<h1>Hello, {{person}}!</h1>', {'person':name})

run(host='localhost', port=8080)
