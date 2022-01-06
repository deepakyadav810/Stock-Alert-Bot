import discord 
import os
from datetime import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime

##logined in as bot
client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

##calculating time
def is_time_between(begin_time, end_time, check_time=None):
  # If check time is not given, default to current UTC time
  check_time = check_time or datetime.utcnow().time()
  if begin_time < end_time:
    return check_time >= begin_time and check_time <= end_time
  else: # crosses midnight
    return check_time >= begin_time or check_time <= end_time

##opening browser
option = Options()
option.add_argument('headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=option)
driver.get("https://in.tradingview.com/") 
print(driver.title)

#initiating the bot
@client.event
async def on_message(message):
  if message.author == client.user: 
    return 

  messageContent = message.content
  if('$' in messageContent):
    stock=messageContent.replace('$', '')
    print(stock)
    element = driver.find_element_by_class_name("searchText-3V6BxBaO")
    element.click()
    sleep(3)
    search = driver.find_element_by_name("query")
    stock=stock.upper()
    print(stock)
    search.send_keys(stock)
    search.send_keys(Keys.RETURN)
    while(is_time_between(time(9,30), time(23,30))==True):
      try:
          main = WebDriverWait(driver, 20).until(
              EC.presence_of_element_located((By.CLASS_NAME, "priceWrapper-3PT2D-PK"))
          )
          string = main.text
          li = list(string.split("\n"))
          print(li[0])
          await message.channel.send(li[0])
          sleep(2)
      except:
        driver.quit()
        
client.run(os.getenv('TOKEN')) 
