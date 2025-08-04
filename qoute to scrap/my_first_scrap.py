import requests,json,sys
from bs4 import BeautifulSoup

url_base = "https://quotes.toscrape.com/page/{}/"
page = 1
titles = []
while True: #it will extract data from every page and increament in page
    url = url_base.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    qoute = soup.find_all("div",class_="quote")
    if not qoute: #if quote is empty then it program will simple exit with good bye msg
        sys.exit("Good Bye!")
    for q in qoute:# taking every quote separately from each page
        text = q.find("span",class_="text").text.strip()
        author = q.find("small",class_="author").text.strip()
        link = q.find("a")["href"]
        Tags = q.find_all("a",class_="tag")
        tag = [t.text.strip() for t in Tags] #using list comprehension for tags 
        titles.append({"text":text,"author":author,"link":link,"Tags":tag})
    with open("titles.json","+w",encoding= "utf-8") as f: # +w for write and read method at same time
        f.write(json.dumps(titles,ensure_ascii=False,indent=4))
        f.seek(0) # taking typing cursor back to start because after writing it will came to end
        data = json.load(f)# we have to load json file instead of read
        print(json.dumps(data,indent=4,ensure_ascii=False))
    page +=1 #moving to next page