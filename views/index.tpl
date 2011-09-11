<!doctype html>
<html>
<head>
	<title>bookshrink</title>
	<meta name="description" content="finds the essence of any book or text" />
	<meta name="keywords" content="book, shrink, essence, summary, summarize, text, tf-idf" />
	<link rel="stylesheet" type="text/css" href="/static/1140.css" />
   	<link rel="stylesheet" type="text/css" href="/static/sexybuttons.css" />
	<link href='http://fonts.googleapis.com/css?family=lato:regular,regularitalic,bold,bolditalic' rel='stylesheet' type='text/css'>

	<script type="text/javascript" src="../static/jquery.js"></script>
	<script type="text/javascript">
		var _gaq=_gaq||[];_gaq.push(['_setAccount','UA-21305179-1']);_gaq.push(['_trackPageview']);(function(){var ga=document.createElement('script');ga.type='text/javascript';ga.async=true;ga.src=('https:'==document.location.protocol ? 'https://ssl':'http://www')+'.google-analytics.com/ga.js';var s=document.getElementsByTagName('script')[0];s.parentNode.insertBefore(ga, s);})();
	</script>
	<script type="text/javascript">
		jQuery(document).ready(function() {
			jQuery("#analyze").click(function() {
				jQuery("#input_header").removeClass("twelvecol last").addClass("sixcol");
				jQuery("#output_header").addClass("sixcol last").show();
				var i_s = jQuery("textarea#input_string").val();
				var r_t = jQuery("select#result_type").val();
				var n_r = jQuery("select#num_results").val();
				var s_s = jQuery("input#seed_string").val();
				jQuery.ajax({
					type: "POST",
					timeout: 60000,
					data: {	input_string : i_s,
							result_type : r_t,
							num_results : n_r,
							seed_string : s_s},
					success: function(data) {
						jQuery('#output').html(data).hide().fadeIn(1500);
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
						jQuery('#output').html("<h3>Error: "+desc+"</h3><br><p>Please try a different text.</p>").hide().fadeIn(1000);
					},
				});
				return false;
			});
			jQuery("#output_header").hide();
			jQuery('#loading')
				.hide()  // hide it initially
    			.ajaxStart(function() {
					jQuery("#loading").delay(500).show(); // delay some time so it doesn't always flicker up
				})
				.ajaxStop(function() {
					jQuery("#loading").hide();
				});
			jQuery("#toggle_output_options")
			jQuery("#toggle_output_options").click(function(){jQuery("#output_options").fadeToggle(500);});
			jQuery("#output_options")
				.hide(); // hide the extra options initially
			});
	</script>

	<!-- for sharing with sharethis.com -->
	<script type="text/javascript">var switchTo5x=true;</script><script type="text/javascript" src="http://w.sharethis.com/button/buttons.js"></script><script type="text/javascript">stLight.options({publisher:'22f9d0a5-e552-495e-b682-3c7d07f3587d'});</script>
</head>

<body>
	<div class="container">
		<div class="row">
			<center><a href="http://www.bookshrink.com/"><img src="/static/logo.png" /></a></center>
    	</div>
    	<div class="row">
    		<div id="input_header" class="twelvecol last"><center>
				<h2>Paste text or link here</h2>
				<p>Links must point to a .txt file</p>
				<div style="scroll;">
					<textarea id="input_string" rows="25" cols="55"></textarea>
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
				<p>Try copying any of these links into the input box above</p>	
				<br>
				<p>&mdash; <a href="http://www.bookshrink.com/static/ihaveadream.txt">"I Have A Dream"</a></p>
				<p>&mdash; <a
				href="http://www.bookshrink.com/static/prideandprejudice.txt"">Pride and Prejudice</a></p>
				<p>&mdash; <a
				href="http://www.bookshrink.com/static/thejunglebook.txt">The Jungle Book</a></p>
				<p>&mdash; <a
				href="http://www.bookshrink.com/static/wealthofnations.txt">An Inquiry into the Nature and Causes of the Wealth of Nations</a></p>
				<p>&mdash; <a href="http://www.bookshrink.com/static/theiliad.txt">The Iliad</a></p>
				<p>&mdash; <a
				href="http://www.bookshrink.com/static/robinsoncrusoe.txt">Robinson Crusoe</a></p>
				<p>&mdash; <a href="http://www.bookshrink.com/static/obamastateofunion2011.txt">2011 State of the Union Address</a></p>
			</div>
			<div class="fourcol last">
				<h3>Who made this?</h3>
				<b><p>Peter Downs</p></b>
				<p>&mdash; peter.l.downs (at) gmail</p>
				<p>&mdash; <a style="font-size: 11pt;" href="http://twitter.com/#!/peterldowns">@peterldowns</a></p>
				<br>	
				<h3>With what?</h3>
				<p> <a href="http://python.org/">Python</a>, <a href="http://webpy.org/">web.py</a>, <a href="http://www.nltk.org">NLTK</a>, <a href="http://jquery.org/">JQuery</a>, <a href="http://cssgrid.net/">1140.css</a>, <a href="http://code.google.com/p/sexybuttons/">sexybuttons</a>, <a href="http://www.vim.org/">vim</a>, and <a href="http://www.photoshop.com/">Adobe Photoshop</a>.
				<br>
				<br>
				<h3>Why?</h3>
				<p>I'm interested in computational linguistics. It's interesting to consider what exactly makes a sentence important, and if it's even possible to find an objective measure of 'meaningfulness'.</p>
				<br>
				<h3>Like This?</h3>
				<p>If so, you should let people know!</p>
				<br><center>
				<!--http://sharethis.com nonsense -->
				<span class='st_twitter_vcount' displayText='Tweet'><span class='st_facebook_vcount' displayText='Facebook'></span><span class='st_slashdot_vcount' displayText='Slashdot'></span><span class='st_digg_vcount' displayText='Digg'></span>
				</center>
			</div>
		</div> <!-- row -->
	</div> <!-- container -->
</body>
</html>
