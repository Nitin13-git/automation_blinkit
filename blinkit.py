from lib2to3.pgen2 import driver
from time import time
import pre_process
from numpy import product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import os
import json
import re

class BlinkIt():
  def start(self):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
    self.driver.get("https://blinkit.com/")
    # self.driver.set_window_size(1550, 838)
    self.driver.maximize_window()

    try:
      self.driver.find_element(By.CSS_SELECTOR, "location-search-input-google-v1").send_keys("mohali")
    except:
      pass
       #self.driver.find_element(By.CSS_SELECTOR, "..Select-placeholder").send_keys("Mohali")
    #self.driver.find_element(By.CSS_SELECTOR, ".location-search-input-google-v1").click()
    #self.driver.find_element(By.CSS_SELECTOR, ".location-search-input-google-v1").send_keys("Mohali")
   # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="pac-item"]'))).click()
    # self.driver.close()
    #.LocationBar__DownArrow-sc-x8ezho-5
    # self.driver.quit()
    return self.driver


def get_product_data(product, raw_data_file):
  Name= product.getText()
  #print (Name)
  tmp = str(product).split(">")[2].split("<")[0]
  name= pre_process.comparing_ingredient_cleaning_dict(tmp)
  quantity= str(product).split(">")[4].split("<")[0]
  discounted_p=str(product).split(">")[8][1:3].split("<")[0]
  discounted_price,qua=pre_process.converstion(quantity,discounted_p)
  actual_p= str(product).split(">")[10][1:3].split("<")[0]
  actual_price,quantity=pre_process.converstion(quantity,actual_p)
 


  with open(raw_data_file, "a") as f:
    
    data = json.dumps({
      'name': name,
      'quantity': quantity,
      'discounted_price': discounted_price,
      'actual_price': actual_price,
          
    })
    f.write(data + "\n")

 


def dump_json(raw_data_file, out_data_file):
  with open(raw_data_file) as f:
    data = f.read().strip().split("\n")
    js_data = list(map(lambda x: json.loads(x), data))
    with open(out_data_file, "a") as f:
      json.dump(js_data, f, indent=2)

if __name__ == "__main__":
  raw_data_file = ""
  test = BlinkIt()
  #test.start()
  driver=test.start()


  DEBUG = True
  OUTPUT_DIR = "Output"
  out_data_file = os.path.join(OUTPUT_DIR, "data.json")
  delay = 8
  with open('links.txt', 'r') as f:
    url_list = f.read().split("\n")


  raw_data_file=""
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    raw_data_file = os.path.join(OUTPUT_DIR, "raw_data.txt")
    with open(raw_data_file, "a") as f:
      pass
  else:
    raw_data_file = os.path.join(OUTPUT_DIR, "raw_data.txt")

  for url in url_list:
    driver.get(url)
    print("Starting Download from: {}".format(url))

    time.sleep(delay)
   
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = bs(html, 'html.parser')
    products = soup.findAll("div", {"class": "Product__DetailContainer-sc-11dk8zk-3 ksQHQi"})

    rel_url = re.sub(r"/?.*", "", url)
    rel_url = rel_url.lstrip('https://blinkit.com/')


  
    for product in products:
      get_product_data(product, raw_data_file)
      print("Downloaded all data from: ".format(url))

  print("Download finished from all the links.")
  dump_json(raw_data_file, out_data_file)
  print("JSON file saved as {}".format(raw_data_file))

  driver.quit()


















  #WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//input[@type="image"][@src="/images/btn_next.png"]'))).click()
  #driver.execute_script("window.scrollyBy(0,1000)","")
  
  '''element=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div[4]/div/div[4]/div/div/div[1]")))
  el1=driver.execute_script("arguments[0].click();", element)
 





  for i in range(1,1,75):
    z='/html/body/div[1]/div/div[1]/div[4]/div/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div/div/a[i]/div/div[4]'
    titles=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, z)))
    #titles=driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[1]/div[4]/div/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div/div/a[1]/div/div[4]')
    print(titles.text)'''




























