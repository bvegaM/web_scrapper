import argparse
import csv
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import news_page_objects as news
import re
from urllib.parse import urlparse


from common import config
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') # https://example.com/hello
is_root_path = re.compile(r'^/.+$') # /some-text

def _news_scrapper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    homepage = news.HomePage(news_site_uid,host)

    articles=[]
    for link in homepage.article_links:
        article = _fecth_article(news_site_uid,_convert_url_host(host),link)
        if article:
            logger.info('Article feteched!')
            articles.append(article)
        
    _save_articles(news_site_uid,articles)


def _save_articles(news_site_uid,articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(news_site_uid=news_site_uid,datetime=now)
    csv_headers = list(filter(lambda property: not property.startswith('_'),dir(articles[0])))

    with open(out_file_name,mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article,prop)) for prop in csv_headers]
            writer.writerow(row)

def _convert_url_host(host):
    host_parser = urlparse(host)
    if host_parser.path=='':
        return host
    else:
        return '{scheme}://{domain}'.format(scheme=host_parser.scheme,domain=host_parser.netloc)

def _fecth_article(news_site_uid,host,link):
    logger.info('Start fetching article at {}'.format(link))

    article = None

    try:
        print(_build_link(host,link))
        article = news.ArticlePage(news_site_uid,_build_link(host,link))
    except(HTTPError,MaxRetryError):
        logger.warning('Error while fetching the article',exc_info=False)
    
    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None
    
    return article

def _build_link(host,link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return '{host}/{uri}'.format(host=host,uri=link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    new_sites_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=new_sites_choices)
    
    args = parser.parse_args()
    _news_scrapper(args.news_site)