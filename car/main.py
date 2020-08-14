from scrapy import cmdline

# cmdline.execute('scrapy crawl brands -s JOBDIR=/workspace/car/data/car_brand'.split())
cmdline.execute('scrapy crawl car_config'.split())
