from systemtools.file import getAllNumbers
from systemtools.logger import logException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import locale
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import itertools
from scroller.scroller import smartScroll, getPageInfos, scrollTo
import os
import sys
import csv
from scroller import *
#
#
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
class11 = 'module even-or-odd admin_stamped wf-see-more-widget'
class2 = 'module'
class33 = 'module even-or-odd created_at wf-see-more-widget'
class44 = 'module even-or-odd order_asc wf-see-more-widget'
class55 = 'module even-or-odd hits_count wf-see-more-widget'
macommande = 'https://forum.bouyguestelecom.fr/'
today = date.today()
yesterday = date.today() - datetime.timedelta(days=1)
forum_links = []
driver = webdriver.Chrome('/Users/ossama/Downloads/chromedriver_win32/chromedriver')
home_driver= 'https://forum.bouyguestelecom.fr/'
driver.get(home_driver)
time.sleep(1)
question_tlt = ''
DATE_FORMAT = "%d %B %Y"
#to accept cookies popup()
def accept_cookies_popup():
    try:
        # checking for the first page to click the cookies pop-up
        AcceptButton = driver.find_element(By.ID, 'popin_tc_privacy_button_3')
        AcceptButton.click()
    except BaseException as e:
        print('no cookies popup!!', str(e))
accept_cookies_popup()

#to click the view more button
def view_more(dclass): #VOIR PLUS DE QUESTIONS
    #voir plus xpath changes when clicking the dropdown options so we added  the paramater dclass
    #dclass will change whenever a click occurs(see get_categorie_questions_links )
    # clicking see more button
    seemore = driver.find_element(By.XPATH, '//*[@class="' + str(dclass) + '"]/div[2]/div[2]/div/a')
    seemore.click()


def get_answers(driver):
    main = driver.find_elements_by_css_selector("#yui-main")
    for m in main:
        # answers
        answers = m.find_elements_by_css_selector("div.answers.answers-tab.tab > div.answer ")
        answers_data = []
        for answer in answers:
            user = answer.find_element_by_css_selector("div.corpus > div.metadata > dl.author-name > dd").get_attribute(
                'innerText').strip()
            user_score = answer.find_element_by_css_selector("div.user > dl.score > dd > strong").get_attribute(
                'innerText').strip()
            user_level = answer.find_element_by_css_selector("div.user > dl.level > dd").get_attribute(
                'innerText').strip()
            answer_date = answer.find_element_by_css_selector(
                "div.corpus > div.metadata > dl.date > dd ").get_attribute('innerText').strip()
            answer_date = datetime.datetime.strptime(answer_date, DATE_FORMAT).date()
            print(answer_date)
            user_answer = answer.find_element_by_css_selector("div.corpus > div.body > div.body-bd").get_attribute(
                'innerText').strip()
            qt = "reponse"
            ah = ""
            answers_data.append(
                {"type": qt,"title": ah, "author": user, "date": answer_date,
                 "text": user_answer})

    return answers_data


def get_question(driver):
        questions_data = []
        main = driver.find_elements_by_css_selector("#yui-main")
        for m in main:
            # questions
            questions = m.find_elements_by_css_selector("div.question > div.corpus ")
            for question in questions:
                question_header = question.find_element_by_css_selector("h1 > a").get_attribute('innerText').strip()
                author = question.find_element_by_css_selector("div.metadata > dl.author-name > dd").get_attribute(
                    'innerText').strip()
                date = question.find_element_by_css_selector("div.metadata > dl.date > dd").get_attribute(
                    'innerText').strip()
                date = datetime.datetime.strptime(date, DATE_FORMAT).date()
                print(date)
                question_text = question.find_element_by_css_selector("div.body > div.body-bd").get_attribute(
                    'innerText').strip()
                qt = "question"
                questions_data.append(
                    {"type":qt,"title": question_header, "author": author, "date": date, "text": question_text})
        return questions_data
