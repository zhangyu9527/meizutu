import requests
import os
from lxml import etree

def get_all_list_url(url):
    print('正在处理的最外层URL:',url)
    print("--"*30)
    responce=requests.get(url)
    html_ele=etree.HTML(responce.text)
    href_list=html_ele.xpath('//ul[@id="pins"]/li/a/@href')
    for href in href_list:
        get_detailed_page_url(href)
    next_page_ele=html_ele.xpath('//a[@class="next page-numbers"]/@href')
    if next_page_ele:
        get_all_list_url(next_page_ele[0])
def get_detailed_page_url(url):
    response=requests.get(url)
    html_ele=etree.HTML(response.text)
    page_num=html_ele.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    for i in range(int(page_num)):
        detailed_url=url+'/'+str(i+1)
        get_image_url(detailed_url)
def get_image_url(url):
    response=requests.get(url)
    html_ele=etree.HTML(response.text)
    src=html_ele.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    download_image(src,url)
def download_image(url,referer):
    print('正在下载...'+url)
    downloaddir='妹子图'
    print("1212")
    if not os.path.exists(downloaddir):
        os.mkdir(downloaddir)
        print("11111")
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Referer':referer,
    }
    response=requests.get(url,headers=headers)
    filename=downloaddir+'/'+url.split('/')[-1]
    with open(filename,'wb')as f:
        f.write(response.content)

if __name__ == '__main__':
    url='https://www.mzitu.com/'
    get_all_list_url(url)
