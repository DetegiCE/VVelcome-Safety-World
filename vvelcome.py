from selenium import webdriver
from time import time, sleep
from bs4 import BeautifulSoup
import re

def init_driver(mode):
    driver_list = ['chromedriver_mac_90', 'chrome_driver_mac_m1_90', 'chromedriver_win32_90.exe', 'chromedriver_linux64_90']
    driver = webdriver.Chrome('./driver/'+driver_list[mode])
    print('[INFO] Chrome Webdriver Loaded')
    return driver

def portal_login(driver, id, pw):
    driver.get('https://portal.korea.ac.kr')
    sleep(5)
    driver.find_element_by_name('id').send_keys(id)
    driver.find_element_by_name('pw').send_keys(pw)
    driver.find_element_by_xpath('//*[@id=\"loginsubmit\"]').click()
    print('[INFO] Portal Login Success')

def access_edupage(driver):
    sleep(3)
    driver.execute_script('moveProgram(\'http://infodepot.korea.ac.kr\', \'3\', \'/common/FMSLogin3.jsp?url=archibus\', \'86\', \'4960\', \'S\')')
    sleep(3)
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(5)
    driver.execute_script('sel_fnc()')
    sleep(3)
    driver.get('http://cafm.korea.ac.kr/archibus/safety_edu/selec_req_list.jsp')
    print('[INFO] Edu Page Access Success')

def get_enrolled(driver):
    driver.get('http://cafm.korea.ac.kr/archibus/safety_edu/selec_my_req_list.jsp')
    sleep(3)
    html = driver.page_source

    pattern = "mv_event\(\'\d{4}\/\d{2}\/index.jsp\',\'\d{1,2}\'\);"
    matchedList = re.findall(pattern, html)
    return matchedList

def build_ajax_payload(idx, totalTime):
    return '''$.ajax({
			url: "sub_entry.jsp",
			data: {"c_type":"save" ,''' + \
            f'''"chap_type": "{str(idx).zfill(2)}" ,"tstart": {math.ceil(time())}, "tend": {math.ceil(time())+totalTime}, "ct": {totalTime}''' + \
            '''
            },
			type:'post',
			dataType:'json',
			success:function(data){}
            });
            '''

def auto_take_class(driver, enrol_list):
    for elem in enrol_list:
        idx = int(elem[15:17])
        newurl = 'http://cafm.korea.ac.kr/archibus/safety_edu/'+elem[10:27]
        driver.get(newurl)
        sleep(3)
        html = driver.page_source
        
        pattern = "vEnt\(\'\d{2}\/\d{2}\'\)"
        matchedList = re.findall(pattern, html)
        for melem in matchedList:
            #print(melem)
            driver.execute_script(melem)
            sleep(6)
            driver.execute_script('document.getElementById("myVideo").currentTime = document.getElementById("myVideo").duration')
            sleep(1)
            driver.execute_script('closeBtn()')
            print(f'[INFO] Success SubClass ID {melem[6:11]}')
            sleep(3)
        print(f'[INFO] Success Class ID {idx}')
    print('[INFO] Success All Classes')

def auto_take_test(driver, enrol_list):
    driver.get('http://cafm.korea.ac.kr/archibus/safety_edu/selec_my_req_list.jsp')
    sleep(3)
    for elem in enrol_list:
        idx = elem[15:17]
        driver.execute_script('test_event(\''+str(idx)+'\',\'kor\')')
        driver.switch_to.alert.accept()
        sleep(5)

        driver.switch_to.window(driver.window_handles[-1])
        for i in range(1, 1000):
            try:
                s = driver.find_element_by_name('ans_'+str(i))
                driver.find_element_by_id(f'ans_{i}_1').click()
            except:
                break
        driver.execute_script('submitPage()')
        sleep(3)
        driver.switch_to.alert.accept()
        driver.switch_to.window(driver.window_handles[1])
        sleep(3)
        driver.execute_script(f'test_revent(\'{idx}\',\'kor\')')
        sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        answers = driver.find_elements_by_class_name('a_td1')
        answerList = [-1]
        countAnswer = 0
        for a in answers:
            countAnswer += 1
            if countAnswer % 2 == 0:
                answerList.append(a.text)
        #for a in answers:
        #    print(a.text)
        sleep(1)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        driver.execute_script('test_event(\''+str(idx)+'\',\'kor\')')
        driver.switch_to.alert.accept()
        sleep(5)

        driver.switch_to.window(driver.window_handles[-1])
        for i in range(1, 1000):
            try:
                s = driver.find_element_by_name('ans_'+str(i))
                try:
                    driver.find_element_by_id(f'ans_{i}_{answerList[i]}').click()
                except:
                    continue
            except:
                break
        driver.execute_script('submitPage()')
        sleep(3)
        driver.switch_to.alert.accept()
        driver.switch_to.window(driver.window_handles[1])
        sleep(3)
        print(f'[INFO] Success Test ID {idx}')
    print('[INFO] Success All Tests')

def alert_finish(driver):
    driver.execute_script('alert("자동 수강이 완료되었습니다.")')
    print('[INFO] Success!')