import random
from flask import Flask, g, render_template

def create_app():          #factory
    app=Flask("jobs")
    app.config.from_mapping(
        DATABASE="naukri",
        USER="postgres",
        HOST="localhost",
        PASSWORD="2611"
    )

    from . import jobs
    app.register_blueprint(jobs.bp)

    from . import db 
    db.init_app(app)

    @app.route("/")
    def index():
        quotes=[["Life is like a bicycle, to keep your balance, you must keep moving." , "Albert Einstein"],
                ["Believe you can and you're half way there." , "Theodore Roosevelt"],
                ["Don't let yesterday take up too much of today." , "Will Rogers"]]
        quote, author= random.choice(quotes)
        conn=db.get_db()
        cur=conn.cursor()
        cur.execute("SELECT COUNT(*) FROM OPENINGS")
        count=cur.fetchone()[0]
        cur.execute("select crawled_on from crawl_status order by crawled_on desc limit 1")
        crawl_date = cur.fetchone()[0]
        return render_template("index.html",quote=quote, author=author, count=count, date=crawl_date)

    from . import crawler
    crawler.init_app(app)

    return app
    