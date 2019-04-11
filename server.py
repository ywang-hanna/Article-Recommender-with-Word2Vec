# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

import sys
from doc2vec import *
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template("articles.html", articles=articles, topics=topics, filenames=filenames)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    for art in articles:
        if art[0] == topic + '/' + filename:
            art_title = art[1]
            art_content = art[2].split('\n\n')
            rmd = recommended(art, articles, 5)
            break
    rmd_topic = [r[0].split('/')[0] for r in rmd]
    rmd_filename = [r[0].split('/')[1] for r in rmd]
    return render_template("article.html", title=art_title, content=art_content, recommended=rmd,
                           topic=rmd_topic, filename=rmd_filename)



# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)

topics = [art[0].split('/')[0] for art in articles]
filenames = [art[0].split('/')[1] for art in articles]


# app.run('0.0.0.0')
