import requests                                         #loading essential libraries and packages
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",                          #using multilpe user agents to avoid  bots set by website
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64)..."
    
]




Master_list = {
    'Price 💲': [],'Location 🗺️': [],'Beds 🛏️': [],'Baths 🛁': [],'Area 📏': [],        #creating a master list to add all the lists 
'Image 🚠': [],'For more Details ❓': [],'Published Time⏲️': []                          to a final main list
}

for i in range(1,5):
    url = f"https://www.zameen.com/Homes/Lahore_DHA_Defence-9-{i}.html"                   #scrapping through 5 pages of the desired website
    

    headers = {
            "User-Agent": random.choice(user_agents)}                                     #calling the headers and usind random package to randomly 
    print(f"Scraping: {url}")                                                              use the headers



    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    time.sleep(random.uniform(3, 7))                                                   # adding time-delay in our requests for safety



    data = {'Price 💲': [], 'Location 🗺️': [], 'Beds 🛏️': [], 'Baths 🛁': [], 'Area 📏': [], 'Image 🚠': [], 'For more Details ❓': [], 'Published Time⏲️': []}


    price = soup.find_all("span", class_="dc381b54")
    for a in price:
        data["Price 💲"].append("PKR " + a.text)
        
    location = soup.find_all("div",class_="_52d0f124")
    for b in location:
        data["Location 🗺️"].append(b.text)

    beds = soup.find_all('span', attrs={'aria-label': 'Beds'})
    for c in beds:
        data["Beds 🛏️"].append("🛏️" + c.text)

    baths = soup.find_all('span', attrs={'aria-label': 'Baths'})
    for d in baths:
        data["Baths 🛁"].append("🛁" +  d.text)

    area = soup.find_all('span', attrs={'aria-label': 'Area'})
    for e in area:
        data["Area 📏"].append("📏" + e.text)

    images = soup.find_all("img",class_="fd6eb59d")
    for f in images:
        src=(f.get("src"))
        if src:  
            data["Image 🚠"].append(src)
    
    more_details=soup.find_all("a",class_="d870ae17")

    for g in more_details:
        relative_path=g.get("href")
        base_url = "https://www.zameen.com"
        full_url = base_url + relative_path
        data["For more Details ❓"].append(full_url)
        
    added_time= soup.find_all('span', attrs={'aria-label': 'Listing creation date'})
    
    for h in added_time:
        data["Published Time⏲️"].append("⌛" + h.text)
        
    
    min_len = min(len(col) for col in data.values())
    for key in data:                                                               #adjusting the elements to a same number to avoid errrors
        data[key] = data[key][:min_len]
        Master_list[key].extend(data[key])                                         #combining all the lists to a  master list 

df=pd.DataFrame.from_dict(Master_list)
df.to_excel("zameen_listings_all_pages.xlsx", index=False)                      storing the master list in a newly created ecxel sheet 
print("✅ Scraping complete. Data saved to 'zameen_listings_all_pages.xlsx'")     

