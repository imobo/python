import requests
from requests.exceptions import RequestException
import re
from lxml import etree
import chardet
import csv
import urllib.parse

def job51StrDecode(query):
    s = urllib.parse.quote_plus(query)
    temp = None
    for i in range(len(s), 0, -1):
        if s[i-1] == "%":
            s = s[:i] + "25" + s[i:]
    return s


def get_html(url):
    try:
        proxies = {
            'http': '',
            'https': '',}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        response = requests.get(url, headers=headers,proxies=proxies)
        if response.status_code == 200:
            response.encoding = chardet.detect(response.content).get('encoding')
            html = response.text
            return html
    except RequestException:
        print(response)
        return None


def main():
    keyword = "工程师"
    s = job51StrDecode(keyword)

    items = []
    for page in range(1, 31):
        url = "https://search.51job.com/list/000000,000000,0000,32,9,99,{0},2,{1}.html".format(s, page)
        print(url)
        print("正在爬取第{}页".format(page))
        html = get_html(url)
        url_lists = re.findall('<script type="text/javascript">.*?engine_search_result":(.*),.*?"jobid_count"', html, re.S)
        url_lists = url_lists[0]
        url_lists = eval(url_lists)
        for url in url_lists:
            url = url.get('job_href')
            url = re.sub(r'\\', '', url)            # 岗位信息的详细页面
            html = get_html(url)
            item = parse_html(html)
            items.append(item)
    # 保存到csv中
    save_csv(items)

def parse_html(html):
    try:
        # 返回xpath对象
        html_xpath = etree.HTML(html)
        # 职位名称
        job_title = html_xpath.xpath("//div[contains(@class, 'tHeader')]/div[@class='in']/div[@class='cn']/h1/text()")
        job_title = job_title[0]
        print("job_title:{}".format(job_title))
        # 公司名称
        company_name = html_xpath.xpath("//div[contains(@class, 'tHeader')]/div[@class='in']/div[@class='cn']/p[@class='cname']/a/@title")
        company_name = company_name[0]
        print("company_name:{}".format(company_name))
        # 工作地点
        info = html_xpath.xpath("//div[contains(@class, 'tHeader')]/div[@class='in']/div[@class='cn']/p[contains(@class, 'msg')]/@title")
        info = re.sub('[(xa0)(|)]', '', info[0])
        info = info.split()
        work_place = info[0]
        print("work_place:{}".format(work_place))
        # 工作经验
        work_year = info[1]
        print("work_year:{}".format(work_year))
        # 学历
        education = info[2]
        print("education:{}".format(education))
        # 招聘人数
        recruit_number = info[3]
        print("recruit_number:{}".format(recruit_number))
        # 发布时间
        release_time = info[4]
        print("release_time:{}".format(release_time))
        # 公司性质
        company_nature = html_xpath.xpath("//div[@class='tCompany_sidebar']//div[@class='com_tag']/p[1]/@title")
        company_nature = company_nature[0]
        print("company_nature:{}".format(company_nature))
        # 公司规模
        company_size = html_xpath.xpath("//div[@class='tCompany_sidebar']//div[@class='com_tag']/p[2]/@title")
        company_size = company_size[0]
        print("company_size:{}".format(company_size))
        # 所属行业
        industry = html_xpath.xpath("//div[@class='tCompany_sidebar']//div[@class='com_tag']/p[3]/@title")
        industry = industry[0]
        print("industry:{}".format(industry))
        # 工资
        salary = html_xpath.xpath("//div[contains(@class, 'tHeader')]/div[@class='in']/div[@class='cn']/strong/text()")
        salary = salary[0]
        print("salary:{}".format(salary))
        # 公司介绍
        company_Inform= html_xpath.xpath("//div[contains(@class, 'tBorderTop_box')]/div[@class='tmsg inbox']/text()")
        #print(company_Inform)
        
        item = [job_title, company_name, work_place, work_year, education, recruit_number, release_time,
                company_nature, company_size, industry, salary, company_Inform]
        return item
    except:
        pass


def save_csv(items):
    with open("jobInformation.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csv_tags = ['职位名称', '公司名称', '工作地点', '工作经验', '学历', '招聘人数', '发布时间', '公司性质', '公司规模',
                      '所属行业', '工资', "公司介绍"]
        writer = csv.writer(csvfile)
        writer.writerow(csv_tags)
        for item in items:
            if item != None:
                writer.writerow(item)


if __name__ == '__main__':
    main()
