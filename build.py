import sys
import os
import time
from datetime import datetime

def main():
    if len(sys.argv) > 1:
        now = sys.argv[1]
    else:
        now = datetime.now().strftime("%Y%m%d")
        print(f"No specific date in the format YYYYMMDD, using current date: {now}")
    print("Starting build...")
    startTime = time.time()
    if not os.path.exists(f"data/{now}-domains.txt"):
        os.system("python3 search-result-extractor.py")
    if not os.path.exists(f"data/{now}-sites.json"):
        os.system("python3 meta-extractor.py")

    # get list of json files in directory
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    # sort by date
    files.sort(key=lambda x: os.path.getmtime(os.path.join("data", x)))

    datestamps = list(map(lambda x: x.split("-")[0], files))

    for datestamp in datestamps:
        print(f"Getting screenshots of sites for {datestamp}...")
        if os.path.exists(f"screenshots/{datestamp}"):
            print(f"Skipping screenshots for {datestamp}, already exists")
        else:
            if os.path.exists("venv/bin/webscreenshot"):
                binPath = "venv/bin/webscreenshot"
            else:
                binPath = "webscreenshot"
            os.system(f"{binPath} -i data/{datestamp}-domains.txt -r phantomjs --renderer-binary bin/phantomjs -o screenshots/{datestamp} --crop '0,0,1280,720' -f 'jpg' -v")

        print(f"Generating site for {datestamp}...")
        os.system(f"python3 site-generator.py {datestamp}")

    endTime = time.time()
    print(f"Build completed in {endTime - startTime} seconds")


if __name__ == '__main__':
    main()