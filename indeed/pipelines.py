# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from scrapy.exceptions import DropItem


class IndeedPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("indeed.db")  # connect to 'indeed' database
        self.curr = self.conn.cursor()

    def create_table(self):
        # drop table if internships_db already exists
        self.curr.execute("""DROP TABLE IF EXISTS internships_db""")
        # create new table
        self.curr.execute(
            """create table internships_db(
        job_title VARCHAR,
        company_name VARCHAR,
        job_url VARCHAR,
        company_rating VARCHAR,
        location VARCHAR,
        remote VARCHAR,
        posted_date VARCHAR
        )"""
        )

    def process_item(self, item, spider):
        self.store_db(item)
        return item  # store items to database

    def store_db(self, item):
        # insert scraped data into specific columns
        self.curr.execute(
            """insert into internships_db values (?,?,?,?,?,?,?)""",
            (
                item["job_title"],
                item["company_name"],
                item["job_url"],
                item["company_rating"],
                item["location"],
                item["remote"],
                item["posted_date"],
            ),
        )
        self.conn.commit()


class DuplicatesPipeline(object):
    """removes duplicates of existing job urls"""

    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        if item["job_url"] in self.url_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.url_seen.add(item["job_url"])
            return item