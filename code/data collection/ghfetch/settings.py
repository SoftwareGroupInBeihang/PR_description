# Scrapy settings for ghfetch project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ghfetch'

SPIDER_MODULES = ['ghfetch.spiders']
NEWSPIDER_MODULE = 'ghfetch.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 12

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ghfetch.middlewares.AccessTokenDownloaderMiddleware': 555,  # 在内置的重试中间件（优先级550）之前处理响应
}

RETRY_TIMES = 10

REFERER_ENABLED = False
