def job_offer_scrapper_indeed (filename, search_word="", search_location="", page_scraped=10):

  start_url="https://www.indeed.com"

  scrap_dict={}
  job_id=[]
  url_l=[]
  location=[]
  company_name=[]
  job_title=[]
  job_description=[]
  company_url=[]

  # The number of loop is also arbitrary
  print("Parameters used:", "filename:",filename, "search_word:", search_word, "search_location:", search_location, "page_scraped:", page_scraped)

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
      print('put some search_word or wearch_location')
    response=requests.get(url)
    print("url selected:",url)
    #Cooling down the model to avoid being kicked out
    time.sleep(10)

    soup = BeautifulSoup(response.text, 'html')

    for recipe in soup.find_all( attrs={"data-hide-spinner":"true"}):

      if recipe.attrs["class"][3] is None:
        job_id.append("NaN")
      else:
        job_id.append(recipe.attrs["class"][3])

      if start_url+recipe.attrs["href"] is None:
        url_l.append("NaN")
      else:
        url_l.append(start_url+recipe.attrs["href"])

        # Entering the dedicated page to get the description and company associated url

        time.sleep(5)
        temp_url=start_url+recipe.attrs["href"]
        response1=requests.get(temp_url)
        soup1 = BeautifulSoup(response1.text, 'html')

        if soup1.find(attrs={"class":"jobsearch-jobDescriptionText"}) is None:
          job_description.append("NaN")
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
          location.append("NaN")
        else:
          location.append(result.text)

      for result in recipe.find_all(class_="companyName"):
        if result.text is None:
          company_name.append("NaN")
        else:
          company_name.append(result.text)
          company_url.append(start_url+"/cmp/"+str(result.text))

      for result in recipe.find_all(class_="jobTitle jobTitle-color-purple"):
        if result :
          job_title.append(result.text)         
        else:
          job_title.append("NaN")

      for result_t in recipe.find_all(class_="jobTitle jobTitle-color-purple jobTitle-newJob"):
        if result_t :
          job_title.append(result_t.text)         
        else:
          job_title.append("NaN")

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
        # Create a writer object from csv module
          test_scrap=pd.DataFrame.from_dict(scrap_dict)
          other_way=test_scrap.to_dict("records")
          dict_writer = DictWriter(write_obj, fieldnames=scrap_dict.keys())
          # Add dictionary as wor in the csv
          # dict_writer.writeheader()
          for beatle in other_way:
            dict_writer.writerow(beatle)
            # dict_writer.writerow(scrap_dict)
      else:
        with open(filename, 'a+', newline='') as write_obj:
          test_scrap=pd.DataFrame.from_dict(scrap_dict)
          other_way=test_scrap.to_dict("records")
          dict_writer = DictWriter(write_obj, fieldnames=scrap_dict.keys())
          dict_writer.writeheader()
          for beatle in other_way:
            dict_writer.writerow(beatle)
      scrap_dict={}

# if len(sys.argv) != 2:
#     print('1 argument expected, found {0}'.format(len(sys.argv) - 1))
#     exit()
# if __name__ == '__main__':