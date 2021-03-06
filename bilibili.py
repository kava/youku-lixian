#!/usr/bin/env python

__all__ = ['bilibili_download']

import re
from common import *
from iask import iask_download_by_id
from youku import youku_download_by_id
from tudou import tudou_download_by_id

def get_srt_xml(id):
	url = 'http://comment.bilibili.tv/dm,%s' % id
	return get_html(url).decode('utf-8')

def parse_srt_p(p):
	fields = p.split(',')
	assert len(fields) == 8, fields
	time, mode, font_size, font_color, pub_time, pool, user_id, history = fields
	time = float(time)

	mode = int(mode)
	assert 1 <= mode <= 8
	# mode 1~3: scrolling
	# mode 4: bottom
	# mode 5: top
	# mode 6: reverse?
	# mode 7: position
	# mode 8: advanced

	pool = int(pool)
	assert 0 <= pool <= 2
	# pool 0: normal
	# pool 1: srt
	# pool 2: special?
	
	font_size = int(font_size)

	font_color = '#%06x' % int(font_color)

	return pool, mode, font_size, font_color

def parse_srt_xml(xml):
	d = re.findall(r'<d p="([^"]+)">(.*)</d>', xml)
	for x, y in d:
		p = parse_srt_p(x)
	raise NotImplementedError()

def bilibili_download(url):
	assert re.match(r'http://www.bilibili.tv/video/av(\d+)', url)
	html = get_html(url)

	title = r1(r'<h2 id="titles">([^<>]+)<a name="titles">', html).decode('utf-8')
	title = unescape_html(title)
	title = escape_file_path(title)

	flashvars = r1(r'flashvars="([^"]+)"', html)
	assert flashvars
	t, id = flashvars.split('=', 1)
	if t == 'vid':
		iask_download_by_id(id, title)
	elif t == 'ykid':
		youku_download_by_id(id, title)
	elif t == 'uid':
		tudou_download_by_id(id, title)
	else:
		raise NotImplementedError(flashvars)

	xml = get_srt_xml(id)
	with open(title + '.xml', 'w') as x:
		x.write(xml.encode('utf-8'))

download = bilibili_download
download_playlist = playlist_not_supported('bilibili')

def main():
	script_main('bilibili', bilibili_download)

if __name__ == '__main__':
	main()

