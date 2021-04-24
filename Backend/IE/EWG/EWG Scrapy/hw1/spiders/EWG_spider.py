import scrapy
import time
import json
import uuid
import pytz
from datetime import datetime
from scrapy.selector import Selector


def get_pst_time():
    utc = pytz.utc
    pst = pytz.timezone("US/Pacific")
    utc_date = datetime.utcfromtimestamp(time.time())
    utc_loc_time = utc.localize(utc_date)
    pst_time = utc_loc_time.astimezone(pst)

    return pst_time.strftime('%Y-%m-%dT%H:%M:%S')


class Spider(scrapy.Spider):
    name = "EWG"
    count = 0
    base_url = 'https://www.ewg.org'
    output_file = 'ewg_data.jl'
    output = open(output_file, 'w')

    def start_requests(self):

        input_file = './ewg_data_links.jl'

        with open(input_file, 'r') as file:
            for line in file:
                result = json.loads(line)
                task1_url = result['product_url']
                time.sleep(2)
                yield scrapy.Request(url=task1_url, callback=self.parse_product, meta={'result': result})

    def parse_product(self, response):
        site = Selector(response)
        result = response.meta['result']

        raw_name = site.xpath('//section[@id="product"]//h2[@class="product-name text-block"]/text()').extract()[0]
        brand = site.xpath('//section[@class="browse-more"]//ul[@class="mb40"]/li/a[@href]/div/text()').extract()
        if brand:
            brand_name = brand[0].strip()
            brand_url = self.base_url + site.xpath('//section[@class="browse-more"]//'
                                                   'ul[@class="mb40"]/li/a/@href').extract()[0]
        else:
            brand_name = ''
            brand_url = ''

        if ',' in raw_name:
            color = raw_name.split(', ')[1].strip()
            name = raw_name.split(', ')[0].replace(brand_name + ' ', '').strip()
        else:
            color = ''
            name = raw_name.replace(brand_name + ' ', '')

        """
        @TODO: ADD Where to purchase: I still use the Amazon.com to be the link if existed
        
        """
        buy_url = self.base_url + site.xpath('//section[@class="browse-more"]//'
                                             'ul[@class="mb40"]/li/a[@target="_blank"]/@href').extract()
        if len(buy_url) > 1:
            buy_url = buy_url[1]
        elif len(buy_url) == 1:
            buy_url = buy_url[0]
        else:
            buy_url = ''

        res = {'Name': name, 'Color': color, 'Brand Name': brand_name,
               'Brand URL': brand_url, 'Buy URL': buy_url}
        result.update(res)

        """
        @TODO: END

        """

        concerns = site.xpath('//section[@class="gauges grid"]//div[@class="gauge-img-wrapper"]/'
                              'img[@class="gauge-img"]/@alt').extract()[0:3]
        concerns_dict = dict([concern.split(' concern is ') for concern in concerns])

        other_concerns = site.xpath('//section[@id="other-concerns"]//li[@class="concern"]/text() | '
                                    '//section[@id="other-concerns"]/h5[@class]/text()').extract()
        other_concerns_dict = {}
        low_index = other_concerns.index('LOW')
        if 'MODERATE' in other_concerns:
            m_index = other_concerns.index('MODERATE')
            other_concerns_dict['HIGH'] = other_concerns[1:m_index]
            other_concerns_dict['MODERATE'] = other_concerns[m_index + 1:low_index]
            other_concerns_dict['LOW'] = other_concerns[low_index + 1:]
        else:
            other_concerns_dict['HIGH'] = other_concerns[1:low_index]
            other_concerns_dict['LOW'] = other_concerns[low_index + 1:]

        ingredient_scores = site.xpath('//section[@class="ingredient-concerns-table-wrapper"]//table[@class='
                                       '"table-ingredient-concerns"]/tbody//tr/td[@class="td-score"]/'
                                       'img[@class="ingredient-score score-popup"]/@src').extract()
        ingredient_scores = [int(score.split('score-')[1][:2]) for score in ingredient_scores]
        ingredient_avails = site.xpath('//section[@class="ingredient-concerns-table-wrapper"]//table[@class='
                                       '"table-ingredient-concerns"]/tbody//tr/td[@class="td-availability"]/'
                                       'div[@class="td-availability-interior"]/span/text()').extract()
        ingredients = site.xpath('//section[@class="ingredient-concerns-table-wrapper"]//table[@class='
                                 '"table-ingredient-concerns"]/tbody//tr/td[@class="td-ingredient"]/'
                                 'div[@class="td-ingredient-interior"]/a[@href]/text()').extract()
        ingredients_dict = {}
        for i in range(len(ingredient_scores)):
            ingredients_dict.update({ingredients[i]: {'Score': ingredient_scores[i],
                                                      'Data Availability': ingredient_avails[i]}})

        result.update({'Overall Concerns': concerns_dict, 'Other Concerns': other_concerns_dict,
                       'Ingredient': ingredients_dict})

        self.count += 1
        print(self.count, result)
        self.output.write(json.dumps(result) + '\n')
