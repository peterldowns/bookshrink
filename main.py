from bottle import route, request, run, view, static_file # web framework
import urllib2 # for downloading links
import sp # sentence analyzing logic

from bottle import debug
debug(True)

class static_files():
	# serves any static files

	@route('/static/:path#.+#')
	def serve(path):
	    return static_file(path, root='./static')

class index():
	# serves the main page
	@route('/', 'GET')
	@view('index')
	def get():
		return {}

	# analyzes any text sent to it
	@route('/', 'POST')
	def post():
		errorstring = 	"""
						<h3 style="color:#CC0000">Analysis could not be completed.</h3>
						<h4>For the program to work, the input needs to be</h4>
						<h4>&mdash; a valid link to a .txt file</h4>
						<em><p>http://www.bookshrink.com/static/ihaveadream.txt</p></em>
						<h3>or</h3>
						<h4>&mdash; some amount of text that is at least one sentence long</h4>
						<em><p>This is a sentence.</p></em>
						""" # show this message when the user messes up
		#postvars = web.input()
		postvars = request.forms
		input_string = postvars['input_string']
		if input_string[-4:] == '.txt' and len(input_string.split('\n')) == 1: # if the input looks like a link
			if input_string[0:7] != 'http://':
				input_string = 'http://'+input_string
			try:
				response = urllib2.urlopen(input_string)
				input_string = response.read()
			except:
				input_string = postvars['input_string'] # it wasn't a valid link, so revert to what the user entered
		
		seed_string = postvars['seed_string']
		if seed_string == "":
			seed_string = None 

		num_results = float(postvars['num_results'])
		result_type = postvars['result_type']
		
		try:
			sa = sp.sentenceAnalyzer(input_string, seed_string)
			sa.analyze()
			output = sa.get_results(result_type, num_results)
		except:
			output = errorstring
		return output

if __name__ == '__main__':
	run(host='localhost', port=8080)
