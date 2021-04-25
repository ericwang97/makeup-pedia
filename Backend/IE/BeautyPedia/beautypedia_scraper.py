from selenium import webdriver
from bs4 import BeautifulSoup
from chemdataextractor import Document
import pandas as pd
from tqdm import tqdm
import copy
import time
import re
import requests
import json


def get_product_links(start_page):
    product_links = []
    product_names = []

    browser = webdriver.Chrome('/usr/local/opt/WebDriver/bin/chromedriver')
    browser.get(start_page)
    # time.sleep(3)

    # select 96 items per page so we can loop less pages
    el = browser.find_element_by_class_name('results-per-page')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == '96':
            option.click()  # select() in earlier versions of webdriver
            break
    time.sleep(3)
    # find how many pages we have to loop
    i = 1
    npage = int(browser.find_element_by_class_name("archive-pagination-select").text.replace('\n', ' ').split()[-1])
    print('page (%d total) - first product' % npage)
    while True:
        soup = BeautifulSoup(browser.page_source, "html5lib")
        links = soup.find_all('a', class_="review-product")
        print("%6d  %s" % (i, links[0].text))
        product_links += [link['href'] for link in links]
        product_names += [link.text for link in links]
        if i == npage:
            break
        else:
            time.sleep(5)  # wait a few seconds -- be gentle to the server
            browser.find_element_by_class_name('next-page').click()  # click next-page button
            el = browser.find_element_by_class_name('results-per-page')
            for option in el.find_elements_by_tag_name('option'):
                if option.text == '96':
                    option.click()  # select() in earlier versions of webdriver
                    break
            i = i + 1
            time.sleep(5)
    browser.close()

    return product_links, product_names


def get_product_by_category(category_list, excluded_category):
    for i, item in enumerate(category_list):
        category = item.text.replace('\n', '').replace('\t', '')
        if category in excluded_category:
            continue
        print('collecting data for ', category)
        product_links, product_names = get_product_links(item['href'])
        for link, name in zip(product_links, product_names):
            record = {'product_links': link, 'product_names': name, 'category': 'Makeup Tools',
                      'sub_category': category}
            mega_data.append(record)
    # return mega_data


