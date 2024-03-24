from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def scrap_google_freelance_jobs(url):
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # In case of a non-200 status code , throw an exception
        soup = BeautifulSoup(response.text, "html.parser")

        jobs_listings = soup.find_all("li", class_="iFjolb gws-plugins-horizon-jobs__li-ed")
        scraped_jobs = []
        for job in jobs_listings:
            title_tag = job.find("div", class_="BjJfJf PUpOsf")
            title = title_tag.text

            company_tag = job.find("div", class_="vNEEBe")
            company = company_tag.text

            location_tag = job.find("div", class_="Qk80Jf")
            location = location_tag.text

            posted_date_span = job.find("span", class_="LL4CDc")
            posted_date = posted_date_span.text

            link = job.find("a")["href"]

            scraped_data = {
                "title": title,
                "company": company,
                "location": location,
                "posted_date": posted_date,
                "link": link
            }
            scraped_jobs.append(scraped_data)
        return scraped_jobs

    except requests.exceptions.RequestException as e:
        print(f"an error occurred while scrapping indeed freelance jobs : {e}")
        return []


def scrap_freelancer_jobs(filter_param):
    print(filter_param)
    headers = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }

    try:
        base_url = "https://www.freelancer.com/jobs"
        redirect_url = "https://www.freelancer.com"

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
            print(base_url + url)

            posted_date_tag = job.find("span", class_="JobSearchCard-primary-heading-days")
            posted_date = posted_date_tag.text.replace('\n', '').strip()

            price_tag = job.find("div", class_="JobSearchCard-secondary-price")
            price = price_tag.text.replace('\n', '').strip() if price_tag else "Price not available"

            job_description_tag = job.find("p", class_="JobSearchCard-primary-description")
            job_description = job_description_tag.text.replace('\n', '').strip()

            jobs_data = {
                "source": "freelancer.com",
                "title": title,
                "posted_date": posted_date,
                "price": price,
                "job_description": job_description,
                "url": redirect_url + url

            }

            scraped_jobs.append(jobs_data)

        return scraped_jobs
    except requests.exceptions.RequestException as e:
        print(f"an error occurred while scrapping indeed freelance jobs : {e}")
        return []~