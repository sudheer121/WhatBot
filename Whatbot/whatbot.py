#!/usr/bin/python
# -*- coding: utf-8 -*-
import bs4
import time
import re
from selenium import webdriver
browser = webdriver.Chrome()  # chromedriver used here
browser.get('https://web.whatsapp.com')


# This function sends the message passed to it on Whatsapp
def sender(browser, message):
    import time
    msg = browser.find_element_by_class_name('_13mgZ')
    msg.click()
    msg.send_keys(message)
    browser.maximize_window()  # window maximized
    browser.implicitly_wait(1)
    button = \
        browser.find_element_by_css_selector('#main > footer > div._2i7Ej.copyable-area > div:nth-child(3) > button'
            )


# This function scrapes data from Amazon.in and returns top 5 results
def amznurl(browser, item):  # forms list of products
    import requests
    import bs4
    import re
    import random
    url = 'https://www.amazon.in/s?k=' + item
    res = requests.get(url,
                       headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
                       })
    try:
        res.raise_for_status()
    except:

        print 'Something went wrong here'
        return
    finally:

        useless = 'string'
    soup = bs4.BeautifulSoup(res.text, 'html.parser')  # bsobj
    tags = soup('a')
    obj = re.compile(r'href="/.*/dp/.*?"')
    final = []

    for i in range(1, 90):
        x = str(tags[i])
        mo = obj.findall(x)
        if len(mo) > 0:
            final.append('https://www.amazon.in' + mo[0].strip('href="'
                         ).strip('#customerReviews'))  # final list of items
        b = []  # final list of items
        for x in final:
            if x not in b:
                b.append(x)
    for i in range(5):  # getting top 5 products result
        time.sleep(random.randint(1, 3))  # avoiding getting blocked
        try:
            res = requests.get(b[i],
                               headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
                               })
        except:
            print "Things go wrong sometimes,it's ok"
            return
        finally:
            useless = 'string'
        funcamzn(browser, res)


def funcamzn(browser, res): # Scrapes data from final html.
    import bs4
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elem = soup.findAll('span', {'id': 'productTitle',
                        'class': 'a-size-large'})
    elem2 = soup.findAll('span', {'id': 'priceblock_ourprice'})
    try:
        sender(browser, str(elem[0].text.strip()) + ' Cost:'
               + str(elem2[0].text.strip()))
    except:
        print "it's the site,not you"
        return


def translator(browser, str1): # This function gives Hindi Translation of words
    import bs4
    import time
    from selenium import webdriver
    bro = webdriver.Chrome()
    bro.get('https://translate.google.com/#view=home&op=translate&sl=auto&tl=hi&text='
             + str1)
    time.sleep(1)

    # chrome.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    try:
        msg2 = \
            bro.find_element_by_css_selector('body > div.frame > div.page.tlid-homepage.homepage.translate-text > div.homepage-content-wrap > div.tlid-source-target.main-header > div.source-target-row > div.tlid-results-container.results-container > div.tlid-result.result-dict-wrapper > div.result.tlid-copy-target'
                )
        sender(browser, msg2.text)
    except:
        print 'Something went wrong'
    finally:
        print 'hi'


def temp(browser, city):
    import requests
    import bs4
    try:
        res = requests.get('https://www.timeanddate.com/weather/india/'
                           + city + '/ext')
    except:
        sender(browser, 'only indian cities, result not found')
        return
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elem = soup.select('#qlook > div.h2')
    print elem[0].text
    sender(browser, 'Its' + str(elem[0].text))


time.sleep(5)  # Scan QR code
my_user = input('Enter Whatsapp name of person ')  # Enter person's name in shell
user = browser.find_element_by_xpath('//span[@title="' + my_user + '"]')
user.click()
lis = []

# hardcoded dictionary for a little interation
useless_dict = {
    'hello': 'hi human ',
    'hi': 'hello!!! human',
    'how are you': 'fine and working',
    'how are you ?': 'fine and working',
    'hello,how are you ?': 'i am fine and working',
    }


# Listening to user input on whatsapp chat
while True:
    lis.clear()
    time.sleep(2)
    exp = \
        browser.find_elements_by_xpath('//span[@dir="ltr"][@class="selectable-text invisible-space copyable-text"]'
            )
    for i in range(len(exp)):
        lis.append(exp[i].text)
    x = lis[len(lis) - 1]  # last element

    if x.lower() == 'hello bot' or x.lower() == 'activate bot':
        sender(browser, 'infobot activated')
    elif x.lower() == 'turn off':

        sender(browser, 'infobot deactivated')
        break
    elif x[:7].lower() == 'cost of':

        sender(browser, 'wait....')
        items = x.split(' ')
        item = '+'.join(items[2:])
        amznurl(browser, item)
        sender(browser, 'session ended')
    elif x[:9].lower() == 'translate':

        sender(browser, 'wait....')
        items = x.split(' ')
        translator(browser, items[1])
    elif x[:14].lower() == 'temperature of':

        items = x.split(' ')
        if len(items) == 3:
            temp(browser, items[2].lower())
    elif x.lower() == 'help':

        msg = \
            '''INSTRUCTIONS ARE BELOW
                     1)For activating type -> hello bot or activate bot
                     2)For temperature type -> temperature of indian_cityname
                     3)For hindi translation type -> translate word
                     4)For getting costs of product typr -> cost of productname
                     5)Does reply to some hi/hello messages
                   '''
        sender(browser, msg)
    else:
        try:
            rep = useless_dict[x.lower()]
            sender(browser, rep)
            sender(browser, 'for help type help')
        except:
            pass
