from csv import DictWriter
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import time
import requests

def job_offer_scrapper_indeed (filename="", search_word="", search_location="", page_scraped=1):
  ''' This scrapper looks for job offers on indeed and get their description
  you need to pass a search_word or a serch_location or both
  the output is made in a csv for which you need to pass a fullpath with  
  filename '''
  start_url="https://www.indeed.com"

  scrap_dict={}
  job_id=""
  url_l=""
  location=""
  company_name=""
  job_title=""
  job_description=[]
  company_url=""
  if filename =="":
    filename=os.getcwd()+"/output.csv"
  print("Parameters used:",
         "filename:",filename,
          "search_word:", search_word,
           "search_location:", search_location,
             "page_scraped:", page_scraped)
  page_scraped=page_scraped*10
  for s in range(0,page_scraped,10):
    start=f"&start={s}"
    if search_word != "" and search_location=="":
      search_url=f"https://www.indeed.com/jobs?q={search_word}"
      url=search_url+start
    if search_word == "" and search_location!="":
      search_url=f"https://www.indeed.com/jobs?q&l={search_location}"
      url=search_url+start
    if search_word != "" and search_location!="":      
      search_url=f"https://www.indeed.com/jobs?q={search_word}&l={search_location}"
      url=search_url+start
    if search_word == "" and search_location=="":
      url=""
      print('You need to put at least a search_word or a search_location, program exiting')
      exit()
    response=requests.get(url)

    print("url selected:",url)

    #Cooling down the model to avoid being kicked out
    time.sleep(10)

    soup = BeautifulSoup(response.text, 'html.parser')

    for recipe in soup.find_all( attrs={"data-hide-spinner":"true"}):

      if recipe.attrs["class"][3] is None:
        job_id="NaN"
      else:
        job_id=recipe.attrs["class"][3]

      if start_url+recipe.attrs["href"] is None:
        url_l="NaN"
      else:
        url_l=start_url+recipe.attrs["href"]

        # Entering the dedicated page to get the description and company associated url

        time.sleep(5)
        temp_url=start_url+recipe.attrs["href"]
        response1=requests.get(temp_url)
        soup1 = BeautifulSoup(response1.text, 'html.parser')

        if soup1.find(attrs={"class":"jobsearch-jobDescriptionText"}) is None:
          job_description="NaN"
        else :
          job_description.append(soup1.find(attrs={"class":"jobsearch-jobDescriptionText"}).text)

        # could not get that part to work properly

        # if soup1.find(attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).findChildren()==[]:
        #   company_url.append("NaN")
        # else:
        #   company_url.append(soup1.find(attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).findChild()["href"] )

        # if soup1.find(attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).a.attrs["href"] is None:
        # # if soup1.find(attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}) is None:

        #   company_url.append("NaN")
        # else :
        #   company_url.append(soup1.find(attrs={"class":"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).a.attrs["href"])

      # Going back to the rest of the fields

      for result in recipe.find_all(class_="companyLocation"):
        if result.text is None:
          location="NaN"
        else:
          location=result.text

      for result in recipe.find_all(class_="companyName"):
        if result.text is None:
          company_name="NaN"
        else:
          company_name=result.text
          company_url=start_url+"/cmp/"+str(result.text)

      for result in recipe.find_all(class_="jobTitle jobTitle-color-purple"):
        if result : 
          job_title=result.text   
        else:
          job_title="NaN"

      for result_t in recipe.find_all(class_="jobTitle jobTitle-color-purple jobTitle-newJob"):
        if result_t :
          job_title=result_t.text         
        else:
          job_title="NaN"

      # Compiling the dictionary

      scrap_dict["job_id"]=job_id
      scrap_dict["url"]=url_l
      scrap_dict["loc"]=location
      scrap_dict["company_name"]=company_name
      scrap_dict["job_title"]=job_title
      scrap_dict["job_description"]=job_description
      scrap_dict["company_url"]=company_url

      if os.path.isfile(filename):
        with open(filename, 'a', newline='') as write_obj:
          dict_writer = DictWriter(write_obj, fieldnames=scrap_dict.keys())
          dict_writer.writerow(scrap_dict)
      else:
        with open(filename, 'a+', newline='') as write_obj:
          dict_writer = DictWriter(write_obj, fieldnames=scrap_dict.keys())
          dict_writer.writeheader()
          dict_writer.writerow(scrap_dict)
      job_description=[]
      scrap_dict={}

