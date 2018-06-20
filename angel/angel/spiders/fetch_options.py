BASE_URL = 'https://trade.angelbroking.com/'
USER_NAME = 'AGRA3303'
PAGES = ['page1.aspx', 'page2.aspx', 'page3.aspx', 'page4.aspx']

class OptionAGL(scrapy.Spider):
    name = "sharespider"
    start_urls = [BASE_URL + '/public/login.aspx']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@id="login"]',
            formdata={
                'UserName': USER_NAME,             
                'Password': PASSWORD,             
                'Action':'1',
            },
            callback=self.after_login)

    def after_login(self, response):
        base_url = BASE_URL + '/public/'
        for page in PAGES:
            yield Request(
                url=base_url + page + "?id=1",
                callback=self.action)

    def action(self, response):
        page = re.search('public/(.*)id=1', response.url)
        if page:
            page_name = page.group(1)
            title = response.xpath('//title/text()').extract_first('').strip()
            item = PageItem()
            item['pagename'] = page_name
            item['description'] = title
            yield item
