import scrapy
from indeed.items import IndeedItem
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# called by web app (app.py)
process = CrawlerProcess(get_project_settings())

#you can enter a specific field
internship_field = 'analytics'

class IndeedSpider(scrapy.Spider):
    # name of spider
    name = "ind"
    # structure of base url to crawl, checks until 67th page (current max number of pages)
    
    start_urls = [
        "https://www.indeed.com/jobs?q="+internship_field+"+intern&start=" + str(i)
        for i in range(0, 660)
    ]

    def parse(self, response):
        """
        Get internship details
        """
        job_card = response.css(".jobsearch-SerpJobCard")

        # scrape the following details from each job card
        for job in job_card:
            item = IndeedItem()

            # job title
            job_title = job.css(".jobtitle::attr(title)").get()

            # company name
            company_name = job.css(".company .turnstileLink::text").get()
            if not company_name:
                company_name = job.css("span.company::text").get()
            company_name = str(company_name).strip()  # remove '\n' tag from string

            # link to individual job application page
            job_url = (
                "https://www.indeed.com/viewjob?jk="
                + job.css(".jobsearch-SerpJobCard::attr(data-jk)").get()
            )

            # company rating (out of 5)
            company_rating = job.css("span.ratingsContent::text").get()
            if not company_rating:  # if None, replace value with "Not enough reviews"
                company_rating = "'Not enough reviews'"
            company_rating = str(
                company_rating
            )  # convert to string for data type cohesion in database

            # for remote jobs
            remote = job.css(".remote::text").get()
            if remote == "Remote":
                remote = "Yes"
            else:
                remote = "No"

            # location of job -- could also be remote
            location = job.css(".accessible-contrast-color-location::text").get()
            if location == "Remote":
                remote = "Yes"

            # date when the job listing was posted
            posted_date = job.css("span.date.date-a11y::text").get()

            item["job_title"] = job_title
            item["company_name"] = company_name
            item["job_url"] = job_url
            item["company_rating"] = company_rating
            item["location"] = location
            item["remote"] = remote
            item["posted_date"] = posted_date

            # pass to IndeedItem() in items.py
            yield item
