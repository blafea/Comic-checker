import requests
from lxml import etree


def check(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    # print(res.text)
    html_find = html.xpath(
        "/html/body/div[@id='__nuxt']/div[@id='__layout']/div[@id='layout']/div[@class='comics-detail']/div[@class='de-info-wr']/div[@class='l-content']/div[@class='pure-g de-info__box']/div[@class='pure-u-1-1 pure-u-sm-2-3 pure-u-md-3-4']/div[@class='comics-detail__info']/div[@class='supporting-text mt-2']"
    )[0]
    aaa = etree.tostring(html_find, encoding='utf-8').decode('utf-8')
    return ("小時" in aaa) or ("今天" in aaa) or ("分鐘" in aaa)
