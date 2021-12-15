# BBox Scraping

This project allows to crawl <https://forum.bouyguestelecom.fr>.

## Export format

Every message found (which can be either a question or an anwser) is exported following, at least, these columns:

 * **type**: either a question or a response (q || r)
 * **title**: the title of the question (if it's a question and not an answer)
 * **author**: the author name (note that authors are upper casd by the website)
 * **date**: a timestamp in seconds
 * **text**: the content of the message
# Python Functions : 

## 1-accept_cookies_popup
   ```python
   def accept_cookies_popup():
        try:
          # checking for the first page to click the cookies pop-up
          AcceptButton = driver.find_element(By.ID, 'popin_tc_privacy_button_3')
          AcceptButton.click()
        except BaseException as e:
          print('no cookies popup!!', str(e))
  ```
  A function to click the accept cookies popup
  ![popup](https://user-images.githubusercontent.com/59144753/146229545-6054692b-370d-4c5a-a9a5-dd10a91f0302.PNG)
## 2-view_more
   ```python
   def view_more(dclass):
    #voir plus xpath changes when clicking the dropdown options so we added  the paramater dclass
    #dclass will change whenever a click occurs(see get_categorie_questions_links_and_data )
    # clicking see more button
    seemore = driver.find_element(By.XPATH, '//*[@class="' + str(dclass) + '"]/div[2]/div[2]/div/a')
    seemore.click()
    
  ```
  A function to click the "Voir Plus" button in categories page
  ![seemore](https://user-images.githubusercontent.com/59144753/146230725-8d1c0618-8550-4b76-9a8f-21debac401ab.PNG)
  
  ## 3-get_categorie_questions_links_and_data
  start looping on each of the 11 categories
  ```python
   def get_categorie_questions_links_and_data(driver):

    data = []
    data.clear()
    selects = driver.find_elements(By.XPATH,'//select[@id="sort_by"]//option')
  ```
  getting every question link from the 4 options in the  combobox  :
  ![combo](https://user-images.githubusercontent.com/59144753/146231942-d6ec2ea2-5cbf-4da7-95a2-b5e1f0e8ec13.PNG)
  ```python
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
 ```
 Getting every question link and metadata : 
 ```python
        for link in links:
            question = link.find_element_by_css_selector("h3 > a").get_attribute('innerText').strip()
            href = link.find_element_by_css_selector("h3 > a").get_attribute("href")
            views = link.find_element_by_css_selector("div.metadata > dl.hits > dd").get_attribute('innerText').strip()
            responds = link.find_element_by_css_selector("div.metadata > dl.answer-count > dd").get_attribute('innerText').strip()
            author = link.find_element_by_css_selector("div.metadata > dl.author-name > dd").get_attribute('innerText').strip()
            date = link.find_element_by_css_selector("div.metadata > dl.date > dd").get_attribute('innerText').strip()
            date = datetime.datetime.strptime(date, DATE_FORMAT).date()
            content_type = link.find_element_by_css_selector("div.metadata > dl.content-type > dd").get_attribute('innerText').strip()
```
now if we're collecting the full version we'll use : 
```python
#to store only links to access them later
forum_links.append(href)
data.append({"link": href, "questoin_text": question, "responds": responds, "views": views,
                                 "author": author, "date": date, "content_type": content_type, })
 return data
```
if we want to collect the filtered version we have 

**option 1 :** collecting by day (getting only todays questions): 
```python
if  date == today # today is a variable contains the date of the day 
    forum_links.append(href)
    data.append({"link": href, "questoin_text": question, "responds": responds, "views": views,
                                 "author": author, "date": date, "content_type": content_type, })
    return data
```
**option 2 :** collecting by days (getting todays and yesterdays questions):
in this case we should have a yesterday csv file to compare the already existing questions  
```python
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

   
  ```
  ## 4-get_question :
  getting all questions from the links we stored in forum_links list and returning a structured dictionary: 
  ```python
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
  ```
  ## 5-get_answers
  getting every answer from every question and returning a structured dictionary
  ```python
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
  ```
