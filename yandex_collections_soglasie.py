startrul = 'https://soglasie-ooo.ru/keramicheskaya-plitka/filter/brand-is-kerlayf/'  # адрес из которого будет создана коллекция и который нужно будет наполнять
log_type = 2  #выбираем способ логина в Яндекс 1 - через форму, 2 - через куки
need_create = 0  #нужно ли создавать коллекцию 1 - нужно, 0 - не нужно
mode_add = 2  # режим добавления фото 1 - для добавления коллекций, 2 - для добавления карточек товаров


url_to_login_v1 = 'https://passport.yandex.ru/auth?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru'
login = 'yandex_login'
password = 'yandex_password'
url_to_login_v2 = 'https://yandex.ru/'
created_collection = 'collection_url' #адрес коллекции с которой работаем в режиме need_create = 0

import time
import random
import pickle
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.request import urlopen
from bs4 import BeautifulSoup
driver = webdriver.Firefox()

#Собираем список адресов для обработки 
starturllist = [startrul]
urls = []
bsObj = BeautifulSoup(urlopen(startrul),'lxml')
if bsObj.find('div',class_='pagination'):
    maxpag = bsObj.find('div',class_='pagination').findAll('li')[-1].previousSibling.previousSibling.get_text()
    for i in range(2,int(maxpag)+1):
        starturllist.append(startrul+'?PAGEN_2='+str(i))
else:
    starturllist = [startrul]
  
for i in starturllist:
    bsObject = BeautifulSoup(urlopen(i),'lxml')
    cards = bsObject.findAll('div',{'class':'item main_small-card'})
    for m in cards:
        urls.append('https://soglasie-ooo.ru'+m.a.attrs['href'])
print('Количество адресов - ', len(urls))

myname = 'Плитка '+bsObj.h1.text
desc = 'Плитка '+bsObj.h1.text+' это роскошный вариант для отделки ванной прихожей или кухни в доме.'

#логинимся в яндекс вариант 1
def login_yandex(aothurl):
    driver.get(aothurl)
    driver.find_element_by_id('passp-field-login').send_keys(login)
    #driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div/div/div[1]/form/div[3]/button[1]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "passp-sign-in-button"))).find_elements(By.TAG_NAME,'button')[0].click()
    #driver.find_element_by_id('passp-field-passwd').send_keys(password)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "passp-field-passwd"))).send_keys(password)
    #driver.find_element_by_css_selector('#root > div > div > div.passp-flex-wrapper > div > div.passp-auth > div.passp-auth-content > div.passp-route-forward > div > div > form > div.passp-button.passp-sign-in-button > button.control.button2.button2_view_classic.button2_size_l.button2_theme_action.button2_width_max.button2_type_submit.passp-form-button').click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#root > div > div > div.passp-flex-wrapper > div > div.passp-auth > div.passp-auth-content > div.passp-route-forward > div > div > form > div.passp-button.passp-sign-in-button > button.control.button2.button2_view_classic.button2_size_l.button2_theme_action.button2_width_max.button2_type_submit.passp-form-button"))).click()
    #Сохраняем куки в файл
    driver.get('https://yandex.ru/')
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb")) #сохраняем куки в файл



#логинимся в яндекс вариант 2 (через куки)
def login_yandex2(hosturl):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.get(hosturl)
    for cookie in cookies:
        driver.add_cookie(cookie)


if log_type == 1:
    login_yandex(url_to_login_v1)
if log_type == 2:
    login_yandex2(url_to_login_v2)

#Создаём коллекцию
def create_collect(name, desc):
    driver.get('https://yandex.ru/collections/')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tabs-head__side']/a"))).click() #нажимаем на создание коллекции
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='side__suggest__wrap']/p[3]"))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "input__input"))).send_keys(name)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "textarea__textarea_original"))).send_keys(desc)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button:nth-child(2)"))).click()
        time.sleep(5)
    except selenium.common.exceptions.TimeoutException:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[3]/div[4]/div[1]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cl-form-input__field"))).send_keys(name)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cl-form-textarea"))).find_element(By.TAG_NAME,'textarea').send_keys(desc)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div/div/div[1]/div/div[3]/button"))).click()
        time.sleep(5)
    global created_collection
    created_collection = driver.current_url
    #return created_collection 

if need_create == 1:
    create_collect(myname,desc)
    
#Добавляем фото в коллекцию
def add_photo(created_collection, url):
    driver.get(created_collection)
    title_collection = driver.find_element_by_xpath("//span[@class='cl-minor-header__title-text']").text
    time.sleep(random.randrange(6,11))
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Добавить"))).click()
    if mode_add == 1:
        #ниже блок добавки как url что хорошо для коллекций но плохо для товаров
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-type-list']/div[2]"))).click() #кликаем на "ссылка"
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "search-input"))).send_keys(url)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-input-search__container']/div[2]/div"))).click() #нажимаем на стрелочку
        time.sleep(1)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='board-list']/div/div[4]"))).click() #добавляем в коллекцию
			#/html/body/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[3] - картинка
			#/html/body/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4] - ссылка
        except:
            print('norm')
    if mode_add == 2:
        #блок добавки картинок
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-type-list']/div[1]"))).click() #кликаем на "картинки"
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-header__tabs']/div[2]"))).click() #выбираем загрузку из интернета
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "search-input"))).send_keys(url) #вводим адрес страницы
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-input-search__container']/div[2]/div"))).click() #нажимаем на стрелочку
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='add-column']/div[3]/div[2]/div/div"))).click() #выбираем первую картинку
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Добавить в коллекцию')]/.."))).click() #нажимаем выбрать коллекцию
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Выбрать коллекцию')]/.."))).click() #нажимаем выбрать коллекцию
            time.sleep(1)
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='board-list']/div/div[3]"))).click() #добавляем в коллекцию
            except:
                print('norm')
        except:
            print('добавлено в ту же коллекцию')
    if random.randint(0,4) <3:
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randrange(5,12))
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
    else:
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
        time.sleep(random.randrange(5,12))
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        

# Запускаем скрпит добавления в коллекции для каждого элемента списка
for j,i in enumerate(urls):
    while True: #конструкция сделана для обработки исключения и возврата к первому элементу списка
        try:
            add_photo(created_collection, i)
            print(j+1,i,'\n Осталось ',len(urls)-(j+1))
            time.sleep(random.randrange(5,10))
        except ElementClickInterceptedException:
            continue
        break	