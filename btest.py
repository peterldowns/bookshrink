from bottle import route, request, run, view, static_file

#debugging
from bottle import debug, run
debug(True)

class static_files():
	""" Serve static files """
	@route('/static/:path#.+#')
	def server_static(path):
	    return static_file(path, root='./static')

class index():
	# serves the main page
	@route('/', 'GET')
	@view('index')
	def get():
		return {}
	@route('/', 'POST')
	def post():
		print "request:"
		print request
		print "forms:"
		print request.forms


run(host='localhost', port=8080, reloader=True)
