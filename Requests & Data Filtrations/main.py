from bs4 import BeautifulSoup #import beautiful soup library
import requests #import requests library

position = input('What is your position search query? ') #requests keyword to use in job search
location = input('What is your location? ') #requests location
sortby= input('Would you like to format data by relevance or posting date? (R/D)')

if sortby=='R' or sortby=='r':
    url = 'https://www.reed.co.uk/jobs/'+position+'-jobs-in-'+location #forms the url using the requested variables and sorts for most relevant postings
elif sortby == 'D' or sortby=='d':
    url = 'https://www.reed.co.uk/jobs/'+position+'-jobs-in-'+location+'?sortby=DisplayDate' #forms the url using the requested variables and sorts for most recent postings

html_text = requests.get(url).text #requests the html page from the custom formed url
soup = BeautifulSoup(html_text, 'lxml') #ueses lxml parser
jobs = soup.find_all('article', class_='job-result') #finds ALL the job articles and saves them in jobs

for job in jobs: #for loop to go through each job within the jobs
    job_title = job.find('h3', class_='title').text.strip() #scrapes job title with class title
    company_name = job.find('a', class_='gtmJobListingPostedBy').text #scrapes company name with class gtmJobListingPostedBy
    job_salary = job.find('li', class_='salary').text #scrapes salary with class salary
    job_location = job.find('li', class_='location').text.split()[0] #scrapes location, splits into list and uses first item
    job_times = job.find('li', class_='time').text  #scrapes the type of job it is (part time, full time, contracted etc)
    job_post_time = job.find('div', class_='posted-by').text.split()[1] #scrapes when the job was posted and selects first item
    job_link = job.find('a', class_='gtmJobTitleClickResponsive').get('href').strip() #scrapes job link from anchor tag
    job_work_home = job.find('li', class_='remote')    #
    if job_work_home != None:                          # Checks whether the job is remote or not
        job_work_home = 'Available'                    #

#Prints all job results for first page of the query and location selected and formats it using the data I have scraped

    print(f'''
    --------------------------------
    | Position: {job_title}
    | Comany: {company_name}
    | Posted: {job_post_time}
    | Salary: {job_salary}
    | Working hours: {job_times}
    | Location: {job_location}
    | Work From Home: {job_work_home}
    | Link: https://www.reed.co.uk{job_link}
    --------------------------------
    ''')
