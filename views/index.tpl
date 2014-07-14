<!doctype html>
<html>
<head>
	<title>bookshrink</title>
	<meta name="description" content="finds the essence of any book or text" />
	<meta name="keywords" content="book, shrink, essence, summary, summarize, text, tf-idf" />

    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,700' rel='stylesheet' type='text/css'>
	<link rel="stylesheet" type="text/css" href="/static/1140.css" />
   	<link rel="stylesheet" type="text/css" href="/static/sexybuttons.css" />
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script type="text/javascript">
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-21305179-1', 'auto');
      ga('send', 'pageview');

    </script>
	<script type="text/javascript">
		$(document).ready(function() {
            var $input_string = $('#input_string');
            var $analyze_button = $('#analyze');
			$analyze_button.click(function() {
				$("#input_header").removeClass("twelvecol last").addClass("sixcol");
				$("#output_header").addClass("sixcol last").show();
				var i_s = $("textarea#input_string").val();
				var r_t = $("select#result_type").val();
				var n_r = $("select#num_results").val();
				var s_s = $("input#seed_string").val();
				$.ajax({
					type: "POST",
					timeout: 60000,
					data: {	input_string : i_s,
							result_type : r_t,
							num_results : n_r,
							seed_string : s_s},
					success: function(data) {
						$('#output').html(data).hide().fadeIn(1500);
					},
					error : function(obj, stat, err) {
						var desc = "";
						if(stat === "error"){
							desc = "The server was unreachable.";
						}
						else if(stat === "timeout"){
							desc = "The connection to the server timed out.";
						}
						else if(stat === "aborted"){
							desc = "The connection to the server was aborted.";
						}
						else if(stat === "parsererror"){
							desc = "The result was unable to be parsed.";
						}
						$('#output').html("<h3>Error: "+desc+"</h3><br><p>Please try a different text.</p>").hide().fadeIn(1000);
					},
				});
				return false;
			});
			$("#output_header").hide();
			$('#loading')
				.hide()  // hide it initially
    			.ajaxStart(function() {
					$("#loading").delay(500).show(); // delay some time so it doesn't always flicker up
				})
				.ajaxStop(function() {
					$("#loading").hide();
				});
			$("#toggle_output_options")
			$("#toggle_output_options").click(function(){$("#output_options").fadeToggle(500);});
			$("#output_options")
				.hide(); // hide the extra options initially
			});
	</script>

</head>

