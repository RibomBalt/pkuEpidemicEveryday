from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
# from datetime import date


def iaaa_login(config_fname, headless=False):
    # read conf.json
    with open(config_fname,'r',encoding='utf-8') as f:
        content = f.read()
    conf = json.loads(content)
    stuid = conf['stuid']
    passwd = conf['passwd']
    webdriver_path = conf['webdriver_path']
    # create selenium driver
    if headless:
        # headless mode
        if conf['driver_name']=='Edge':
            options = webdriver.EdgeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gpu')
            
            driver = getattr(webdriver, conf['driver_name'])(webdriver_path, options=options)
        else:
            raise NotImplementedError('Currently on Edge is supported in headless mode')
    else:
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
    '''
    2021.11.23
    新的出入校填报越来越crazy了，不过填报似乎有所简化，可以填上次填过的内容
    所以这里也是，simply点击填入上一次，勾选确认，上传，结束
    '''
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
    driver.switch_to.window(driver.window_handles[1])
    # 填报
    for churu in ['出校申请信息','入校申请信息']:
        butns = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, 'el-card')
        )
        dict(zip([butn.text for butn in butns], butns))['出入校备案'].click()
        # 出校
        butns = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, 'el-button')
        )
        butn_dict = dict(zip([butn.text for butn in butns], butns))
        butn_dict[churu].click()
        cbox = driver.find_elements(By.CLASS_NAME, 'el-checkbox')
        assert '本人承诺' in cbox[0].text
        cbox[0].click()
        butn_dict['保存'].click()
        butns2 = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, 'el-button') if\
                '暂不提交' in [butn.text for butn in d.find_elements(By.CLASS_NAME, 'el-button')]\
                    else False
        )
        [butn.click() for butn in butns2 if butn.text=='提交' and butn not in butns]

        time.sleep(1)
        # 返回
        # driver.refresh()
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, 'el-message-box') and\
                 (not d.find_elements(By.CLASS_NAME, 'el-message-box')[0].is_displayed())
        )
        driver.find_elements(By.CLASS_NAME, 'el-page-header__left')[0].click()
        driver.refresh()

        # driver.find_elements(By.CLASS_NAME, 'el-page-header__left')[0].click()
        time.sleep(1)

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
    driver, conf = iaaa_login('conf.json', headless=False)
    # epidemic(driver, conf['input_temperature'])
    # driver.quit()
    
    # epidemic_access_out(driver,conf['epidemic_access'])
    # epidemic_access_in(driver,conf['epidemic_access'])
    epidemic_access(driver)
    with open('exit_school.log','a') as f:
        f.write('%s\n'%(time.asctime(time.localtime()),))

    
