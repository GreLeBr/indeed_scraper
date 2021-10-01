# Scrapper for indeed.com 
Harvest the job_id, the url of the offer, company name, the title of the job, the job description and the company URL if it exists. 

# Installation: 
You need python and pandas
download the package and move to the decompressed directory run:
`pip install -e .`

To use the script run (with options):
`indeed_scraper-run`
Options are :
* --d or --dir -> to specify the location of the output file if you want it somewhere else
* --j or --job -> to specify the keyword related to the job you are looking for, it can be left empty
* --l or --loc -> to specify the location you want the job search to be operated, it can be left empty
* --p or --page -> to specify how many pages you want to search for the query you are using

so for example:
`indeed_scraper-run --j data`

By default it creates a output.csv in the folder you run the script
`

