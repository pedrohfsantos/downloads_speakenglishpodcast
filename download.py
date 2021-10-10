from requests_html import HTMLSession
from tqdm.auto import tqdm
import os
from pprint import pprint

r = HTMLSession()
erros = []
name_mp3, name_pdf = 0, 0

if not os.path.dirname("downloads"):
    os.mkdir("downloads")


for number in tqdm(range(32, 0, -1)):
    try:
        url = r.get(f"https://speakenglishpodcast.com/podcast/page/{number}/")
        #links_eps = list(reversed(url.html.xpath('//*[@class="entry-title"]/a/@href')))
        links_eps = list(reversed(url.html.xpath('//*[@class="entry-title"]/a[starts-with(text(),"#")]/@href')))
        for link in links_eps:
            url_link = r.get(link)
            mp3, pdf = url_link.html.xpath('//h2[text()="Resources:"]/following-sibling::ul//li/a/@href')
            
            name_mp3 = name_mp3 + 1
            name_pdf = name_pdf + 1

            if not os.path.isfile(f"downloads/{name_mp3}.mp3"):
                try:
                    mp3 = r.get(mp3).content
                    with open(f"downloads/{name_mp3}.mp3", "wb") as data:
                        data.write(mp3)
                
                except:
                    erros.append(f"{name_mp3} - MP3({name_mp3})")
                    name_mp3 = name_mp3 + 1

            if not os.path.isfile(f"downloads/{name_pdf}.pdf"):
                try:
                    pdf = r.get(pdf).content
                    with open(f"downloads/{name_pdf}.pdf", "wb") as data:
                        data.write(pdf)
                    
                except:
                    erros.append(f"{name_pdf} - PDF({name_pdf})")
                    name_pdf = name_pdf + 1

    except:
        erros.append(f"page: {number}, PDF: {name_pdf}, MP3: {name_mp3}")
        name_pdf = name_pdf + 1
        name_mp3 = name_mp3 + 1



print("============ ERROS ============")
[print(x) for x in erros]