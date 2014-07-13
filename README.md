#Bookshrink - Find the essence#

###What is it?###
Bookshrink is a tool for picking out the most representative sentences from
some amount of text. It works well on research papers, books, and newspaper
articles. It isn't all that good at understnding poetry. It will do its best on
any type of text you care to run through it.

###Why did you make this?###
I'm interested in natural language processing - more than anything, bookshrink
scratches my own itch. It's also useful for skimming through large amounts of
text to pick up the main ideas.

###How do I use it?###

You can see bookshrink in action at
[bookshrink.com](http://bookshrink.com), where I'm currently
hosting the "canonical" instance. If you'd like to explore the code locally, do this:

```bash
$ git clone https://github.com/peterldowns/bookshrink.git
$ cd bookshrink
$ make dev-server
```

Then, in your browser, visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/).
