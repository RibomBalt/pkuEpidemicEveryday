from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time

def iaaa_login(config_fname):
    # read conf.json
    with open(config_fname,'r') as f:
        content = f.read()
    conf = json.loads(content)
    stuid = conf['stuid']
    passwd = conf['passwd']
    webdriver_path = conf['webdriver_path']
    # create selenium driver
    driver = getattr(webdriver, conf['driver_name'])(webdriver_path)
    driver.get('https://portal.pku.edu.cn/portal2017/#/bizCenter')
    # iaaa login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_name"))
    ).send_keys(stuid)
    driver.find_element_by_id('password').send_keys(passwd)
    driver.find_element_by_id('logon_button').click()
    return (driver, conf)

def epidemic_access(driver:webdriver.Edge):
    # find fresh register on portal
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).clear()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).send_keys('学生出入校',Keys.ENTER)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "stuCampusExEnReq"))
    ).click()
    driver.switch_to.window(driver.window_handles[1])
    # TODO after opening epidemic access.

def epidemic(driver, input_temperature):
    # open pku epidemic
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).clear()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).send_keys('燕园云战“疫”',Keys.ENTER)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "epidemic"))
    ).click()
    driver.switch_to.window(driver.window_handles[1])
    # temperature, optional
    time.sleep(1)
    if input_temperature:
        s = input("Please input your temperature today: ") # no validation check.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-daily_info_tab"]/form/div[12]/div/div/div/input'))
        ).clear()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-daily_info_tab"]/form/div[12]/div/div/div/input'))
        ).send_keys(s)
    # show symptoms? no
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pane-daily_info_tab"]/form/div[13]/div/label[2]/span[1]'))
    ).click()
    # status? healthy.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pane-daily_info_tab"]/form/div[14]/div/div/div'))
    ).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[1]'))
    ).click()
    # submit
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pane-daily_info_tab"]/form/div[17]/div/button'))
    ).click()
    print('Task Finished!')
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    driver, conf = iaaa_login('conf.json')
    epidemic(driver, conf['input_temperature'])
    # epidemic_access(driver)
    
