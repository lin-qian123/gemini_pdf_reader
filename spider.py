import os
import requests
from bs4 import BeautifulSoup

def get_paper_links(category):
    url = f"https://arxiv.org/list/{category}/new"
    response = requests.get(url)
    print(f"Status code: {response.status_code}")  # 打印出请求的状态码
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and '/abs/' in href:
            arxiv_id = href.split('/abs/')[1]
            links = links + [f"https://arxiv.org/pdf/{arxiv_id}.pdf"]
    # with open(f'{category}/links.txt', 'w') as f:
    #     f.write('\n'.join(links))
    return links

def download_papers(links, category):
    if not os.path.exists(f'pdf/{category}'):
        os.makedirs(f'pdf/{category}')
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:  # 检查请求是否成功
            filename = os.path.join('pdf', category, link.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {link}")  # 打印出下载失败的链接

def up_to_baiduPCS(links, category):
    if not os.path.exists(category):
        os.makedirs(category)
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:  # 检查请求是否成功
            filename = os.path.join(category, link.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {link}")  # 打印出下载失败的链接
        os.system(f'BaiduPCS-Py upload {filename} /home/arxiv/{category}')
        os.system(f'rm {filename}')

def main():
    category = 'astro-ph'
    links = get_paper_links(category)
    download_papers(links, category)
    # up_to_baiduPCS(links, category)

if __name__ == "__main__":
    main()