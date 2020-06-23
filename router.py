#!/usr/bin/python3

import env
import psycopg2
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

#run webbrowser
browser = webdriver.Firefox()
browser.get(env.url)

#find text field
login = browser.find_element_by_id(env.login_element_id)
passwd = browser.find_element_by_id(env.password_element_id)
#insert credentials
login.send_keys(env.login)
passwd.send_keys(env.password)

#login
python_button = browser.find_elements_by_xpath(env.xpath)[0]
python_button.click()

#find mainPage
frame = browser.find_element_by_id(env.frame)

#copy all data from mainPage
frame.send_keys(Keys.CONTROL + 'a')
frame.send_keys(Keys.CONTROL + 'c')

#close webbrowser
browser.close()

#paste information
text=pyperclip.paste()
print(text)

#parse information
table = text.split('\n')

#select usage
used_v = table[17].split(":")

#select signal strength
signal_v = table[11].split(':')

print(used_v)

#log console information
print("Monthly used:")
print(used_v[1])
print("Signal strength:")
print(signal_v[1])

#connect to database
try:
    conn = psycopg2.connect(host=env.host, port=env.port, database=env.db_name, user=env.db_user, password=env.db_password)
    print("Connected to database")
    
    cur = conn.cursor()
    
    #prepare query
    insert_query = "INSERT INTO usage (date,usage,signal,type) VALUES (%s, %s, %s, %s)"

    #get time
    now = datetime.now()
    print("Measure date-time",now)
    
    time = now.time()
    print("Measure time:", time)

    #type: 1 = mornig_count, 2 = night_count, 3 = test_count 
    type_count = 3
    
    if time.hour == 8 and time.minute < 5:
        type_count = 1
    elif time.hour == 1 and time.minute < 5:
        type_count = 2
    

    #values to insert
    values_to_insert=(now, used_v[1], signal_v[1], type_count )

    cur.execute(insert_query, values_to_insert)

    conn.commit()
    conn.close()

except (Exception, psycopg2.DatabaseError) as error:
        print(error)
