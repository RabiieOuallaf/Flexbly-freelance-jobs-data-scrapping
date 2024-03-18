from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def scrap_freelancer_jobs(filter_param):
    print(filter_param)
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }

    try:
        base_url = "https://www.freelancer.com/jobs"

        if filter_param:
            query_string = urlencode(filter_param)
            base_url += f'?{query_string}'

        response = requests.get(base_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = soup.find_all("div", class_="JobSearchCard-item-inner")
        scraped_jobs = []

        for job in job_listings:
            title_tag = job.find("a", class_="JobSearchCard-primary-heading-link")
            title = title_tag.text.replace('\n', '').strip()
            url = title_tag.get("href")

            posted_date_tag = job.find("span", class_="JobSearchCard-primary-heading-days")
            posted_date = posted_date_tag.text.replace('\n', '').strip()

            price_tag = job.find("div", class_="JobSearchCard-secondary-price")
            price = price_tag.text.replace('\n', '').strip() if price_tag else "Price not available"

            job_description_tag = job.find("p", class_="JobSearchCard-primary-description")
            job_description = job_description_tag.text.replace('\n', '').strip()

            jobs_data = {
                "title": title,
                "posted_date": posted_date,
                "price": price,
                "job_description": job_description,
                "url": url
            }

            scraped_jobs.append(jobs_data)

        return scraped_jobs
    except requests.exceptions.RequestException as e:
        print(f"an error occurred while scrapping indeed freelance jobs : {e}")
        return []