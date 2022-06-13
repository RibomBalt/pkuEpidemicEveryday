from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import json
import os
import time
import pickle
from getpass import getpass
import re
from zipfile import ZipFile
import logging

# from datetime import date

def uspw_input(db_name = 'uspw.dat'):
    '''use pickle
    '''
    us = input('Please input Your Student ID: ')
    pw = getpass('Please input your Password: ')
    print('In this version only Edge Browser on Windows is supported.')
    engine_name = 'Edge'
    engine_path = input('Please input the ABSOLUTE PATH of folder of msedgedriver.exe\n(if empty, the webdriver.exe will be downloaded the same directory)\n: ')
    if not engine_path:
        engine_path = './msedgedriver.exe'
    else:
        engine_path = os.path.join(engine_path, 'msedgedriver.exe')

    conf = {'stuid': us, 'passwd': pw, 'webdriver_path': engine_path, 'driver_name': engine_name}
    with open(db_name, 'wb') as f:
        pickle.dump(conf, f)
    return conf



def iaaa_login(conf:dict, headless=False):
    # read conf.json
    # with open(config_fname,'r',encoding='utf-8') as f:
    #     content = f.read()
    # conf = json.loads(content)

    stuid = conf['stuid']
    passwd = conf['passwd']
    webdriver_path = conf['webdriver_path']
    # default path
    if not webdriver_path:
        webdriver_path = './msedgedriver.exe'

    # create selenium driver
    try:
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

    except (SessionNotCreatedException, WebDriverException) as e:
        # webdriver conflict
        try:
            this_edge_version = re.findall(r'Current browser version is ([0-9\.]+?) with', e.msg)[0]
        except:
            # webdriver not present at all, download a history version first
            r = requests.get('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
            this_edge_version = re.findall(r'Version: ([\d\.]+?):', r.text)[0]

        # TODO currently only win64-edge is supported
        r = requests.get('https://msedgedriver.azureedge.net/{0}/edgedriver_win64.zip'.format(this_edge_version))
        with open('webdriver.zip', 'wb') as f:
            f.write(r.content)
        driver_zip = ZipFile('webdriver.zip', 'r')
        driver_zip.extract('msedgedriver.exe', os.path.dirname(conf['webdriver_path']))
        # rerun
        driver = getattr(webdriver, conf['driver_name'])(webdriver_path)

    except Exception:
        raise

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
    2022.6.6
    园区往返填报，
    '''
    # locate 学生出入校 on portal
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

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'el-card'))
    )
    butns = driver.find_elements(By.CLASS_NAME, 'el-card')
    dict(zip([butn.text for butn in butns], butns))['园区往返申请'].click()

    # insert jQuery no conflicts
    driver.execute_script('''
        jQ_ele = document.createElement("script");
        jQ_ele.type = "text/javascript"
        jQ_ele.src = "https://code.jquery.com/jquery-2.2.4.min.js";
        document.getElementsByTagName('html')[0].appendChild(jQ_ele);
        return 0;
    ''')
    WebDriverWait(driver, 10).until(
        lambda d:d.execute_script('try{$;return 1;}catch{return 0;}')
    )
    # Note: 第二天填报会缓存前一天的信息……
    
    # # attach id for certain elements
    # driver.execute_script('''
    #     $('label.el-form-item__label:contains("园区（出）")').parent().find('input').parent().attr('id','yuanquchu')
    #     $('label.el-form-item__label:contains("园区（入）")').parent().find('input').parent().attr('id','yuanquru')
    # ''')

    # # fill in forms of 园区（出） and 园区（入）
    # for item_id in ['yuanquchu', 'yuanquru']:
    #     item = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.ID, item_id)),
    #     )
    #     item.click()
    #     WebDriverWait(driver, 10).until(
    #         lambda d:d.execute_script('''
    #         return $('ul').parent().parent().parent('div.el-select-dropdown:visible').find('ul').length
    #         ''')
    #     )
    #     driver.execute_script('''
    #         $('ul').parent().parent().parent('div.el-select-dropdown:visible').find('ul').attr('id', 'focus_ul')
    #     '''.format(item_id))
    #     li_focus = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "focus_ul"))
    #     ).find_elements_by_tag_name('li')
    #     # TODO add this to conf file
    #     time.sleep(.5)
    #     access_list = ['燕园', '物理学院']
    #     for li in li_focus:
    #         if li.text in access_list:
    #             li.click()
    #     # resume focus 
    #     time.sleep(.5)
    #     driver.execute_script('''
    #         $('#{0}').click();
    #         $('#focus_ul').removeAttr('id');
    #     '''.format(item_id))

    #     WebDriverWait(driver, 10).until(
    #         lambda d:d.execute_script('''
    #         return !$('ul').parent().parent().parent('div.el-select-dropdown:visible').find('ul').length
    #         ''')
    #     )

    # # fill in 出入校具体事项
    # driver.execute_script('''
    #         $('label.el-form-item__label:contains("出入校具体事项")').parent().find('textarea').attr('id', 'focus_crxjtsx')
    #     ''')
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, 'focus_crxjtsx'))
    # ).send_keys('科研工作：物理楼419')

    # 2022.6.13: new 5sec check
    time.sleep(6)
    driver.execute_script('''
            $('button.el-button--primary').find('span:contains("确定")').parent().attr('id', 'focus_queding');
            $('span:contains("保存")').attr('id', 'focus_save');
            $('span:contains("提交")').attr('id', 'focus_submit');
        ''')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'focus_queding'))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'focus_save'))
    ).click()

    # wait for msgbox to be present
    WebDriverWait(driver, 10).until(
        lambda d:d.execute_script('''
            return $('div.el-message-box__btns').find('button.el-button--primary').length
        ''')
    )
    driver.execute_script('''
            $('div.el-message-box__btns').find('button.el-button--primary').attr('id', 'focus_msg_submit');
    ''')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'focus_msg_submit'))
    ).click()
    print('填报完成')

def epidemic_access_211123(driver:webdriver.Edge):
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


if __name__ == "__main__":
    # log
    logging.basicConfig(level=logging.ERROR,
         filename='errlog.log', 
         format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    try:
        if not os.path.isfile('uspw.dat'):
            conf = uspw_input()
        else:
            with open('uspw.dat', 'rb') as f:
                conf = pickle.load(f)

        driver, conf = iaaa_login(conf, headless=False)
        # epidemic(driver, conf['input_temperature'])
        # driver.quit()
        
        epidemic_access(driver)
    except Exception:
        logging.error('Error in Selenium', exc_info=True)
        # TODO when error, arrange a redo / send email notification
        raise

    # with open('exit_school.log','a') as f:
    #     f.write('%s\n'%(time.asctime(time.localtime()),))
    driver.quit()

    
