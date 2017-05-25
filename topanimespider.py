import scrapy

class AnimeItem(scrapy.Item):
    title = scrapy.Field()
    pagetype = scrapy.Field()
    link = scrapy.Field()
    rank = scrapy.Field()
    episodes = scrapy.Field()
    members = scrapy.Field()
    score = scrapy.Field()


class AnimePage(scrapy.Item):
    title = scrapy.Field()
    pagetype = scrapy.Field()
    status = scrapy.Field()
    streamtype = scrapy.Field()
    aired = scrapy.Field()
    producers = scrapy.Field()
    studios = scrapy.Field()
    genres = scrapy.Field()
    episodes = scrapy.Field()
    score = scrapy.Field()
    recommendationlink = scrapy.Field()
    statslink =scrapy.Field()

class AnimeRecommendations(scrapy.Item):
    title = scrapy.Field()
    pagetype = scrapy.Field()
    recommendations = scrapy.Field()

class AnimeStats(scrapy.Item):
    title = scrapy.Field()
    pagetype = scrapy.Field()
    score1 = scrapy.Field()
    score2 = scrapy.Field()
    score3 = scrapy.Field()
    score4 = scrapy.Field()
    score5 = scrapy.Field()
    score6 = scrapy.Field()
    score7 = scrapy.Field()
    score8 = scrapy.Field()
    score9 = scrapy.Field()
    score10 = scrapy.Field()

class AnimeSpider(scrapy.Spider):
    name = "topanimespider"
    pagecount = 0
    pagelimt = 2000

    download_delay = 0.25

    start_urls = [
        "https://myanimelist.net/topanime.php?type=tv&limit=0"
    ]

    #Parses Pages of top anime list
    def parse(self, response):
        self.pagecount+=1
        animeentry = response.xpath("//tr[@class='ranking-list']")
        for a in animeentry:
            item =  AnimeItem()
            item['pagetype'] = 'ListEntry'
            atitlecell =  a.xpath("td[@class='title al va-t word-break']")
            item['rank'] =  a.xpath("td[@class='rank ac']/span/text()").extract()[0]
            item['score'] =  a.xpath("td[@class='score ac fs14']/div/span/text()").extract()[0]
            item['title'] = atitlecell.xpath("div/div[@class='di-ib clearfix']/a")[0].xpath("text()").extract()[0]
            item['link'] = atitlecell.xpath("div/div[@class='di-ib clearfix']/a")[0].xpath("@href").extract()[0]
            item['episodes'] = atitlecell.xpath("div/div[@class = 'information di-ib mt4']/text()").extract()[0].strip('\n').strip()
            #item.years = atitlecell.xpath("div/div[@class = 'information di-ib mt4']/text()").extract()[1]
            item['members'] = atitlecell.xpath("div/div[@class = 'information di-ib mt4']/text()").extract()[2].strip('\n').strip()
            yield item
            if(item['link']):
                yield scrapy.Request(item['link'], callback = self.parseAnimePage)

        #Next Page Link
        next50 = response.xpath("//a[text()='Next 50'][1]")
        if next50 and (self.pagecount<self.pagelimt):
            next50link = "https://myanimelist.net/topanime.php" + next50.xpath('@href').extract()[0]
            yield scrapy.Request(next50link, callback = self.parse)


    def parseAnimePage(self, response):
        pagedata =  response.css('.js-scrollfix-bottom').xpath('div')
        item = AnimePage()
        item['pagetype'] = 'PageEntry'
        item['title'] = response.xpath("//span[@itemprop='name']/text()").extract()[0]
        item['streamtype'] = pagedata.re(r'Type:\s*</span>\s*(.*)')[0]
        item['status'] = pagedata.re(r'Status:\s*</span>\s*(.*)')[0]
        item['aired'] =  pagedata.re(r'Aired:\s*</span>\s*(.*)')[0]
        item['producers'] = pagedata.re(r'Producers:\s*</span>\s*(.*)')[0]
        item['studios'] = pagedata.re(r'Studios:\s*</span>\s*(.*)')[0]
        item['genres'] = pagedata.re(r'Genres:\s*</span>\s*(.*)')[0]
        item['episodes'] = pagedata.re(r'Episodes:\s*</span>\s*(.*)')[0]
        item['score'] = pagedata.re(r'Score:\s*</span>\s*(.*)')[0]
        linkdata = response.css('#horiznav_nav').xpath("ul/li")
        item['recommendationlink'] = linkdata.re(r'href="(.*)".*Recommendations')[0]
        item['statslink'] = linkdata.re(r'href="(.*)".*Stats')[0]
        yield item
        yield scrapy.Request(item['statslink'], callback = self.parseAnimeStats)
        yield scrapy.Request(item['recommendationlink'], callback = self.parseAnimeRecommendations)

    def parseAnimeStats(self, response):
        item = AnimeStats()
        item['pagetype'] = 'StatsEntry'
        item['title'] = response.xpath("//span[@itemprop='name']/text()").extract()[0]
        scoretable = response.xpath("//h2[.='Score Stats']/following::table[1]")
        for i in range(1,11):
            if(scoretable.xpath("tr/td[.='"+str(i)+"']/following::td[1]/div/span/small").re('\((.*) votes')):
                item['score'+str(i)] = scoretable.xpath("tr/td[.='"+str(i)+"']/following::td[1]/div/span/small").re('\((.*) votes')[0]
            else:
                item['score'+str(i)] = "0"
        yield item

    def parseAnimeRecommendations(self, response):
        item = AnimeRecommendations()
        item['pagetype'] = 'RecommendationEntry'
        item['title'] = response.xpath("//span[@itemprop='name']/text()").extract()[0]
        item['recommendations'] = {} 
        recommendationlist = response.css(".js-scrollfix-bottom-rel").xpath("div[@class='borderClass']/table/tr")
        for recommendation in recommendationlist:
            recTitle = recommendation.xpath("td/div[@style='margin-bottom: 2px;']/a[1]//text()").extract()[0]
            if(recommendation.css(".spaceit").re(r"by <strong>(.*)</strong> more")):
                recscore = recommendation.css(".spaceit").re(r"by <strong>(.*)</strong> more")[0]
            else:
                recscore = '0'
            item["recommendations"][recTitle] = recscore
        yield item

