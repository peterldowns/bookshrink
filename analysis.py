# coding: utf-8
import re
from collections import Counter


def clean(s):
    """ Get rid of any non-alphabetic character and clean up whitespace. """
     # Remove everything that isn't an alphabet character (only interested
     # in words, not numbers or punctuation).
    s = re.sub(r'[^a-zA-Z]', ' ', s)
    # Collapse whitespace in any amount or type (tabs, newlines, etc.) into
    # a single space.
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


class SentenceAnalyzer():
    # The ~100 most common words in the english language (which will be
    # ignored in the analysis), taken from
    # http://www.duboislc.org/EducationWatch/First100Words.html
    commonstr = set(
            "mr mrs ms dr the of and a to in is you that it he was for on "
            "are as with his they i at be this have from or one had by "
            "word but not what all were we when your can said there use "
            "an each which she do how their if will up other about out "
            "many then them these so some her would make like him into "
            "time has look two more write go see number no way could "
            "people my than first water been call who oil its now find "
            "long down day did get come made may part am let".split())
    # The darkest possible highlight color for a sentence when outputting
    # highlighted HTML.
    darkest_highlight_hex = '#FF0F0F'
    # A simple regex for splitting text into sentences, ignoring some common
    # abbreviations, numbers, and other phrases that also use a '.' to mean
    # something other than the end of a sentence. In my experience this works
    # well enough to compare favorably with the NLTK sentence splitter.
    sentence_splitter = re.compile(
            ur'''(?<!\d)
                (?<![A-Z]\.)
                (?<!\.[a-z]\.)
                (?<!\.\.\.)
                (?<!etc\.)
                (?<![Mm]r\.)
                (?<![Pp]rof\.)
                (?<![Dd]r\.)
                (?<![Mm]rs\.)
                (?<![Mm]s\.)
                (?<![Mm]z\.)
                (?<![Mm]me\.)
                (?:
                    (?<=[.!?])|
                    (?<=[.!?]['"“”\(\)\[\]])
                )
                [\s]+?
                (?=[^a-z0-9])''',
            re.VERBOSE)


    def __init__(self, seed_string=None):
        # Allow an optional, comma-separated string of words to be given extra
        # importance.
        self.seed_string = seed_string
        if self.seed_string is not None:
            self.seeds = [clean(s).strip().lower()
                          for s in self.seed_string.split(',')]
        else:
            self.seeds = None


    def analyze(self, input_string):
        self.inputstr = input_string
        if not isinstance(self.inputstr, unicode):
            self.inputstr = self.inputstr.decode('utf8')

        # Step 1: split the input into sentences.
        self.sentences = self.sentence_splitter.split(self.inputstr.strip())

        # Count each unique word's frequency in the input text.
        self.words = clean(self.inputstr).split()
        self.word_weights = Counter()
        for word in self.words:
            # Don't count frequencies for stop words.
            if word.lower() in self.commonstr:
                continue
            self.word_weights[word] += 1

        # The number of times a word has appeared in the text is it's raw
        # weight. Modify these weights by certain conditiosn not based on
        # appearance count.
        for word in self.word_weights:
            # Modify proper noun weights.
            if word.istitle() and not word.isupper():
                self.word_weights[word] *= 2
            # Modify weights of words that appear in the optional list of
            # important words passed when the analyzer was created.
            if self.seeds is not None and word.lower() in self.seeds:
                self.word_weights[word] *= 3

        # Assign each individual sentence a weight/score based on the weights
        # of the words of which they are comprised.
        self.total_sentence_length = 0.0
        lengths = []
        self.scores = {}
        for s in self.sentences:
            sentence = clean(s)
            # Keep track of each sentence length so we can figure out an
            # average length later.
            lengths.append(len(sentence.split()))
            s_sum = 0.0 # Sum of the weights of the words in this sentence.
            s_words = 0 # Number of words in the sentence.
            for s_word in sentence.split():
                # This works because the Counter object returns 0 if a key
                # doesn't exist. Stop-words removed earlier will have a value
                # of 0.
                s_sum += self.word_weights[s_word]
                s_words += 1

            # Sentence scores are normalized by length; if it's a word-less
            # 'sentence' (because of our regex-based splitting algorithm) give
            # it a value of 0.
            self.scores[s] = s_sum/s_words if s_words else 0

        self.av_length = sum(lengths)/len(lengths)

        # Despite earlier normalization, sentence scores do depend on length.
        for sentence in self.sentences:
            length = len(clean(sentence).split())
            if length < self.av_length/1.5: # punish short self.sentences
                try:
                    self.scores[sentence] = float(self.scores[sentence])/3
                except: pass
            elif length > self.av_length*1.5: # reward longer self.sentences
                try:
                    self.scores[sentence] = self.scores[sentence]*3
                except: pass

        self.sorted_sentences = sorted(
                self.scores.keys(),
                key=lambda k: self.scores[k],
                reverse=True)
        self.highest_s_score = self.scores[self.sorted_sentences[0]]

        self.sorted_words = sorted(
                self.word_weights.keys(),
                key=lambda key: self.word_weights[key],
                reverse=True)
        self.highest_w_score = self.word_weights[self.sorted_words[0]]

    def get_results(self, result_type, num_results=15):
        # Hex color changing functions stolen from
        # http://thadeusb.com/weblog/2010/10/10/python_scale_hex_color for use
        # in the highlighting section.
        def clamp(val, minimum=0, maximum=255):
            if val < minimum:
                return minimum
            if val > maximum:
                return maximum
            return val

        def colorscale(hexstr, scalefactor):
            """
            Scales a hex string by ``scalefactor``. Returns scaled hex string.
            To darken the color, use a float value between 0 and 1.
            To brighten the color, use a float value greater than 1.
            >>> colorscale("#4F75D2", 1)
            """
            hexstr = hexstr.strip('#')
            if scalefactor < 0 or len(hexstr) != 6:
                return hexstr
            r = clamp(int(hexstr[:2], 16) * scalefactor)
            g = clamp(int(hexstr[2:4], 16) * scalefactor)
            b = clamp(int(hexstr[4:], 16) * scalefactor)
            return "#%02x%02x%02x" % (r, g, b)

        # If num_results is < 1, then it is a percentage.
        if num_results < 1:
            # Even with a short input text and a small percentage, always
            # return at least one result.
            num_results = max(num_results * len(self.sorted_sentences), 1)
            # At most, return as many sentences as there are. It would be
            # impossible to return more.
            num_results = min(num_results, len(self.sorted_sentences))

        # Create a list of the first `num_results` sentences.
        self.individ_list = self.sorted_sentences[0:int(num_results)]
        if result_type == "paragraph":
            self.paragraph = " ".join(self.individ_list)
            return self.paragraph
        elif result_type == "individual":
            self.paragraph = "<br><br>".join(self.individ_list)
            return self.paragraph
        elif result_type == "frequency":
            # Add information to the first num_results sentences and put them
            # in a list.
            self.individ_freq_list = []
            for i, sentence in enumerate(self.individ_list):
                self.individ_freq_list.append("%d (%f): %s" % (
                    i+1,
                    float(self.scores[sentence])/self.highest_s_score,
                    sentence))
            return "<br><br>".join(self.individ_freq_list)
        elif result_type == "highlight":
            self.highlight = self.sentences
            for sentence in self.sorted_sentences:
                rel_score = self.scores[sentence]/self.highest_s_score
                rel_score = rel_score ** 2 # Emphasize visual differences.
                color = self.darkest_highlight_hex
                if rel_score != 0:
                    factor = 1.0/rel_score
                    color = colorscale(color, factor).upper()
                else:
                    color = "#FFFFFF"
                self.highlight.insert(
                    self.highlight.index(sentence),
                    ('<div class="highlight" '
                     'style="background-color:%s;">') % color)
                self.highlight.insert(
                    self.highlight.index(sentence) + 1,
                    '</div><div></div>')

            # Recompile the list back into paragraph form.
            self.highlight = ' '.join(self.highlight)
            # Use HTML whitespace characters.
            self.highlight = re.sub(r'\n', '<br>', self.highlight)
            self.highlight = re.sub(r'\r', '', self.highlight)
            self.highlight = re.sub(r'\t', '&nbsp;' * 4, self.highlight)
            return self.highlight
        else:
            return None
