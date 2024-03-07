import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from datetime import datetime

if len(sys.argv) > 1:
    now = sys.argv[1]
else:
    now = datetime.now().strftime("%Y%m%d")
    print(f"No specific date in the format YYYYMMDD, using current date: {now}")

def main():
    sites = []
    response = ""

    with open(f"data/{now}-domains.txt") as f:
        domains = f.read().splitlines()
    for domain in domains:
        if domain:
            try:
                response =  requests.get(f"https://{domain}/")
            except:
                print(f"Failed to fetch {domain}")
            soup = BeautifulSoup(response.text, "html.parser")
            metas = soup.find_all('meta')
            description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
            title = soup.find('title')

            sites.append({
                "domain": domain,
                "title": title.text if title else "No title found",
                "description": len(description) > 0 and description[0] or "No description found"
            })
    with open(f"data/{now}-sites.json", "w") as f:
        print(f"Writing {len(sites)} sites to data/{now}-sites.json")
        f.write(json.dumps(sites, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()