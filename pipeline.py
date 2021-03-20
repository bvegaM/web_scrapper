import logging
logging.basicConfig(level=logging.INFO)
import subprocess

logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal','platzi']

def main():
    _extract()
    _transform()

def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python','extract.py',news_site_uid], cwd='extract/')
        subprocess.run(['find','.','-name','{}*'.format(news_site_uid),'-exec','mv','{}','../transform/{}_.csv'.format(news_site_uid),';'],cwd='extract/')

def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = '{}_.csv'.format(news_site_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python','transform.py',dirty_data_filename],cwd='transform/')
        subprocess.run(['rm',dirty_data_filename],cwd='transform/')

if __name__ =='__main__':
    main()