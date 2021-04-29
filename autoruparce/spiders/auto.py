import scrapy
import pymongo



class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']

    db_client = pymongo.MongoClient()
    db = db_client['db_lesson4_homework']
    collection = db['autoru']

    selector = {
        "brands":".TransportMainFilters_brandsList__2tIkv a.blackLink",
        "pagnin":".Paginator_block__2XAPy app_roundedBlockWithShadow__1rh6w a.Paginator_button__u1e7D",
        "car": "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_photoWrapper__3W9J4"
    }


    def _get_follow(self, response, selector, callback, **kwargs):
        for link in response.css(selector):
            yield response.follow(link.attrib.get("href"), callback=callback)


    def parse(self, response):
        yield from self._get_follow(response, self.selector["brands"], self.brand_parce)


    def brand_parce(self, response):
        yield from self._get_follow(response, self.selector["pagnin"], self.brand_parce)
        yield from self._get_follow(response, self.selector["car"], self.car_parce)

    def car_parce(self, response):
        data = {
            "url":response.url,
            "name": response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "jpg": [x.attrib.get("style").split("(")[1].split(")")[0] for x in response.css("section.PhotoGallery_thumbnails__3-1Ob button")],
            "characteristics":{x.css(".AdvertSpecs_label__2JHnS::text").extract_first():x.css(".blackLink::text").extract_first() if x.css(".blackLink::text").extract_first() is not None else x.css(".AdvertSpecs_data__xK2Qx::text").extract_first() for x in response.css("div.AdvertSpecs_row__ljPcX")},
            "description":response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first()
             }
        self.collection.insert_one(data)







