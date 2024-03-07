import requests
import bs4
import urllib.parse
import re
import sys
from datetime import datetime

domains = []

if len(sys.argv) > 1:
    now = sys.argv[1]
else:
    now = datetime.now().strftime("%Y%m%d")
    print(f"No specific date in the format YYYYMMDD, using current date: {now}")
    
def filter_links(links):
    filtered_links = []
    for link in links:
        if re.match(r".*google.com.*", link):
            continue
        else:
            domain = re.match(r"https?:\/\/(\w+\.(netlify|vercel|github).(io|app))\/.*", link)
            if domain != None:
                domain = domain.group(1)
                filtered_links.append(domain)

    # Remove duplicates
    filtered_links = list(set(filtered_links))
    return filtered_links
        

def scrape_google_results_page(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    links = soup.findAll('a')
    results = []
    for link in links:
        if link.has_attr('href'):
            url = link['href']
            if url.startswith('/url?q='):
                url = url.replace('/url?q=', '')
                url = url.split('&')[0]
                results.append(url)
    
    return results

def fetch_google_results_page(query, num_results=10, language="en", page=1):
    query = urllib.parse.quote(query, safe="")
    url = "https://www.google.com/search?q={}&num={}&hl={}&start={}".format(query, num_results, language, (page-1)*10)
    # print(url)
    response = requests.get(url)
    if response.ok:
        print("Success")
        results = scrape_google_results_page(response.text)
        filtered = filter_links(results)
        # print(f"Found {len(filtered)} results")
        domains.extend(filtered)
    else:
        print("Failed")
    

def main():
    for i in range(1, 10):
        fetch_google_results_page("site:*.netlify.app web developer", 10, "en", i)
        fetch_google_results_page("site:*.vercel.app web developer", 10, "en", i)
        fetch_google_results_page("site:*.github.io web developer", 10, "en", i)
    if len(domains) > 0:
        deduped = list(set(domains))
        print(f"Found {len(deduped)} domains")
        with open(f"data/{now}-domains.txt", "w") as f:
            f.write("\n".join(deduped))

if __name__ == '__main__':
    main()