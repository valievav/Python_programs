import cfscrape  # library to bypass Cloudflare's anti-bot/ddos protection
import os, bs4
from urllib.parse import urlparse, urljoin
from urllib.request import urlretrieve


def download_comisc(urls, cwd):

    # create folder to store comics
    if not os.path.isdir(cwd):
        os.mkdir(cwd)

    os.chdir(cwd)

    # iterate over each comic in a list
    for url in urls:

        # bypass Cloudfare protection
        def get_page_bypass_cloudfare(protected_url):
            scraper = cfscrape.create_scraper()
            html = scraper.get(protected_url).content
            return html


        html = get_page_bypass_cloudfare(url)
        print(f"Retrieved HTML page for '{url}'")

        # get url path part to use for link search
        url_path = urlparse(url).path
        soup = bs4.BeautifulSoup(html, "html.parser")
        a_elements = soup.select(f"a[href^='{url_path}/']")
        print(f"Found {len(a_elements)} comic issues")

        # iterate over each comic issue link
        for a_elem in a_elements:
            href = a_elem.get("href")
            comic_issue = a_elem.find(text=True).strip()

            # create separate folder for each issue
            if not os.path.isdir(comic_issue):
                os.mkdir(comic_issue)
                print(f"Created directory {os.path.abspath(comic_issue)}")

            os.chdir(comic_issue)

            comic_page_number = 1

            while comic_page_number <= 30:
                issue_full_url = urljoin(url, href + f"#{comic_page_number}")
                issue_html = get_page_bypass_cloudfare(issue_full_url)
                soup_inner = bs4.BeautifulSoup(issue_html, "html.parser")
                print(f"Got HTML for page {issue_full_url}")
                img_elem = soup_inner.select("#imgCurrent")

                if img_elem:
                    img_path = img_elem[0].get("src")
                    file_name =f"{comic_issue} - page {comic_page_number}.jpg"
                    urlretrieve(img_path, file_name)
                    print(f"Saved file '{file_name}'. Original path = {img_path}")
                    comic_page_number+=1


            # go back cwd to create next folder in cwd directory
            os.chdir(cwd)


urls_list = ['https://readcomiconline.to/Comic/Saga', 'https://readcomiconline.to/Comic/Monstress']
working_folder = "D:\\Comics"
download_comisc(urls_list, working_folder)

