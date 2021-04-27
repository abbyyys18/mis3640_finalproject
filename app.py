from flask import Flask, request, render_template, redirect
import sqlite3
from flask import g

import scrapy
from scrapy.crawler import CrawlerProcess
from indeed.spiders.indeed_spider import IndeedSpider, process

app = Flask(__name__)

#CONNNECT FLASK TO SQLITE DATABASE
DATABASE = '/Users/abby/Documents/GitHub/mis3640_finalproject/indeed.db'
def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

#Greet user with home page
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/result', methods=["POST", "GET"])
def result():
    """
    Once 'submit button' is clicked, this function 
    starts the crawling process of the scrapy spider. 
    Then, the scraped data gets stored in the database.

    This function fetches the scraped data again and is displayed as 
    an HTML table in the results.html page. 
    """
    if request.method == 'POST':
        process.crawl(IndeedSpider)
        process.start()

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor() 
        cur.execute('SELECT job_title,company_name,company_rating,location,remote,job_url,posted_date FROM internships_db')
        rows = cur.fetchall()
        return render_template('results.html', rows = rows)


if __name__ == '__main__':
    app.run(debug=True)
