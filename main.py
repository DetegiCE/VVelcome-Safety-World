import vvelcome
import getpass
import sys

id = input("포털 ID : ")
pw = getpass.getpass("포털 PW : ")

mode = input("OS 선택\n1 : MacOS\n2 : MacOS M1\n3 : Windows\n4 : Linux\n> ")

driver = vvelcome.init_driver(int(mode)-1)
vvelcome.portal_login(driver, id, pw)
vvelcome.access_edupage(driver)

enrol = input("[INFO] 본인 학과에 따른 교육 이수 조건을 확인하여 자신에게 맞는 과목을 수강신청 완료한 뒤 1을 입력하고 엔터를 치세요\n> ")

if not enrol:
    print('[WARN] 프로그램을 종료합니다')
    sys.exit()

enrolled_list = vvelcome.get_enrolled(driver)
vvelcome.auto_take_class(driver, enrolled_list)
vvelcome.auto_take_test(driver, enrolled_list)
vvelcome.alert_finish(driver)