def fetch_product(mega_data):
    for i in tqdm(range(4082, len(mega_data))):
        mega_data[i]['product_id'] = i
        mega_data[i]['product_links'] = mega_data[i]['product_links'].split('?archive_search')[0]
        mega_data[i]['brand'] = None
        mega_data[i]['ingredient'] = None
        mega_data[i]['size'] = None
        mega_data[i]['price'] = None
        mega_data[i]['claims'] = None
        mega_data[i]['image_url'] = None
        mega_data[i]['expert_rating'] = None
        mega_data[i]['expert_reviews'] = None
        mega_data[i]['expert_pros'] = None
        mega_data[i]['expert_cons'] = None
        mega_data[i]['jar_package'] = None
        mega_data[i]['animal_test'] = None
        mega_data[i]['user_rating'] = None
        mega_data[i]['user_reviews'] = None

        browser = webdriver.Chrome('/usr/local/opt/WebDriver/bin/chromedriver')
        browser.get(mega_data[i]['product_links'])
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, "html5lib")

        # brand
        brand = soup.find('h2')
        if brand is not None:
            mega_data[i]['brand'] = brand.text

        # ingredient
        ingredient = soup.find('div', class_=re.compile("content-item ingredients"))
        if ingredient is not None:
            mega_data[i]['ingredient'] = ingredient.text.strip()

        # size
        size = soup.find('span', class_=re.compile("size"))
        if size is not None:
            mega_data[i]['size'] = size.text

        # price
        price = soup.find('span', class_=re.compile("price"))
        if price is not None:
            mega_data[i]['price'] = price.text

        # claims
        claims = soup.find('div', id="claims")
        if claims is not None:
            mega_data[i]['claims'] = claims.text

        # image
        img_url = soup.find('div', class_="product-image").find('img')['src']
        if img_url is not None:
            mega_data[i]['image_url'] = img_url

        # expert_rating
        expert_rating = soup.find('div', class_="expert-rating").find('span')['class']
        if expert_rating is not None:
            expert_rating = expert_rating[-1].split('-')[-1]
            mega_data[i]['expert_rating'] = expert_rating

        # expert_reviews
        expert_review_content = soup.find('div', id="expert")
        if expert_review_content is not None:
            expert_reviews = expert_review_content.find('div', class_="review-content").find_all('p')
            if len(expert_reviews) != 0:
                # expert_reviews = '\n'.join(expert_reviews)
                mega_data[i]['expert_reviews'] = [i.text for i in expert_reviews]

        # expert_pros
        expert_pros = soup.find('div', class_="review-pros")
        if expert_pros is not None:
            expert_pros = expert_pros.find('ul').find_all('li')
            if len(expert_pros) != 0:
                mega_data[i]['expert_pros'] = [i.text for i in expert_pros]

        # expert_cons
        expert_cons = soup.find('div', class_="review-cons")
        if expert_cons is not None:
            expert_cons = expert_cons.find('ul').find_all('li')
            if len(expert_cons) != 0:
                mega_data[i]['expert_cons'] = [i.text for i in expert_cons]

        # jar_package
        jar_package = soup.find('div', class_=['stat', 'jar_packaging'])
        if jar_package is not None:
            jar_package = jar_package.find('span', class_="value").text
            mega_data[i]['jar_package'] = jar_package

        # animal_test
        animal_test = soup.find('div', class_=['stat', 'tested-on-animals'])
        if animal_test is not None:
            animal_test = animal_test.find('span', class_="value").text
            mega_data[i]['animal_test'] = animal_test

        # user_rating
        user_rating = soup.find('div', class_="pr-snippet-rating-decimal")
        if user_rating is not None:
            user_rating = user_rating.text
            if user_rating != '0.0':
                mega_data[i]['user_rating'] = float(user_rating)

        # user_review
        browser.find_element_by_xpath("//div[@class='tab-titles']/h3[2]").click()
        time.sleep(1)

        usr_review_summary = None
        usr_review_details = None

        ##user_review_summary
        usr_review_count = None
        usr_pros_summary = None
        usr_cons_summary = None

        usr_review_summary_content = soup.find('section', id="pr-review-snapshot")
        if usr_review_summary_content is not None:
            usr_review_count = usr_review_summary_content.find('span', class_="pr-snippet-review-count").text
            usr_review_count = int(re.search("(\d+)", usr_review_count).group(1))

            usr_pros_block = usr_review_summary_content.find('section', class_="pr-review-snapshot-block-pros")
            if usr_pros_block is not None:
                usr_pros_summary = usr_pros_block.find_all('dd', class_="pr-snapshot-tag-def")
                usr_pros_summary = [[p.text for p in r.find_all('span')] for r in usr_pros_summary]
            if usr_pros_summary == [[]]:
                usr_pros_summary = None

            usr_cons_block = usr_review_summary_content.find('section', class_="pr-review-snapshot-block-cons")
            if usr_cons_block is not None:
                usr_cons_summary = usr_cons_block.find_all('dd', class_="pr-snapshot-tag-def")
                usr_cons_summary = [[p.text for p in r.find_all('span') if r.find_all('span') is not None] for r in
                                    usr_cons_summary]
            if usr_cons_summary == [[]]:
                usr_cons_summary = None

            usr_review_summary = {'usr_review_count': usr_review_count, 'usr_pros_summary': usr_pros_summary,
                                  'usr_cons_summary': usr_cons_summary}

        ##user_review_details
        next_flag = True
        positive_reviews = []
        negative_reviews = []
        reviews = []
        while next_flag:
            usr_review_details_content = soup.find('section', id="pr-review-display")
            if usr_review_details_content is not None:
                review_title = None
                review_rating = None
                review_content = None
                review_cons = None
                review_pros = None
                review_best_for = None
                usr_routine_time = None
                usr_def_tag = None
                usr_age = None
                usr_skin_type = None

                el = browser.find_elements_by_class_name('pr-accordion-btn')
                for b in el:
                    # b.click()
                    browser.execute_script("arguments[0].click();", b)
                    time.sleep(1)

                usr_reviews_block = usr_review_details_content.find_all('div', class_="pr-review")

                for review in usr_reviews_block:
                    review_title = review.find('span', class_=['pr-rd-review-headline', 'pr-h2']).text
                    review_rating = review.find('span', class_="pr-accessible-text").text
                    review_rating = re.findall('\d+', review_rating)[0]
                    review_content = review.find('p', class_="pr-rd-description-text").text

                    review_tags = review.find_all('dl', class_="pr-rd-review-tag")
                    for tag in review_tags:
                        if tag.find('dt').text == 'Cons':
                            review_cons = [t.text for t in tag.find_all('dd')]
                        if tag.find('dt').text == 'Pros':
                            review_pros = [t.text for t in tag.find_all('dd')]
                        if tag.find('dt').text == 'Best for':
                            review_best_for = [t.text for t in tag.find_all('dd')]

                    review_usr_tags = review.find_all('dl', class_="pr-rd-def-list")
                    for tag in review_usr_tags:
                        if tag.find('dt').text == 'My Beauty Routine Takes':
                            usr_routine_time = tag.find('dd').text
                        if tag.find('dt').text == 'Describe Yourself':
                            usr_def_tag = [t.text for t in tag.find_all('dd')]
                        if tag.find('dt').text == 'Age':
                            usr_age = tag.find('dd').text
                        if tag.find('dt').text == 'Skin Type':
                            usr_skin_type = tag.find('dd').text

                    review_record = {'review_title': review_title, 'review_rating': review_rating,
                                     'review_content': review_content, 'review_cons': review_cons,
                                     'review_pros': review_pros, 'review_best_for': review_best_for,
                                     'usr_routine_time': usr_routine_time, 'usr_def_tag': usr_def_tag,
                                     'usr_age': usr_age, 'usr_skin_type': usr_skin_type}

                    bottom_line = review.find('p', class_=["pr-rd-bottomline", "pr-rd-inner-content-block"])
                    if bottom_line is not None:
                        text_content = bottom_line.find_all('span')
                        for text in text_content:
                            if text.text != "Bottom Line":
                                attitude = text.text.split(',')[0].strip()
                                if attitude == "No":
                                    negative_reviews.append(review_record)
                                if attitude == "Yes":
                                    positive_reviews.append(review_record)
                    else:
                        reviews.append(review_record)

                try:
                    next_btn = browser.find_element_by_xpath(
                        "//a[@class='pr-rd-pagination-btn' and @aria-label='Next']")
                    browser.execute_script("arguments[0].click();", next_btn)
                    time.sleep(1)
                except:
                    next_flag = False
            else:
                next_flag = False

        if len(positive_reviews) == 0:
            positive_reviews = None
        if len(negative_reviews) == 0:
            negative_reviews = None
        if len(reviews) == 0:
            reviews = None
        usr_review_details = {'positive_reviews': positive_reviews, 'negative_reviews': negative_reviews,
                              'reviews': reviews}

        mega_data[i]['user_reviews'] = {'usr_review_summary': usr_review_summary,
                                        'usr_review_details': usr_review_details}

        with open('./bp_makeup_mega_data.jl', 'a+', encoding="utf8") as f:
            json.dump(mega_data[i], f)
            f.write('\n')

        browser.close()


