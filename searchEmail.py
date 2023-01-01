# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv

driver = webdriver.Firefox()

#Task 5:
#Now we would go to a seperate website: contactout.com and in there we would search for CEOs' emails:
sleep(2)

url1 = 'https://contactout.com/login' 
driver.get(url1)
sleep(2)
all_emails=[]  #would store all the emails

#Import username and password
credential = open('login_credentials.txt') # login credential in a text file 
line = credential.readlines()
username1= line[2]  
password1= line[3]
sleep(2)

#  Key in login credentials
email_field = driver.find_element("xpath", "/html/body/div/div/section/div/div[3]/form/div[1]/div/div/input")
email_field.send_keys(username1)     

sleep(3)

password_field = driver.find_element('xpath','/html/body/div/div/section/div/div[3]/form/div[2]/div/div/input')
password_field.send_keys(password1)   

sleep(2)

#  Click the Login button
signin_field = driver.find_element("xpath",'/html/body/div/div/section/div/div[3]/form/div[3]/button')
signin_field.click()
sleep(3)

#Now we would read data for Name and Job Title from the csv file:
with open('output.csv') as file:
    reader=csv.reader(file)   #creating a object to extract the values/elements from csv file

    i=0  #would exclude first row as they include headers

    for row in reader:
        if(i>=1):
            name=row[0]
            job_title=row[1]
            name_field = driver.find_element('xpath','/html/body/div[1]/div[2]/div[3]/form/div/div[1]/div[1]/label/input') #locating the Name bar
            name_field.send_keys(name)
            sleep(3)
            title_field = driver.find_element('xpath','//*[@id="react-select-2-input"]') #locating the Name bar
            title_field.send_keys(job_title)
            sleep(2)
            signin_field = driver.find_element('xpath','/html/body/div[1]/div[2]/div[3]/form/div/div[1]/div[14]/button')
            signin_field.click()
            sleep(2)
            try:
                see_email_button=driver.find_element('xpath','/html/body/div[1]/div[2]/div[4]/div[3]/div/div[2]/div[3]/button')
                see_email_button.click()
            except:
                email='null'
                pass
                
            
            sleep(2)
            try:
                page_source = BeautifulSoup(driver.page_source, "html.parser")
                email = page_source.find('p', class_='css-1ca4b1z').get_text().strip() #Remove unnecessary characters 
                print('Email is: ', email)
                all_emails.append(email)
                
                
            except:
                email='null'
                print('Email is: ', email)
                all_emails.append(email)
                pass

                

            driver.get('https://contactout.com/dashboard/search?login=success')
        i=i+1


print(all_emails)   



#now we will write the emails to the output_1.csv file at their respective positions along with other data from
# output.csv:


from csv import writer
from csv import reader
# Open the input_file in read mode and output_file in write mode
with open('output.csv', 'r') as read_obj, \
        open('output_1.csv', 'w', newline='') as write_obj:

    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    k=0 #initializing k=0 to input email in the first row
    for row in csv_reader:
        # Append the default text in the row / list
        if(k==0):
            row.append(' Email')
            csv_writer.writerow(row)
        if(k>=1):
            row.append(' '+all_emails[k-1])    
            # Add the updated row / list to the output file
            csv_writer.writerow(row)
        k=k+1
            

   
print('Mission Completed')
    



