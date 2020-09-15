from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
from datetime import date

def do_selection(driver:webdriver.Edge, root_xpath, ul_xpath, target_text):
    # /html/body/div[3]/div[1]/div[1]/ul/li[1]
    driver.find_element_by_xpath(root_xpath).click()
    time.sleep(1)
    target_index = driver.find_element_by_xpath(ul_xpath).text.split('\n').index(target_text) + 1
    driver.find_element_by_xpath(ul_xpath + '/li[%d]'%(target_index)).click()
    time.sleep(1)


def iaaa_login(config_fname):
    # read conf.json
    with open(config_fname,'r',encoding='utf-8') as f:
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

def epidemic_access_out(driver:webdriver.Edge, conf_access:dict):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).clear()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).send_keys('学生出入校',Keys.ENTER)
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "stuCampusExEnReq"))
    ).click()
    # driver.execute_script('window.open("https://simso.pku.edu.cn/pages/epidemicAccess.html#/editApplyInfo");')
    driver.switch_to.window(driver.window_handles[1])
    # 点击：出入校备案
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/section/div/div/div[2]/main/div[2]/a/div/div"))
    ).click()
    # 点击：出校
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div/div[2]/main/div/div[2]/form/div/div[3]/div/div/div/div'))
    ).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[1]'))
    ).click()
    time.sleep(1)
    # 填入：出入校事由
    # driver.execute_script('var tb=document.querySelector("body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-22.el-col-sm-22.el-col-md-20.el-col-lg-16 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div > div:nth-child(7) > div > div > div.el-textarea > textarea"); tb.value="%s";'%(conf_access['reason']))
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[7]/div/div/div/textarea').send_keys(conf_access['reason'])
    # 填入：出校行动轨迹
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[3]/div/div/div[1]/textarea').send_keys(conf_access['track'])
    # 点击：承诺
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[9]/div/div/label/span[1]/span').click()
    # 点击：保存，提交，确定
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[10]/div/div/div/div[1]/button').click()
    time.sleep(1)
    driver.find_elements_by_tag_name('button')[-1].click()
    time.sleep(1)
    driver.find_elements_by_tag_name('button')[-1].click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def epidemic_access_in(driver:webdriver.Edge, conf_access:dict):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).clear()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "keyword"))
    ).send_keys('学生出入校',Keys.ENTER)
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "stuCampusExEnReq"))
    ).click()
    # driver.execute_script('window.open("https://simso.pku.edu.cn/pages/epidemicAccess.html#/editApplyInfo");')
    driver.switch_to.window(driver.window_handles[1])
    # 点击：出入校备案
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/section/div/div/div[2]/main/div[2]/a/div/div"))
    ).click()
    # 点击：入校
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div/div[2]/main/div/div[2]/form/div/div[3]/div/div/div/div'))
    ).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[2]'))
    ).click()
    time.sleep(1)
    # 填入：出入校事由
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[7]/div/div/div/textarea').send_keys(conf_access['reason'])
    # 填入：入校前所在区
    # TODO：现在是写死成海淀区，以后考虑加其他支持
    do_selection(driver, '/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[2]/div/div/div[1]/div/input', '/html/body/div[3]/div[1]/div[1]/ul','海淀区')
    # 填入：居住地所在街道
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[3]/div/div/div[1]/textarea').send_keys(conf_access['street'])
    # 填入：是否入校14天，根据入校日期自动判断
    if (date.today() - date(*conf_access['BJdate'])).days >= 13:
        driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[4]/div/div/div/label[1]/span[1]/span').click()
    else:
        driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[4]/div/div/div/label[2]/span[1]/span').click()
        # 填入日期选择框，需要先删除只读属性再send_text
        driver.execute_script('document.querySelector("body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-22.el-col-sm-22.el-col-md-20.el-col-lg-16 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div > div:nth-child(8) > div:nth-child(2) > div:nth-child(5) > div > div > div.el-date-editor.el-input.el-input--prefix.el-input--suffix.el-date-editor--date > input").readOnly=false;')
        driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[5]/div/div/div/input').clear()
        driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[8]/div[2]/div[5]/div/div/div/input').send_keys(str(date(*conf_access['BJdate'])))
        driver.execute_script('document.querySelector("body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-22.el-col-sm-22.el-col-md-20.el-col-lg-16 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div > div:nth-child(8) > div:nth-child(2) > div:nth-child(5) > div > div > div.el-date-editor.el-input.el-input--prefix.el-input--suffix.el-date-editor--date > input").readOnly=true;')
    # 点击：承诺
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[9]/div/div/label/span[1]/span').click()
    # 点击：保存，提交
    driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[2]/main/div[1]/div[2]/form/div/div[10]/div/div/div/div[1]/button').click()
    time.sleep(1)
    driver.find_elements_by_tag_name('button')[-1].click()
    time.sleep(1)
    driver.find_elements_by_tag_name('button')[-1].click()
    time.sleep(1)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/button[2]'))
    # ).click()
    # time.sleep(1)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def epidemic(driver, input_temperature):
    # TODO 入校后的云战役多了一些新的项，处理一下
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
    # epidemic(driver, conf['input_temperature'])
    # driver.quit()
    
    epidemic_access_out(driver,conf['epidemic_access'])
    epidemic_access_in(driver,conf['epidemic_access'])
    
