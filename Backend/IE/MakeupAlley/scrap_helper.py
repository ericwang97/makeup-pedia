from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import re
import requests
import json

def get_category_links(start_url):
    browser = webdriver.Chrome('/usr/local/opt/WebDriver/bin/chromedriver')
    browser.get(start_url)
    time.sleep(3)
    category_links = []
    for i in range(0,5):
        cat_block = browser.find_element_by_xpath("//div[@class='category-selector-component']/select").find_elements_by_tag_name('optgroup')
        cat_i = cat_block[i]
        cat_name = cat_i.get_attribute('label')
        sub_cat_blocks = cat_i.find_elements_by_tag_name('option')
        for j in range(len(sub_cat_blocks)):
            sub_cat_name=sub_cat_blocks[j].text
            sub_cat_blocks[j].click()
            browser.find_element_by_class_name('mua-filter-reviews-btn').click()
            time.sleep(1)
            subcat_url = browser.current_url
            category_links.append({'category':cat_name,'sub_category':sub_cat_name,'url':subcat_url})

            browser.back()
            time.sleep(1)
            sub_cat_blocks = browser.find_element_by_xpath("//div[@class='category-selector-component']/select").find_elements_by_tag_name('optgroup')[i].find_elements_by_tag_name('option')
    browser.close()

    return category_links

def get_mua_product_links(category_links):
    browser = webdriver.Chrome('/usr/local/opt/WebDriver/bin/chromedriver')
    product_links = []
    for cat in category_links:
        browser.get(cat['url'])
        while True:
            el = browser.find_elements_by_xpath("//div[@class='col d-lg-none']/div[@class='details']")
            for r in el:
                product_name_el = r.find_element_by_class_name('item-name')
                product_name = product_name_el.text
                product_url_l = str(product_name_el.get_attribute('href'))
                product_id = int(re.search(r'(\d+)', product_url_l).group(0))
                product_url = product_url_l.split('=')[0] + '=' + str(product_id)+'/'
                
                product_record = {'product_name':product_name,'product_id':product_id,'product_url':product_url,'category':cat['category'],'sub_category':cat['sub_category']}
                product_links.append(product_record)
                with open('mua_makeup_data.jl','a+',encoding='utf8') as f:
                    json.dump(product_record,f)
                    f.write('\n')
            time.sleep(2)
            #next_page = browser.find_element_by_xpath("//li[@class='next']/a")
            try:
                browser.find_element_by_xpath("//li[@class='next']/a").click()
                next_content = browser.find_elements_by_class_name('prlc-results-list')
                if next_content == []:
                    break  
            except:
                break 
    browser.close()
    return product_links

def fetch_mua_product(product_links):
    product_details = []
    for p in tqdm(range(10000,len(product_links))):
        r = requests.get(product_links[p]['product_url'])
        soup = BeautifulSoup(r.text,"html5lib")
        #product_name
        product_header = soup.find('div',class_=['headline'])

        if product_header is None:
            continue
        product_name = product_header.find('h1').text

        if product_header.find('div') is None:
            brand_name = None
            brand_url = None 
            brand_id = None
        else:
            prodct_brand = product_header.find('div').find('h2').find('a')
            #brand_name
            brand_name = prodct_brand.text
            #brand_url
            brand_url = 'www.makeupalley.com'+prodct_brand['href']
            #brand_id
            brand_id = int(re.search(r'(\d+)', brand_url).group(0))
        
        #img_url
        img_source = soup.find('a',id='image-gallery-image-primary')
        if img_source is None:
            img_url = None
        else:
            img_url = img_source['href']

        #rating
        rating = soup.find('h3',class_='rating-value').text
        if rating =='':
            rating = None
        else:
            rating = float(rating)
        #review_cnt
        review_cnt = re.search(r'(\d+)',soup.find('a',class_='overall-rating').text)
        if review_cnt is not None:
            review_cnt = int(review_cnt.group(0))
        #repurchase_pct
        repurchase_pct = re.search(r'(\d+)',soup.find('span',class_='buyagain').text)
        if repurchase_pct is not None:
            repurchase_pct =float(repurchase_pct.group(0))
        #packaging_rate
        packaging_rate = soup.find('span',class_='packaging').text
        if packaging_rate =='':
            packaging_rate = None
        else:
            packaging_rate = float(packaging_rate)
        #product_description
        product_description = soup.find('p',class_='product-description')
        if product_description is not None:
            product_description = soup.find('p',class_='product-description').text
        else:
            None
        
        #Review
        reviews = []
        page_i=1
        while True:
            review_content = soup.find_all('article',class_='small-image-review')
            for review in review_content:
                user_name = review.find('div',class_='user-name').find('div').find('a').text
                user_url = 'www.makeupalley.com' + review.find('p',class_='reviewer').find('a')['href']
                details = review.find('div',class_='user-details').find_all('p')
                for d in details:
                    d_contents = d.find_all('span')
                    if d_contents[0].text =='Age':
                        user_age = d_contents[1].text
                    if d_contents[0].text =='Skin':
                        user_skin_type = d_contents[1].text.split(', ')
                    if d_contents[0].text =='Hair':
                        user_hair_style = d_contents[1].text.split(', ')
                    if d_contents[0].text =='Eyes':
                        user_eyes = d_contents[1].text
                #user_details
                user_details = {'user_name':user_name,'user_url':user_url,'user_age':user_age,'user_skin_type':user_skin_type,'user_hair_style':user_hair_style,'user_eyes': user_eyes}
                #rating
                user_rating = float(review.find('span',class_='rating-value').text)
                #review_text
                review_text = review.find('div',class_='product-review-text').find('div')['data-text']
                reviews.append({'user_details':user_details,'user_rating':user_rating,'review_text':review_text})
            
            page_i += 1
            time.sleep(1)
            r = requests.get(product_links[p]['product_url']+'?page='+str(page_i)+'#reviews')
            soup = BeautifulSoup(r.text,"html5lib")
            if soup.find_all('article',class_='small-image-review') ==[]:
                break
        
        record = {'product_name':product_name,'product_id':product_links[p]['product_id'],'product_url':product_links[p]['product_url'],'brand_name':brand_name,'brand_url':brand_url,'brand_id':brand_id,'img_url':img_url,'rating':rating,'review_cnt':review_cnt,'repurchase_pct':repurchase_pct,'packaging_rate':packaging_rate,'product_description':product_description,'reviews':reviews}
        product_details.append(record)
        with open('mua_mega_data.jl','a+',encoding='utf8') as f:
            json.dump(record,f)
            f.write('\n')
        time.sleep(2)


#category_links = get_category_links('https://www.makeupalley.com/product/searching')
#product_links = get_mua_product_links(category_links)

#reload product_links data
product_links = []
with open('mua_makeup_data.jl','r',encoding="utf8") as f:
    links_data = f.readlines()
    for i in links_data:
        product_links.append(json.loads(i))


fetch_mua_product(product_links)



