# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv



# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options)

 
driver = webdriver.Firefox()

sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)

sleep(2)

# # Task 1.2: Import username and password
credential = open('login_credentials.txt') # login credential in a text file 
line = credential.readlines()
username = line[0]  
password = line[1]
sleep(2)

# # Task 1.2: Key in login credentials
email_field = driver.find_element("id", "username")
email_field.send_keys(username)     #my fake id's email

sleep(3)

password_field = driver.find_element('id','password')
password_field.send_keys(password)    #my fake id's password

sleep(2)

# Task 1.2: Click the Login button
signin_field = driver.find_element('xpath','/html/body/div/main/div[2]/div[1]/form/div[3]/button')
signin_field.click()
sleep(2)


# # Task 2: Search for the profile we want to crawl
# # Task 2.1: Locate the search bar element
search_field = driver.find_element('xpath','/html/body/div[5]/header/div/div/div/div[1]/input') 
# # Task 2.2: Input the search query to the search bar
search_query = input('What profile do you want to scrape?')
sleep(3)
search_field.send_keys(search_query)
sleep(3)

# # Task 2.3: Search
search_field.send_keys(Keys.RETURN)
sleep(2)



# # Task 3: Scrape the URLs of the profiles
# # Task 3.1: Write a function to extract the URLs of one page

page_source = BeautifulSoup(driver.page_source, 'html.parser') #features="lxml"
profiles = page_source.find_all('a', class_ = 'app-aware-link') 
all_profile_URL = []
for profile in profiles:
    profile_ID = profile.get('href')
    profile_URL = "https://www.linkedin.com" + profile_ID
    profile_URL = profile.get('href')
    if profile_URL not in all_profile_URL:   #for profile links of people only!
        all_profile_URL.append(profile_URL)
     
        

# print(all_profile_URL)        #all the profile links would be printed here!

# # Task 3.2: Navigate through many page, and extract the profile URLs of each page
# input_page = int(input('How many pages you want to scrape: '))
URLs_all_page = []
# for page in range(input_page):
# URLs_one_page = all_profile_URL
sleep(2)
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
    # sleep(3)
    # next_button = driver.find_element('class',"artdeco-button__icon") #here
    # driver.execute_script("arguments[0].click();", next_button)

URLs_all_page=all_profile_URL


sleep(2)
print(URLs_all_page)

# print('- Finish Task 3: Scrape the URLs')


# # Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location','Company', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    i=0  #using i, because we got 6 non-related links at the beginning, hence to avoid those links we use variable i
    for linkedin_URL in URLs_all_page:
        i=i+1
        if(i>6):
            driver.get(linkedin_URL)
            print('- Accessing profile: ', linkedin_URL)
            sleep(3)
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('div',class_='mt2 relative')
            try:
                name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
                print('--- Profile name is: ', name)
                location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters 
                print('--- Profile location is: ', location)
                title = info_div.find('div', class_='text-body-medium break-words').get_text().strip()
                print('--- Profile title is: ', title)
                company = info_div.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline').get_text().strip()
                print('--- company name is: ', company)
                writer.writerow({headers[0]:name, headers[1]:title, headers[2]:location, headers[3]:company, headers[4]:linkedin_URL})
                print('\n')
            except:
                pass
       

# # print('Mission Completed!')