<body>
    <div class="row header"><a href="http://www.bookshrink.com/">
        <div id='title'>Bookshrink</div>
        <div id='tagline'>Find the Essence</div>
    </a></div>
	<div class="container">
    	<div class="row">
    		<div id="input_header" class="twelvecol last"><center>
				<div style="scroll;">
					<textarea id="input_string" rows="20" cols="55"
                      placeholder="Paste any text or a link to a .txt file"></textarea>
    			</div>
    			<br>
				<button id="analyze" class="sexybutton sexysimple sexyred sexyxxxl">Analyze my text !</button>
				<br>
				<br>
				<div id="toggle_output_options">
					<a>Toggle Advanced Options</a>
				</div>
				<div id="output_options">
					<select id="num_results" size="1">
						%for i in range(10, 30, 5):
							<option value=.{{i}}>{{i}} % of input</option>
						%end
						%for i in range(10, 15):
							<option value={{i}}>{{i}} sentences</option>
						%end
						<option selected value=15>15 sentences</option>
						%for i in range(16, 21):
							<option value={{i}}>{{i}} sentences</option>
						%end
					</select>
					<br>
					<select id="result_type" size="1">
						<option value="paragraph">Show sentences as a paragraph</option>
						<option value="individual">Show sentences individually</option>
						<option selected value="frequency">Show sentences with relative frequencies</option>
						<option value="highlight">Show original input with highlighted text</option>
					</select>
					<br>
					<p>Pre-weighted words (optional; comma-separated):</p>
					<input type="text" size=50 id="seed_string" />
				</div>
			</center></div>
			
			<div id="output_header" class="">
				<center>
					<div id="loading">
						<img src="/static/ajax-loader.gif" alt="Loading input (may take a while)"/>
						<p>We'll try to grab the text as fast as we can.</p>
						<p>The more text there is, the more time it will take.</p>
					</div>
				</center>
				<div id="output"></div>
			</div>
		</div> <!-- row -->
        <hr class="row"></hr>
		<div class="row">
			<div class="fourcol">
				<h3>How does the program work?</h3>
				<p>&mdash; The algorithm  cleans up the input text so that it can be analyzed.</p>
				<br><p>&mdash; Then, it finds the frequency of each word in the cleaned up text.</p>
				<br><p>&mdash; Each word is assigned a score based on a simple <a href="http://en.wikipedia.org/wiki/TF_IDF">TF-IDF</a> analysis.</p>
				<br><p>&mdash; Based on the scores of the words within them, a score is calculated for each sentence.</p>
				<br><p>&mdash; So that longer sentences aren't favored and shorter sentences aren't punished, the sentence scores are then normalized by length.</p>
				<br><p>&mdash; The sentences are sorted by their scores.</p>
				<br><p>&mdash; Finally, depending on what type of output is asked for, the program spits out the results.</p>
		
			</div>
			<div class="fourcol">
			
				<h3>What does this do?</h3>
				<p>The program tries to pick out the sentences of an input text that are most representative of the text as a whole; that is to say, find the essence of a text.</p>
				<br>
				<h3>Where can I get texts?</h3>
				<p><a href="http://www.gutenberg.org/browse/scores/top">Project Gutenberg</a> is an excellent resource for full books in the public domain.</p>
				<br>
				<p>Try copying any of these links into the input box above:</p>	
				<br>
                <ul>
                    <li><a href="http://www.bookshrink.com/static/ihaveadream.txt">"I Have A Dream"</a></li>
                    <li><a href="http://www.bookshrink.com/static/prideandprejudice.txt">Pride and Prejudice</a></li>
                    <li><a href="http://www.bookshrink.com/static/thejunglebook.txt">The Jungle Book</a></li>
                    <li><a href="http://www.bookshrink.com/static/wealthofnations.txt">An Inquiry into the Nature and Causes of the Wealth of Nations</a></li>
                    <li><a href="http://www.bookshrink.com/static/theiliad.txt">The Iliad</a></li>
                    <li><a href="http://www.bookshrink.com/static/robinsoncrusoe.txt">Robinson Crusoe</a></li>
                    <li><a href="http://www.bookshrink.com/static/obamastateofunion2011.txt">2011 State of the Union Address</a></li>
                </ul>
			</div>
			<div class="fourcol last">
				<h3>Who made this?</h3>
				<p><a href="http://peterdowns.com">Peter Downs</a></p>
				<br>	
				<h3>With what?</h3>
				<p> <a href="http://python.org/">Python</a>, <a href="http://webpy.org/">web.py</a>, <a href="http://www.nltk.org">NLTK</a>, <a href="http://jquery.org/">JQuery</a>, <a href="http://cssgrid.net/">1140.css</a>, <a href="http://code.google.com/p/sexybuttons/">sexybuttons</a>, <a href="http://www.vim.org/">vim</a>, and <a href="http://www.photoshop.com/">Adobe Photoshop</a>.
				<br>
				<br>
				<h3>Why?</h3>
				<p>I'm interested in computational linguistics. It's interesting to consider what exactly makes a sentence important, and if it's even possible to find an objective measure of 'meaningfulness'.</p>
				<br>
				<h3>Want to learn more?</h3>
                <p><a href="http://github.com/peterldowns/bookshrink">Check out the code on GitHub!</a></p>
			</div>
		</div> <!-- row -->
	</div> <!-- container -->
</body>
</html>
