from scrapy import cmdline

# cmdline.execute('scrapy crawl car_config -s JOBDIR=/workspace/car/data/car_config'.split())
cmdline.execute('scrapy crawl car_config '.split())
# cmdline.execute('scrapy crawl car_spider '.split())
