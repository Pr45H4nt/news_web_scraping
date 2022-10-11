from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

option = Options()
option.headless= True

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
url = 'https://annapurnapost.com/tags/cpn-uml'
driver.get(url)

def main():
    pagination_counter = 0
    firstpage = scrape_items() #getting first page
    paginate() #paginating to next page
    secondpage = scrape_items() # next page
    data = firstpage + secondpage
    saving_as_plain(data)
    saving_as_unicode(data)
    driver.close()


def scrape_items():
    #getting image source to find the source
    images_scr = driver.find_elements(By.CLASS_NAME, 'single-category')
    #getting post texts
    posts = driver.find_elements(By.CLASS_NAME , 'single-category-text')


    Totaldata = []
    for i , img in zip(posts, images_scr):
        #title is in 'a' tag and adding attribute text to convert it in string
        title = i.find_element(By.TAG_NAME, 'a').text 
        date_posted = i.find_element(By.TAG_NAME, 'small').text
        #as 'src' is in html getting the inner html 
        image = img.get_attribute('innerHTML')

        data = {
            #formatting for the json file
            "Title" : title.replace("'", "").replace('"', ""),
            "Date Posted" : date_posted.replace('"', ""),
            #slicing between two words 'src' and 'alt' to find the link for the thumbnail
            "Thumbnail" : image[image.find('src')+5:image.find('alt')-2]
        }
        #appending the dict in the Total data
        Totaldata.append(data)
    return Totaldata

def paginate():
    global pagination_counter
    try:
        driver.find_element(By.LINK_TEXT, 'थप समाचार').click()
    except:
        #paginating again if any error happened, trying 8 times
        pagination_counter+= 1
        print('tried pagination', pagination_counter)
        while pagination_counter > 8:
            paginate()

def saving_as_unicode(item):
    #nepali is seen as unicode if we direct dump the json file, it will save as 'u/35...' format
    import json
    with open("rawinfo.json", 'a', encoding='utf-8', errors='ignore') as file:
        json.dump(obj=item, fp=file, indent=4)

def saving_as_plain(item):
    #for saving in plain form
    with open("info.json", 'a', encoding='utf-8', errors='ignore') as file:
        file.write("[")
        for i in item:
            #replacing " for any json error
            file.write(str(i).replace("'", '"')+",")
            file.write("\n")
        file.write("]")
    

if __name__ == "__main__":
    main()
