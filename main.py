from comcrawl import IndexClient
from time import time
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from tqdm import tqdm


class Crawl():

    def __init__(self, sources, indecies, keywords):
        self.keywords = keywords
        self.indecies = indecies
        self.sources = sources
        self.urls_file_path = "urls.txt"
        self.urls = []
        self.results = []
        self.client = None


    def download_client(self, index):
        print('--------------------- Download Initiated ---------------------')
        client = IndexClient([index], verbose=False)
        self.client = client


    def search(self, search):
        self.client.search(search, threads=14)
        self.client.download(threads=14)
        self.results = self.client.results
        print('--------------------- Download Completed ---------------------')


    def relevance_checker(self, text):
        relevance_index = 0
        dictionary = set(text.split(" "))
        length = len(dictionary)

        for keyword in self.keywords:
            if keyword in dictionary:
                relevance_index += 1
                # arbitrary cutoff 
                if relevance_index >= 4:
                    print('relevance_index:' + str(relevance_index))
                    return True

        print('relevance_index:' + str(relevance_index))
        return False


    def iterate(self):
        for i in range(len(self.indecies)):
            for j in range(len(self.sources)):
                self.download_client(self.indecies[i])
                self.search(self.sources[j])
                print(len(self.results))
                for record in tqdm(self.results):
                    print(record)
                    if record['status'] != "200":
                        continue

                    url, doc = self.read_doc(record, self.get_text_selectolax)
                    if not doc or not url:
                        continue

                    if self.relevance_checker(doc):
                        self.urls.append(url)

        self.write_urls()


    def write_urls(self):
        file1 = open("urls.txt","a")
        for url in self.urls:
            file1.write(url + "\n")

        file1.close()


    # from rushter.com/blog
    def get_text_selectolax(self, html):
        tree = HTMLParser(html)

        if tree.body is None:
            return None

        for tag in tree.css('script'):
            tag.decompose()
        for tag in tree.css('style'):
            tag.decompose()

        text = tree.body.text(separator='\n')
        return text


    # from rushter.com/blog
    def read_doc(self, record, parser=get_text_selectolax):
        url = record["url"]
        text = None

        if url:
            payload = record['html']
            html = payload.split('\r\n\r\n', maxsplit=1)[0]
            html = html.strip()

            if len(html) > 0:
                text = parser(html)

        return url, text



indecies = ['2020-05', '2020-10', '2020-16', '2020-24', '2020-29', '2020-34',
            '2020-40', '2020-45', '2020-50']

f = open("keywords.txt", "r")
keywords = [word[:-1] for word in f]
f.close()

f = open("sources.txt", "r")
sources = [source[:-1] for source in f]
f.close()


x = Crawl(sources, indecies, keywords)
x.iterate()
