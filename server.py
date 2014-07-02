#!/usr/bin/env python
# coding: utf-8
import os
import urllib2
from bottle import route, request, view, static_file, default_app, debug

import analysis # sentence analyzing logic


DEVELOPMENT = not os.environ.get('BOOKSHRINK_PRODUCTION')

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
        errorstring = """
            <h3 style="color:#CC0000">Analysis could not be completed.</h3>
            <h4>For the program to work, the input needs to be</h4> <h4>&mdash;
            a valid link to a .txt file</h4>
            <em><p>http://www.bookshrink.com/static/ihaveadream.txt</p></em>
            <h3>or</h3> <h4>&mdash; some amount of text that is at least one
            sentence long</h4> <em><p>This is a sentence.</p></em>
            """
        #postvars = web.input()
        postvars = request.forms
        input_string = postvars['input_string']
        if input_string[-4:] == '.txt' and len(input_string.split('\n')) == 1:
            if input_string[0:7] != 'http://':
                input_string = 'http://'+input_string
            try:
                response = urllib2.urlopen(input_string)
                input_string = response.read()
            except:
                # it wasn't a valid link, so revert to what the user
                # entered
                input_string = postvars['input_string']

        seed_string = postvars['seed_string'] or None

        num_results = float(postvars['num_results'])
        result_type = postvars['result_type']

        try:
            sa = analysis.SentenceAnalyzer(seed_string)
            sa.analyze(input_string)
            output = sa.get_results(result_type, num_results)
        except:
            if DEVELOPMENT:
                raise
            else:
                output = errorstring

        return output


if __name__ == '__main__':
    from bottle import run
    application = default_app()
    run(application,
        server='paste',
        host='127.0.0.1',
        port=8080,
        reloader=DEVELOPMENT,
        debug=DEVELOPMENT)
