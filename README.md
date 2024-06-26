# Web Dev Showcase - Custom SSG Demo

**Web Dev Showcase** is a showcase and archive of the top-ranked web developer portfolios as indexed by Google. 

_This project is a demonstration of how to build a static site generator (SSG) from scratch using Python._


## Pre-Requisites

Please make sure you install `xvfb` before completing the setup steps below.
On Linux, this can be done with the following command:

> sudo apt-get install xvfb

On macOS, you can install it through downloading and installing the [XQuartz](https://www.xquartz.org) installer.

## Setup 

1. Create a Python virtual environment 
    
    > python -m venv venv/

2. Activate the virtual environment

    > source venv/bin/activate

3. Install the requirements

    > pip install -r requirements.txt

4. Run the build script
    
    > python build.py


### Other Commands

These don't need to be run manually, but are here for reference.

```bash
venv/bin/webscreenshot -i data/20240407-domains.txt -r phantomjs --renderer-binary bin/phantomjs -o screenshots/20240407 --crop "0,0,1280,720" -f "jpg" -v
```

