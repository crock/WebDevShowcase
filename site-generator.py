#!./venv/bin/python3
import json
import re
import os
import sys
from datetime import datetime
from pybars import Compiler

compiler = Compiler()

if len(sys.argv) > 1:
    now = sys.argv[1]
else:
    now = datetime.now().strftime("%Y%m%d")
    print(f"No specific date in the format YYYYMMDD, using current date: {now}")

def inline_stylesheet():
    with open("assets/global.css") as f:
        styles = f.read()
    
    return f"""
<style type="text/css">
{styles}
</style>
"""

def generate_page_html(title, content, metaDescription = ""):
    analyticsHtml = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2BHVK54E8T"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-2BHVK54E8T');
</script>
"""

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    {analyticsHtml}
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Dev Portfolio Showcase</title>
    <meta name="description" content="{metaDescription}">
    <link rel="stylesheet" href="/assets/global.css" />
</head>
<body>
    {content}
    <script src="/assets/script.js"></script>
    <script id="dsq-count-scr" src="//worksauce.disqus.com/count.js" async></script>
</body>
</html>
"""

def generate_iframe_html(src, title = ""):
    return f"""
<iframe src="{src}" title="{title}" frameborder="0" allowfullscreen width="100%" height="720"></iframe>
"""

def generate_disqus_html(site):
    domain = site["domain"]
    html = """
<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    /*$
    var disqus_config = function () {
"""
    html += f"""
    this.page.url = "https://worksauce.com/{now}/{domain}";  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = "{domain}"; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
"""
    html += """
    };
    */
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://worksauce.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
"""
    return html

def create_site_page(name, html):
    outputPath = f"www/{now}/{name}/index.html"
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)

    with open(outputPath, "w") as f:
        f.write(html)
        print(f"Created {name} at {outputPath}")

def copy_assets():
    os.makedirs("www/assets", exist_ok=True)
    os.system("rsync -r assets/* www/assets")
    print("Copied assets to www/assets")

def copy_images():
    os.makedirs("www/img", exist_ok=True)
    os.system("rsync -r screenshots/* www/img")
    print("Copied screenshots to www/img")

def get_screenshot_public_path(site):
    domain = site["domain"]
    filename = f"http_{domain}_80.jpg"
    screenshotPath = f"/img/{now}/{filename}"
    
    return screenshotPath

def get_thumbnail_public_path(site):
    publicPath = get_screenshot_public_path(site)
    screenshotPath = f"{publicPath}?nf_resize=fit&w=350"
    if not os.path.exists(f"./www{publicPath}"):
        screenshotPath = f"/assets/no-preview-available.png"
    
    return screenshotPath

def get_all_sites():
    # get list of json files in directory
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    # sort by date
    files.sort(key=lambda x: os.path.getmtime(os.path.join("data", x)))

    allSites = []

    for file in files:
        with open(f"data/{file}") as f:
            sites = json.load(f)
            for site in sites:
                site["datestamp"] = file.split("-")[0]
            allSites.extend(sites)
    
    return allSites

def get_datestamps():
    # get list of json files in directory
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    # sort by date
    files.sort(key=lambda x: os.path.getmtime(os.path.join("data", x)))

    datestamps = list(map(lambda x: x.split("-")[0], files))    

    return datestamps   
    

def create_directory_listing(sites):
        html = inject_header(sites)
        html += inject_crawls()
        html += """
<ul class="grid sites">
"""
        for site in sites:
            domain = site["domain"]
            title = site["title"]

            pageSlug = re.sub(r"\.+", "-", domain)

            html += f"""
<li class="soft-shadow site-card">
<div class="img-preview">
    <a href="{get_screenshot_public_path(site)}" target="_blank" style="{"display:none" if not os.path.exists( f"./www/img/{now}/http_{domain}_80.jpg" ) else "display:block"}">
        <img src="/assets/expand-arrow.png" alt="View full size preview" width={24} />
    </a>
    <img class="preview" src="{get_thumbnail_public_path(site)}" alt="{domain} screenshot thumbnail" width="512" />
</div>
<a href="/{now}/{pageSlug}#disqus_thread">{domain}</a>
<p>{title}</p>
<small>{domain}</small>
</li>
"""
        html += """
</ul>
"""
        pageContent = generate_page_html(f"Home - {now}", html, "Showcase and archive of the top-ranked web developer portfolios as indexed by Google")
        outputPath = f"www/{now}/index.html"
        with open(outputPath, "w") as f:
            f.write(pageContent)
            print(f"Created directory index at {outputPath}") 

def create_index_page(sites):
    html = inject_header(sites)
    html += inject_crawls()
    html += """
<ul class="grid sites">
"""
    for site in sites:
        domain = site["domain"]
        title = site["title"]

        pageSlug = re.sub(r"\.+", "-", domain)

        html += f"""
<li class="soft-shadow site-card">
    <div class="img-preview">
        <a href="{get_screenshot_public_path(site)}" target="_blank" style="{"display:none" if not os.path.exists( f"./www/img/{now}/http_{domain}_80.jpg" ) else "display:block"}">
            <img src="/assets/expand-arrow.png" alt="View full size preview" width={24} />
        </a>
        <img class="preview" src="{get_thumbnail_public_path(site)}" alt="{domain} screenshot thumbnail" width="512" />
    </div>
    <a href="/{now}/{pageSlug}#disqus_thread">{domain}</a>
    <p>{title}</p>
    <small>{domain}</small>
</li>
"""
    html += """
</ul>
"""
    pageContent = generate_page_html("Home", html, "Showcase and archive of the top-ranked web developer portfolios as indexed by Google")
    with open("www/index.html", "w") as f:
        f.write(pageContent)
        print(f"Created homepage at www/index.html")


def inject_header(sites):
    with open("./components/header.hbs") as f:
        contents = f.read()
        template = compiler.compile(contents)
        return template({
            "title": "WorkSauce",
            "description": "Showcase and archive of the top-ranked web developer portfolios as indexed by Google",
            "now": now,
            "total": len(sites)
        })
    
def inject_crawls():
    datestamps = get_datestamps()
    with open("./components/previous-crawls.hbs") as f:
        contents = f.read()
        template = compiler.compile(contents)
        return template({
            "crawls": datestamps
        })


def main():
    path = os.path.join("data", f"{now}-sites.json")
    with open(path) as f:
        sites = json.load(f)
    if len(sites) == 0:
        print("No sites found")
        return
    for site in sites:
        domain = site["domain"]
        title = site["title"]
        description = site["description"]

        pageSlug = re.sub(r"\.+", "-", domain)

        html = f"""
<h1>{title}</h1>
<p>{description}</p>
{generate_iframe_html(f"https://{domain}/", title)}
{generate_disqus_html(site)}
"""

        pageContent = generate_page_html(f"Viewing {domain}", html, description)
        create_site_page(pageSlug, pageContent)
    create_directory_listing(sites)
    create_index_page(sites)
    copy_assets()
    copy_images()

if __name__ == '__main__':
    main()