import requests
from bs4 import BeautifulSoup

url_links = {'a': [], 'link': [], 'img': [], 'script': []}


def get_a_tag(soup, url):
    try:
        for tag in soup.find_all('a'):
            if tag.attrs['href'] is not None:
                link = tag.attrs['href']
                #print("a tag: ", link)

                pure_link = link.strip()
                if pure_link and (not 'javascript' in pure_link) and (pure_link[0] != '#'):
                    if (not "http" in pure_link) and (pure_link[0] == "/"):
                        pure_link = url + pure_link

                    url_links['a'].append(pure_link)

    except Exception as e:
        print(e)


def get_link_tag(soup):
    try:
        for tag in soup.find_all('link'):
            if tag.attrs['href'] is not None:
                link = tag.attrs['href']
                print("link: ", link)

                pure_link = link.strip()
                if pure_link and (not 'javascript' in pure_link) and (pure_link[0] != '#'):
                    if (pure_link[0:3] != "http") and (pure_link[0] == "/"):
                        pure_link = url + pure_link

                    url_links['link'].append(pure_link)

    except Exception as e:
        print(e)


def get_img_tag(soup):
    try:
        for tag in soup.find_all('img'):
            if tag.attrs['src'] is not None:
                link = tag.attrs['src']
                print("img link: ", link)

                pure_link = link.strip()
                if pure_link and (not 'javascript;' in pure_link) and (pure_link[0] != '#'):
                    if (pure_link[0:3] != "http") and (pure_link[0] == "/"):
                        pure_link = url + pure_link

                    url_links['img'].append(pure_link)

    except Exception as e:
        print(e)


def get_script_tag(soup):
    try:
        for tag in soup.find_all('script'):
            if tag.attrs['src'] is not None:
                link = tag.attrs['src']
                print("script link: ", link)

                pure_link = link.strip()
                if pure_link and (not 'javascript;' in pure_link) and (pure_link[0] != '#'):
                    if (pure_link[0:3] != "http") and (pure_link[0] == "/"):
                        pure_link = url + pure_link

                    url_links['script'].append(pure_link)

    except Exception as e:
        print(e)


def pattern_maker():
    with open('test_pattern.txt', 'r') as f:
        buff = f.readlines()

    return buff


def scan():
    scan_url = []
    scan_param = {}

    for link in url_links['a']:
        scan_page = []
        param_list = []

        if "?" in link:
            scan_page = link.split('?')

            print(scan_page[0])

            if scan_page[1] is not None:
                params = scan_page[1].split('&')

                for param in params:
                    print(param)
                    new_param = param.split('=')
                    param_name = new_param[0]
                    param_value = new_param[1]
                    #param_type = type(param_value)
                    param_list.append({param_name: param_value})

                scan_param[scan_page[0]] = param_list

    # for scan_page in scan_param:
    #     print(scan_page)
    #     print(scan_param[scan_page])
    # print(scan_param)

    # xss patterns
    xss_patterns = []
    xss_patterns = pattern_maker()
    #print("xss patterns : ", xss_patterns)

    # URL 복원
    for scan_page in scan_param:
        for pattern in xss_patterns:
            first = True
            new_url = scan_page + "?"
            for param in scan_param[scan_page]:
                for key in param:
                    # param[key] <- 스캔 패턴 넣기 & 변경하기
                    if first:
                        #params = key + '=' + param[key]
                        params = key + '=' + pattern.rstrip('\n')
                        new_url += params
                        first = False
                    else:
                        #params = key + '=' + param[key]
                        params = key + '=' + pattern.rstrip('\n')
                        new_url += "&" + params

                    # print(params)

            scan_url.append(new_url)
            print(new_url)

    #print("scan url : ", scan_url)

    # res = requests.get(new_url)

    # if res.status_code == 200:
    #     print("success")
    #     html = res.text
    #     print(html)


if __name__ == '__main__':

    url = 'http://demo.testfire.net'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        get_a_tag(soup, url)
        get_link_tag(soup)
        get_img_tag(soup)
        get_script_tag(soup)

        # Deduplication
        url_links['a'] = list(set(url_links['a']))
        # url_links['link'] = list(set(url_links['link']))
        # url_links['img'] = list(set(url_links['img']))
        # url_links['script'] = list(set(url_links['script']))

        print("a tag", url_links['a'])
        # print("link tag", url_links['link'])
        # print("img tag", url_links['img'])
        # print("script tag", url_links['script'])

        scan()
