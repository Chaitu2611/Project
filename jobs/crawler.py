import datetime
import requests
import sys
import html5lib
from bs4 import BeautifulSoup
import click
from flask.cli import with_appcontext

from . import db

def fetch_jobs():
    url="https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=python&location=banglore&pageNo=1&k=python&l=banglore&seoKey=python-jobs-in-banglore&src=jobsearchDesk&latLong="
    headers={"appid":"109","systemid":"109"}
    r=requests.get(url, headers=headers)
    data = r.json()
    return data['jobDetails']

def insert_jobs(jobs):
    dbconn = db.get_db()
    cursor = dbconn.cursor()
    cursor.execute("select id from job_status where name = 'crawled'")
    crawled_id = cursor.fetchone()[0]
    
    crawled_on = datetime.date.today()
    for i in jobs:
        title = i['title']
        job_id = i['jobId']
        company_name = i['companyName']
        jd_url = i['jdURL']
        soup =BeautifulSoup(i['jobDescription'], features="html.parser")
        jd = str(soup.text)
        cursor.execute("""INSERT INTO
        openings (title, job_id, company_name, jd_url, jd_text, status, crawled_on) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",(title, job_id, company_name, jd_url, jd, crawled_id, crawled_on))
    click.echo(f"Added {len(jobs)} jobs.")

    crawled_on = datetime.datetime.now()
    cursor.execute("insert into crawl_status (crawled_on) values (%s)", (crawled_on,)) #removed here
    dbconn.commit()

@click.command('crawl', help="Crawl for jobs")
@with_appcontext
def crawl_command():
    jobs = fetch_jobs()
    insert_jobs(jobs)

def init_app(app):
    app.cli.add_command(crawl_command)
    