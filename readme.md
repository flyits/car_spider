
源码仅限于技术研究与学习。

### 环境配置
windows 下启动Docker-Desktop后，进入爬虫根目录,运行命令
         
    docker-compose up -d
    docker ps -a

看到服务启动即可
![Image discription](https://raw.githubusercontent.com/Flyits/car_spider/master/docker_container.jpg)

### 爬虫运行
1. docker环境启动之后，在Pycharm中配置python解释器（docker-compose),运行car/main.py
2. `docker exec -ti car_spider bash`进入爬虫容器,
   `cd /workspace` 后运行 `scrapy crawl car_config`
### 注
`setting.py 中 `以实际机子性能动态调控，这里我500是刚刚好跑满CPU

    # Configure maximum concurrent requests performed by Scrapy (default: 16)
    CONCURRENT_REQUESTS = 500