
import csv
import os
import requests
import re

from bs4 import BeautifulSoup

# main url for sec page 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-Q&dateb=&owner=exclude&count=100'
tsla_quarterly_reports = ['https://www.sec.gov/Archives/edgar/data/1318605/000156459019026445/tsla-10q_20190630.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459019013462/tsla-10q_20190331.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459018026353/tsla-10q_20180930.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459018011086/tsla-10q_20180331.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459017021343/tsla-10q_20170930.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459017015705/tsla-10q_20170630.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459017009968/tsla-10q_20170331.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459016026820/tsla-10q_20160930.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459016023024/tsla-10q_20160630.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459016018886/tsla-10q_20160331.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459015009741/tsla-10q_20150930.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459015006666/tsla-10q_20150630.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000156459015003789/tsla-10q_20150331.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312514403635/d812482d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312514303175/d766922d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312514192606/d715897d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312513435480/d588506d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312513327916/d549636d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312513212354/d511008d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312512457610/d410318d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312512332138/d364775d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312512225825/d325967d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312511308489/d226201d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312511221497/d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312511139677/d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312510259068/d10q.htm',
           'https://www.sec.gov/Archives/edgar/data/1318605/000119312510188792/d10q.htm']

class WebScraper:
    def extract_date_from_article(self, words):
        return words.split('ended ')[1]

    def clean_article(self, article):
        article = " ".join(article.split())  # Remove extra white spaces


    def find_article_content(self, soup):
        """Finds Article by looking for P tags in HTML"""
        date = None
        tag = soup.find_all('p')
        article = ''
        for i in tag:
            if 'for the quarterly period ended' in i.get_text().lower():
                date = self.extract_date_from_article(i.get_text().lower())
            article += (i.get_text())
        article = self.clean_article(article)
        return date, [article]

    def scrape_article_from_web(self, article_URL):
        """Given a url, it calls out to other functions to extract article info
           and returns the info """
        try:
            page = requests.get(article_URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            date, article_content = self.find_article_content(soup)
            print(date)
            print(article_content)
            # article_extracted_info = {'URL': str(article_URL),
            #                           'Title': title,
            #                           'Author': author,
            #                           'Date_Published': date_published,
            #                           'Time_Published': time_published,
            #                           'Article': article_content}
            #return (article_extracted_info)
        except Exception as e:
            print(e)

    def find_articles_from_search_URL(self, search_URLs):
        """Given a search URL, it finds all the article URLs and sends them to get extracted"""
        allArticles = {}

        path = (f'{os.getcwd()}/QuarterlyReports/')
        fileName = path + 'TSLA_Quarterly_Reports.csv'

        if not os.path.exists(path):  # Create path if it doesnt exist
            os.makedirs(path)

        for URL in search_URLs:
            try:
                articleInfo = self.scrape_article_from_web(URL)
                #  self.write_dict_to_csv(allArticles, fileName)
            except Exception as e:
                self.write_dict_to_csv(allArticles, fileName)
                print(f'Error loading info from page {URL}:', e)
            print('Finished Creating', fileName, 'for page', URL, '\n')

    def write_dict_to_csv(self, articleInfo, fileName):
        with open(fileName, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('URL', 'Title', 'Author',
                             'Date_Published', 'Time_Published',
                             'Article'))
            for key, value in articleInfo.items():
                writer.writerow([key, value['Title'], value['Author'],
                                 value['Date_Published'], value['Time_Published'],
                                 value['Article']])


def run_webscraper_program():
    print('Starting Web Scraper')
    #search_url = "https://www.ibtimes.com/search/site/tsla"
    #search_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-Q&dateb=&owner=exclude&count=100'
    scraper = WebScraper()
    scraper.find_articles_from_search_URL(tsla_quarterly_reports)
    print('Finished Web Scraper')

run_webscraper_program()