if __name__ == "__main__":
    url = 'https://www.beautypedia.com/makeup'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    makeup_cat = soup.find_all('a', class_="submenu-item", href=re.compile('/makeup/'))[:30]
    excluded_category = ['Best & Worst Makeup Products']
    mega_data = get_product_by_category(makeup_cat, excluded_category)
    fetch_product(mega_data)

    # BP Ingredient Extraction
    ingredent = set()
    with open('bp_makeup_mega_data.jl', 'r', encoding='utf8') as f:
        bp_data = f.readlines()
        for r in bp_data:
            record = json.loads(r)
            cleaned_record = copy.deepcopy(record)
            cleaned_record['ingredient'] = []
            if record['ingredient'] is not None:
                record_ingredients = re.split(',  |, |,', record['ingredient'])
                for term in record_ingredients:
                    # ingre_text = ', '.join(record_ingredients)
                    for i in Document(term).cems:
                        chemical_name = i.text.replace('\n', '')
                        cleaned_record['ingredient'].append(chemical_name)
                        if chemical_name not in ingredent:
                            ingredent.add(chemical_name)
            with open('beautypedia_clean_ingr.jl', 'a+', encoding='utf8') as of:
                json.dump(cleaned_record, of)
                of.write('\n')

    # Generate Ingredient File
    index = 0
    with open('bp_ingredient.jl', 'w', encoding="utf8") as f:
        for ing in ingredent:
            json.dump({'id': index, 'ingredient': ing}, f)
            f.write('\n')
            index += 1
