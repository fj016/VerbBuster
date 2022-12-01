# VerbBuster

A badly written, multi-threaded, python script to test endpoints for exotic http methods.
## Install

To install :

```sh
git clone https://github.com/fj016/VerbBuster.git
cd VerbBuster/
pip3 install -r requirements.txt
```
## Usage

```sh
python VerbBuster.py -h
VerbBuster.py [-h] -l LIST -m {validate,trace,custom} [-c CUSTOM] -oN
                     OUTPUT_NAME

Validate a list of URLs or discover endpoints that uses exotic HTTP verbs.

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST                                             File containing a list of URLS to scan
  
  -m {validate,trace,custom}, --mode {validate,trace,custom}       The mode you want to use
  
  -c CUSTOM, --custom CUSTOM                                       The custom verb to use if mode set to custom
  
  -oN OUTPUT_NAME, --output-name OUTPUT_NAME                       The path and prefix to output files
```

When using the mode **validate** the script will just check the provided list for url that respond with valid code (Anything except 404, and 5XX) and write to a file the URLs returning code 2XX (xxx_ok.txt) and 3XX or 403 to xxx_maybe.txt

When using the mode **trace** it will probe all URLs provided for the trace method and output the ones that respond to xxx_trace_ok.txt

When using the mode **cutsom** it will do the same as trace but with a user-provided verb


This could be useful to parse output from crawling and recon tool like katana or dirbuster
