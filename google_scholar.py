#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests


class ScholarInfo():

    def __init__(self, proxy=None):
        self.proxy = proxy

    def get_authors(self, soup):
        return soup.find('div', class_='gs_fmaa').text.split(',')

    def get_title(self, soup):
        return soup.find('h3', class_='gs_rt').text

    def get_citation(self, soup):
        cite = soup.find('a', text=lambda t: t and 'Cited by' in t)
        if cite is None:
            return -1, None
        base_url = "https://scholar.google.com"
        url = base_url + cite.get('href')
        num = int(cite.text.split()[-1])
        return num, url

    def get_pub(self, soup):
        data = soup.find('div', class_='gs_a gs_fma_p')
        input_text = str(data)
        div_index = input_text.find("</div>")
        span_index = input_text.find('<span class="gs_pdot">')

        # Extract the text between the two indices
        if div_index != -1 and span_index != -1:
            extracted_text = input_text[div_index + 6:span_index]
            return extracted_text.strip()
        else:
            print(f"Substring not found in input: {input_text}")
            return None

    def search_by_arxiv_id(self, arxiv_id):
        url = f"https://scholar.google.com/scholar_lookup?arxiv_id={arxiv_id}"
        data = requests.get(url, proxies=self.proxy)
        soup = BeautifulSoup(data.content, 'html.parser')
        authors = self.get_authors(soup)
        cite, cite_url = self.get_citation(soup)
        pub_info = self.get_pub(soup)
        if pub_info is None:
            pub, date = 'arXiv', arxiv_id
        else:
            pub, date = self.publication_mapping(pub_info)
        title = self.get_title(soup)
        return {"title": title, "authors": authors,
                "citation": cite, "citation_url": cite_url,
                "publication": pub, "publication_date": date}

    def publication_mapping(self, pub_info):
        pub, date = pub_info.split(',')
        pub = pub.lower()
        map_dict = {
            "International Conference on Machine Learning".lower(): "ICML",
            "Proceedings of the IEEE conference on computer vision and".lower(): "CVPR",
            "IEEE/CVF Conference on Computer Vision".lower(): "CVPR",
            # ICCV
            "Proceedings of the IEEE/CVF International Conference on".lower(): "ICCV",
            # ECCV
            "European Conference on Computer Vision".lower(): "ECCV",
            # NeurIPS
            "Neural Information Processing Systems".lower(): "NeurIPS",
            # ICLR
            "International Conference on Learning Representations".lower(): "ICLR",
            # IJCAI
            "International Joint Conference on Artificial Intelligence".lower(): "IJCAI",
            "arxiv".lower(): "arXiv",
            # AAAI
            "Proceedings of the AAAI Conference on Artificial Intelligence".lower(): "AAAI",
            # ACL
            "Proceedings of the Association for Computational Linguistics".lower(): "ACL",
            # EMNLP
            "Proceedings of the Conference on Empirical Methods in Natural".lower(): "EMNLP",
            # CoRL
            "Conference on Robot Learning".lower(): "CoRL",
        }
        for k, v in map_dict.items():
            if k in pub:
                return v, date.strip()
        print(f"Cannot find the publication for {pub_info}")
        return pub, date.strip()


if __name__ == '__main__':
    proxy = {
        'http': '127.0.0.1:7890',
        'https': '127.0.0.1:7890',
    }
    gscholar = ScholarInfo(proxy=proxy)
    arxiv_id = "2106.06103"
    res = gscholar.search_by_arxiv_id(arxiv_id)
    print(res)


# vim: ts=4 sw=4 sts=4 expandtab
