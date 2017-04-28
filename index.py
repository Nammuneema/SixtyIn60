from bs4 import BeautifulSoup
import html.parser
import selector as sl
import dbHelper as db
import helper
import summary

def getArticle(url):

    selectors = sl.getSelectors()
    domain = helper.getDomain(url)

    article = {
        'id':helper.hashId(url),
        'title':'',
        'body':'',
        'image':'',
        'source':'',
        'link':url,
        'date':'',
        'category':''
    }

    if domain in selectors.keys():
        the_page = helper.getHTML(url)
        soup = BeautifulSoup(the_page, "html.parser")

        # get the selector for this perticular site.
        selector = selectors[domain]
        items = soup.select(selector)

        # extract image from meta
        article['image'] = soup.find("meta", property="og:image")['content']
        text = ""

        for item in items:
            text = text + item.text

        article['body'] = helper.cleanText(text)

    else:
        print('no selector for this site: '+url)

    return article

def getNews():

    url = "https://news.google.com/news?cf=all&hl=en&pz=1&ned=in&output=rss"
    the_page = helper.getHTML(url)

    soup = BeautifulSoup(the_page, "html.parser")
    items = soup.find_all('item')

    for item in items:

        # unescape html entitiles
        htmlParser = html.parser.HTMLParser()
        title = htmlParser.unescape(item.find('title').text)
        # remove website name from title
        parts = title.split(' - ')
        source = parts[len(parts)-1]
        parts = parts[:-1]
        title = "-".join(parts)

        url = item.find('link').text
        link = url.split('url=')[1]

        date = item.find('pubdate').text
        category = item.find('category').text

        try:
            # print(title)
            # print(date)
            # print(link)
            # print('\n')

            article = getArticle(link)
            article['title'] = title
            article['date'] = date
            article['category'] = category
            article['source'] = source

            if article['body'] != "" and db.exist(article) is False:
                try:
                    article['body'] = summary.getSummary(article['body'])
                    if len(article['body']) < 60:
                        db.insert(article)
                except:
                    print(">> Error in summerising: ")
                    print(article['link'])

        except:
            print('error while fetching: '+link+'\n')

if __name__ == '__main__':
    getNews()