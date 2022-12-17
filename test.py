import os
import sys
import logging

from flask import send_file
from pysitemap import crawler
print('start')
# if __name__ == '__main__':
# if '--iocp' in sys.argv:
from asyncio import events, windows_events
# sys.argv.remove('--iocp')
# logging.info('using iocp')
el = windows_events.ProactorEventLoop()
events.set_event_loop(el)
# else:
#     print('End')

# root_url = sys.argv[1]
root_url = 'http://complexprogrammer.uz'
crawler(root_url, out_file='sitemap.xml', exclude_urls=[".ico", ".css", ".pdf", ".jpg", ".zip", ".png", ".svg"])
print('End')
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
print(os.path.join(basedir, 'sitemap.xml'))
send_file(os.path.join(basedir, 'sitemap.xml'), as_attachment=True)