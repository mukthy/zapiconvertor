import json
import subprocess
import sys


def payload_to_zyte():
    data = sys.argv[1]
    data = data.replace(',}', '}')
    data = data.replace(',]', ']')
    data = json.loads(data)

    # print(data)

    # with open("file.json", "r") as f:
    #     data = f.read()
    #     data = json.loads(data)
    #     print(data)

    url = data['url']
    if 'actions' in data:
        actions = data['actions']
    else:
        actions = []

    if 'httpResponseBody' in data and data['httpResponseBody'] == True:
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True
        javascript = False
        browserHtml = False
        screenshot = False
        actions = []
        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

    elif 'browserHtml' in data and data['browserHtml'] == True:
        httpResponseBody = False
        httpResponseHeaders = False
        browserHtml = True
        javascript = True
        screenshot = True
        if 'experimental' in data:
            experimental = data['experimental']
        else:
            experimental = {
                "responseCookies": False,
            }

    else:
        httpResponseBody = True
        httpResponseHeaders = True
        javascript = False
        browserHtml = False
        screenshot = False
        actions = []
        if 'experimental' in data:
            experimental = data['experimental']
        else:
            experimental = {
                "responseCookies": False,
            }

    formatter = {
        'url': url
    }

    meta = {"zyte_api": {"javascript": javascript, "screenshot": screenshot,
                         "browserHtml": browserHtml, "actions": actions,
                         "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                         "experimental": experimental}}

    custom_settings = {
        'DOWNLOAD_HANDLERS': {"http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
                              "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler"},
        'DOWNLOADER_MIDDLEWARES': {"scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000},
        'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'ZYTE_API_KEY': "YOUR_API_KEY"
    }

    data = """
import scrapy
class SampleQuotesSpider(scrapy.Spider):
    name = "sample_quotes"
        
    custom_settings = {custom_settings}
        
    def start_requests(self):
        yield scrapy.Request(url="{url}", meta={meta})
    
    def parse(self, response):
        print(response.text)
""".format(**formatter, meta=meta, custom_settings=custom_settings)

    return data


if __name__ == '__main__':
    code = payload_to_zyte()
    # print(code)
    print("Code Generated!")
    print("Writing to file...")
    subprocess.run(["scrapy", "startproject", "sample_scrapy_zapi_project"], stdout=subprocess.DEVNULL)  # create a new scrapy project.
    with open("sample_scrapy_zapi_project/sample_scrapy_zapi_project/spiders/sample_scrapy_zapi.py", "w") as f:  # write the code to a file.
        f.write(code)
    print("Writing Done!")
    subprocess.run(["black", "sample_scrapy_zapi_project/sample_scrapy_zapi_project/spiders/sample_scrapy_zapi.py"])  # format the code using black.
    print("Formatting Done!")
