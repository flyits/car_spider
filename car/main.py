from scrapy import cmdline

print("hello,world!")
# cmdline.execute('scrapy crawl car_config -s JOBDIR=/workspace/car/data/car_config'.split())
cmdline.execute('scrapy crawl car_config '.split())
# cmdline.execute('scrapy crawl car_spider '.split())
# cmdline.execute('scrapy crawl car_images '.split())
