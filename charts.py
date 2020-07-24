''' Download all "Essential Charts" from the /mu/ wiki '''

import re
import bs4
import requests

def main():
    ''' Driver function '''
    page = requests.get("https://4chanmusic.fandom.com/wiki/Essential_Charts")
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    gallery = soup.find('div', id='gallery-0')
    images = gallery.find_all('img', class_='lzy')
    captions = gallery.find_all('div', class_='lightbox-caption')
    root = '/home/david/Pictures/Music/'
    for image, caption in zip(images, captions):
        end = image['data-src'].index('/revision')
        file_end = image['data-src'][end-4:end]
        if file_end == 'jpeg':
            file_end = '.jpg'
        caption = '_'.join(re.findall(r'[a-zA-Z0-9]+', caption.text))
        download_img(root + caption + file_end, image['data-src'][:end])

def download_img(file_name, url):
    ''' Download the image located at 'url' and save as 'file_name' '''
    with open(file_name, 'wb') as f:
        f.write(requests.get(url).content)

if __name__ == '__main__':
    main()
