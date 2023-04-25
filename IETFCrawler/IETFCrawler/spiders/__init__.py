# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

class IETFSpider(scrapy.Spider):
    name = 'IETF'
    
    allowed_domains = ['mailarchive.ietf.org']
    start_urls = ['https://mailarchive.ietf.org/arch/browse/']

    # LEVEL1 | all activities

    def parse(self, response):
        # find every <a><a/> elements in 'https://mailarchive.ietf.org/arch/browse/'
        ietf_activities = response.xpath("//ul[@class='browse-list']/li")
        for activities in ietf_activities:

            root_name = activities.xpath('.//a/text()').get()
            # activity_url: all the root mail url w.r.t. the activitiy name
            root_url = activities.xpath('.//a/@href').get()
            
            yield response.follow(root_url, callback=self.parse_allmailurl,
                                    meta= {'root_name': root_name,
                                            'root_url': root_url})

    # LEVEL2 | all mails w.r.t. the activities

    def parse_allmailurl(self, response):
        
        # using meta to pass extra arguments to call back function in parse (activity, root_url)
        root_name = response.meta['root_name']
        root_url = response.meta['root_url']
        
        # find every  <a><a/> elements in level2
        ietf_mails = response.xpath("//div[@class='xtr']")
        for mail in ietf_mails:
            mail_url = mail.xpath('.//a/@href').get()

            yield response.follow(mail_url,
                                    callback=self.parse_detailpage,
                                    meta= {'root_name': root_name,
                                            'root_url': root_url})

        next_page = response.xpath("//a[@class='msg-detail']/following-sibling::a[1]/@href").get()
        if next_page is not None:

            # This is the fixed line:

            yield response.follow(next_page, callback=self.parse_allmailurl,
                                    meta= {'root_name': root_name,
                                            'root_url': root_url})


    # LEVEL3 | mail_content

    def parse_detailpage(self, response):
        
        root_name = response.meta['root_name']
        root_url = response.meta['root_url']
            
        details = response.xpath("//div[@id='msg-body']")
        for detail in details:

            mail_content = detail.xpath('.//pre/text()').get()
    
            print(mail_content)

            yield  {'root_name': root_name,
                    'root_url': root_url,
                    'mail_content:': mail_content}