# -*- coding: utf-8 -*-

# Scrapy settings for Tieba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Tieba'

SPIDER_MODULES = ['Tieba.spiders']
NEWSPIDER_MODULE = 'Tieba.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Tieba (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept-Encoding': 'gzip,deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Cookie':'BIDUPSID=B15B92C2992C2D50205C82D818C8F67A; BAIDUID=0243AB90E89A7CE7394DE49DC59DD2AA:FG=1; PSTM=1602212284; TIEBA_USERTYPE=a909e9f7c999cc6478fc4db3; bdshare_firstime=1602215612027; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; TIEBAUID=cb23caae14130a0d384a57f1; delPer=0; PSINO=6; H_PS_PSSID=7509_32617_1436_32788_7544_31660_32723_32231_7516_32117_32719; wise_device=0; st_key_id=17; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1602728142,1602728621,1602733521,1602733540; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1602745902; st_data=9270c89938ae16a64df0b7ef1ea448cefdd99ca0784e0a66b4ab2d2b2129c6f2b291a8fc591388c8af7ce6a678157bc1e67d70bde64a65976b758ea4e44972699b225a519fb9dd24db0c0981b5c7399a0905e645e3efd0dbd06c2b3f9d8dcbfc35028e3e087f45d9f7499ff3fc26f2e33ba33ba5e10848a33421bb1456054394; st_sign=94610b55; tb_as_data=c431fee611714ee0db71a98541d87d17f33c5ca80703005dc0e763e655185ad6ec81fa35f1f66f8ce662961909eaf5e21f6b89979a44d430ae34c656d82bd9033237d593372b4370b86a9d9e5b99d9212bd72b351c2e180a87489a5766acf955'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Tieba.middlewares.TiebaSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Tieba.middlewares.TiebaDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Tieba.pipelines.TiebaPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
