from bs4 import BeautifulSoup #import beautiful soup library
import requests #import requests library
import time #import time library
from datetime import datetime #import library for date and time
import numpy as np #imports numpy library
#some UI :)
print('''


░░░░░██╗░█████╗░██████╗░  ███████╗██╗███╗░░██╗██████╗░███████╗██████╗░
░░░░░██║██╔══██╗██╔══██╗  ██╔════╝██║████╗░██║██╔══██╗██╔════╝██╔══██╗
░░░░░██║██║░░██║██████╦╝  █████╗░░██║██╔██╗██║██║░░██║█████╗░░██████╔╝
██╗░░██║██║░░██║██╔══██╗  ██╔══╝░░██║██║╚████║██║░░██║██╔══╝░░██╔══██╗
╚█████╔╝╚█████╔╝██████╦╝  ██║░░░░░██║██║░╚███║██████╔╝███████╗██║░░██║
░╚════╝░░╚════╝░╚═════╝░  ╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝


''')

position = input('What is your position search query? ') #requests keyword to use in job search
location = input('What is your location? ') #requests location
sortby = input('Would you like to format data by relevance or posting date? (R/D) ') #requests the type of results the user desires
email = input('What is your email address for the job updates? ') #requests email to send email with alerts using API

def job_search_reed(): #function that searches for jobs
    page = 1    #defines first page
    job_reed_print = [] #defines the list that will hold the jobs
    job_average_salary = [] #defines the list that will hold all salaries

    while page<=20: #loop for 20 pages because any more slows the program down too much. NOTE: try make a function to check how many pages the search result has and change the 20 to that variable
        if sortby.lower() == 'r': #if you requested relevance for the sorting
            url_reed = 'https://www.reed.co.uk/jobs/' + position + '-jobs-in-' + location + '?pageno=' + str(page) #forms the url using the requested variables and sorts for most relevant postings
        elif sortby.lower() == 'd': #if you requested date for the sorting
            url_reed = 'https://www.reed.co.uk/jobs/' + position + '-jobs-in-' + location + '?pageno=' + str(page) + '&sortby=DisplayDate' #forms the url using the requested variables and sorts for most recent postings
        html_text_reed = requests.get(url_reed).text #requests the html page from the custom formed url
        soup_reed = BeautifulSoup(html_text_reed, 'lxml') #ueses lxml parser
        jobs_reed = soup_reed.find_all('article', class_='job-result') #finds ALL the job articles and saves them in jobs
        
        
        for job in jobs_reed: #for loop to go through each job within the jobs
            job_title_reed = job.find('h3', class_='title').text.strip() #scrapes job title with class title
            company_name_reed = job.find('a', class_='gtmJobListingPostedBy').text #scrapes company name with class gtmJobListingPostedBy
            job_salary_reed = job.find('li', class_='salary').text #scrapes salary with class salary
            job_location_reed = job.find('li', class_='location').text.split()[0] #scrapes location, splits into list and uses first item
            job_times_reed = job.find('li', class_='time').text  #scrapes the type of job it is (part time, full time, contracted etc)
            job_post_time_reed = job.find('div', class_='posted-by').text.split()[1] #scrapes when the job was posted and selects first item
            if job_post_time_reed != 'Today' or job_post_time_reed != 'Yesterday': 
                job_post_time_reed= job_post_time_reed+' days ago'  #filters the jobs that were posted today or yesterday and adds days ago since I only used the first item in the list
            job_link_reed = job.find('a', class_='gtmJobTitleClickResponsive').get('href').strip() #scrapes job link from anchor tag
            job_work_home_reed = job.find('li', class_='remote')    #
            if job_work_home_reed != None:                          # Checks whether the job is remote or not
                job_work_home_reed = 'Available'                    #

        #Prints all job results for first page of the query and location selected and formats it using the data I have scraped
            job_reed_print.append(f'''
            --------------------------------
            | Position: {job_title_reed}
            | Comany: {company_name_reed}
            | Posted: {job_post_time_reed}
            | Salary: {job_salary_reed}
            | Working hours: {job_times_reed}
            | Location: {job_location_reed}
            | Work From Home: {job_work_home_reed}
            | Link: https://www.reed.co.uk{job_link_reed}
            --------------------------------
            ''')
            
            if job_salary_reed.split()[-1]=='annum': #finds the annual salary
                job_salary_reed = int(job_salary_reed.split()[0].replace('£','').replace(',',''))  #strips the symbols, and uses the lowest amount of the salary spectrum
                job_average_salary.append(job_salary_reed) #appends the salary to the salary list

        page+=1 #increments page by one, moves onto next page

    average = sum(job_average_salary) / len(job_average_salary) #finds mean of salaries from scraped results
    np_job_salary = np.array(job_average_salary) #creates np array with all the salaries
    file = open('jobs.txt', 'w') #opens file in write mode
    alert_facts = f'''
    
    File Last Updated: {datetime.now()}

    The mean salary for {position} in {location} is £{round(average, 2)}

    The 95th percentile salary for {position} in {location} is £{np.percentile(np_job_salary, 95)}0
    '''
    # find 95th percentile using numpy lib

    file.write(alert_facts) #write the facts to file
    for x in job_reed_print: #for loop to write all jobs onto the file
        print(x)
        file.write(x)
    file.close

    job_reed_print.insert(0,alert_facts) #inserts to the start of the list
    email_update(job_reed_print) #call the email api

def email_update(job_reed_print):
	return requests.post( #sends email to the email given at the start with the subject job updates and the list with jobs and facts
		"https://api.mailgun.net/v3/sandbox2228b756d9d7418ea72406439f7adbf4.mailgun.org/messages",
		auth=("api", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"), #insert api key here
		data={"from": "Job Updates Script <mailgun@sandbox2228b756d9d7418ea72406439f7adbf4.mailgun.org>",
			"to": [email],
			"subject": "Job Updates",
			"text":job_reed_print})

if __name__ == "__main__":
    while True: #infinite loop
        job_search_reed() #calls function
        print("Please wait 5 hours for positions to update...") #alerts user that the program has finished and will re-scrape the website in 5 hours and send another alert
        time.sleep(18000) #sleep for 5 hours in seconds