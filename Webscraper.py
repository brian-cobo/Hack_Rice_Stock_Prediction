
import csv
import os
import requests
import re

from bs4 import BeautifulSoup


class WebScraper:
    def find_title_from_article(self, soup):
        """Finds Title tag from HTML"""
        return soup.find_all('title')[0].get_text()

    def find_author_from_article(self, soup):
        """Finds Span tag, and name property from HTML"""
        return soup.find_all('span', itemprop='name')[0].get_text()

    def find_publish_date_and_time_from_article(self, soup):
        """Finds Time tag and date published property from
            HTML and separates the date and time"""
        time = soup.find_all('time', itemprop='datePublished')
        published_time = ''
        for i in time:
            published_time += i.get_text()
        published_time = published_time.split()
        date_published = published_time[0]
        time_published = (' ').join(published_time[2:4])
        return (date_published, time_published)

    def find_article_content(self, soup):
        """Finds Article by looking for P tags in HTML"""
        tag = soup.find_all('p')
        article = ''
        for i in tag:
            article += (i.get_text())
        return [article]

    def scrape_article_from_web(self, article_URL):
        """Given a url, it calls out to other functions to extract article info
           and returns the info """
        try:
            page = requests.get(article_URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = self.find_title_from_article(soup)
            author = self.find_author_from_article(soup)
            date_published, time_published = self.find_publish_date_and_time_from_article(soup)
            article_content = self.find_article_content(soup)

            article_extracted_info = {'URL': str(article_URL),
                                      'Title': title,
                                      'Author': author,
                                      'Date_Published': date_published,
                                      'Time_Published': time_published,
                                      'Article': article_content}
            return (article_extracted_info)
        except Exception as e:
            print(e)

    def find_articles_from_search_URL(self, search_URL, numPages=1):
        """Given a search URL, it finds all the article URLs and sends them to get extracted"""
        allArticles = {}

        path = (f'{os.getcwd()}/Articles/')
        fileName = path + 'Article_Info.csv'

        if not os.path.exists(path):  # Create path if it doesnt exist
            os.makedirs(path)

        for i in range(1, numPages+1):
            try:
                if numPages > 1:
                    URL = search_URL + f'?page={i}'
                else:
                    URL = search_URL
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, 'html.parser')
                links = soup.findAll('a', attrs={'href': re.compile("^https://")})
                for link in links:
                    newLink = link.get('href')
                    if ('twitter.com' not in newLink and
                            'facebook.com' not in newLink and
                            'linkedin.com' not in newLink and
                            'ibtimes.tumblr.com' not in newLink):
                        print('Analyzing link:', newLink)
                        articleInfo = self.scrape_article_from_web(newLink)
                        if articleInfo:  # Ensure article info exists
                            if articleInfo['URL'] not in allArticles:  # Check if article has been saved already
                                allArticles[articleInfo['URL']] = {'Title': articleInfo['Title'],
                                                                   'Author': articleInfo['Author'],
                                                                   'Date_Published': articleInfo['Date_Published'],
                                                                   'Time_Published': articleInfo['Time_Published'],
                                                                   'Article': articleInfo['Article']}
                            self.write_dict_to_csv(allArticles, fileName)
            except Exception as e:
                self.write_dict_to_csv(allArticles, fileName)
                print(f'Error loading info from page {i}:', e)
            print('Finished Creating', fileName, 'for page', i, '\n')

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


if __name__ == "__main__":
    print('Starting Web Scraper')
    search_url = "https://www.ibtimes.com/search/site/tsla"
    scraper = WebScraper()
    scraper.find_articles_from_search_URL(search_url, numPages=2)
    print('Finished Web Scraper')