def get_categorie_questions_links_and_data(driver):

    data = []
    data.clear()
    selects = driver.find_elements(By.XPATH,'//select[@id="sort_by"]//option')
    for count, select in enumerate(selects, start=1):
        sel = driver.find_element(By.XPATH,'//select[@id="sort_by"]//option['+str(count)+']')
        sel.click()
        time.sleep(1)
        # clicking see more button
        if count == 1:
           view_more(class11)
           links = driver.find_elements_by_css_selector("div.ipl_widget > div.module.even-or-odd.admin_stamped.wf-see-more-widget > div.bd > div.b > ul > li.questions-content > div.question > div.corpus ")
        elif count == 2:

            view_more(class33)
            links = driver.find_elements_by_css_selector("div.ipl_widget > div.module.even-or-odd.created_at.wf-see-more-widget > div.bd > div.b > ul > li.questions-content > div.question > div.corpus ")
        elif count == 3:
            view_more(class44)
            links = driver.find_elements_by_css_selector("div.ipl_widget > div.module.even-or-odd.order_asc.wf-see-more-widget > div.bd > div.b > ul > li.questions-content > div.question > div.corpus ")
        elif count == 4:
            view_more(class55)
            links = driver.find_elements_by_css_selector("div.ipl_widget > div.module.even-or-odd.hits_count.wf-see-more-widget > div.bd > div.b > ul > li.questions-content > div.question > div.corpus ")
        for link in links:
            question = link.find_element_by_css_selector("h3 > a").get_attribute('innerText').strip()
            href = link.find_element_by_css_selector("h3 > a").get_attribute("href")
            views = link.find_element_by_css_selector("div.metadata > dl.hits > dd").get_attribute('innerText').strip()
            responds = link.find_element_by_css_selector("div.metadata > dl.answer-count > dd").get_attribute('innerText').strip()
            author = link.find_element_by_css_selector("div.metadata > dl.author-name > dd").get_attribute('innerText').strip()
            date = link.find_element_by_css_selector("div.metadata > dl.date > dd").get_attribute('innerText').strip()
            date = datetime.datetime.strptime(date, DATE_FORMAT).date()
            content_type = link.find_element_by_css_selector("div.metadata > dl.content-type > dd").get_attribute('innerText').strip()
            print(date)
            if date == yesterday or date == today:
                is_in_file = 1
                if date == yesterday:
                    with open('Forum BT '+str(yesterday)+'D.csv', 'rt',encoding='utf8') as f:
                        reader = csv.reader(f, delimiter=',')
                        for row in reader:
                            if href in row:
                             is_in_file = 0
                    if is_in_file == 1:
                        print('appending (yesterday but not in csv)')
                        forum_links.append(href)
                        data.append({"link": href, "questoin_text": question, "responds": responds, "views": views,
                                 "author": author, "date": date, "content_type": content_type, })
                else:

                    print('appending (new day)')
                    forum_links.append(href)
                    data.append({"link": href, "questoin_text": question, "responds": responds, "views": views,
                             "author": author, "date": date, "content_type": content_type, })
            else:
                print('not in date range')
    return data

forum_links.clear()
categorie_name = driver.find_elements(By.XPATH, '//div[@class="name"]//strong//a')
for count, c_name in enumerate(categorie_name, start=1):
    forum_links.clear()
    #cat_class = class1
    #if count != 1:
     #   cat_class = class2
    categorie_name = driver.find_element(By.XPATH,
                                         '(//div[@class="name"]//strong//a)[' + str(
                                             count) + ']')
    print(" clicking categorie: "+ categorie_name.text)
    categorie_name.click()
    time.sleep(1)
    # getting question from each categorie
    cat_data = get_categorie_questions_links_and_data(driver)
    print(cat_data)
    aa_file = "dataa.csv"
    csv_columns = ['link', 'questoin_text', 'responds','views','author','date','content_type']
    with open(aa_file, 'a',encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for c_data in cat_data:
            writer.writerow(c_data)


    for link in forum_links:
        driver.get(link)
        print('im in question')
        get_q = get_question(driver)
        get_a = get_answers(driver)
        get_all = get_q + get_a
        time.sleep(1)
        print(get_q)
        print(get_a)
        a_file = "Forum BT "+str(today)+"D.csv"
        csvv_columns = ['type', 'title', 'author', 'date', 'text']
        with open(a_file, 'a',encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csvv_columns)
            writer.writeheader()
            for c_data in get_all:
                writer.writerow(c_data)
    print('done')
    # return to home page
    driver.get(home_driver)

driver.quit()
df = pd.read_csv("Forum BT "+str(today)+"D.csv")
df.to_parquet("Forum BT "+str(today)+"D.parquet")