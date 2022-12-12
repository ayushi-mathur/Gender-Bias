from selenium import webdriver
import pandas as pd

driver = webdriver.Firefox()

url = "https://www.resurchify.com/conference-ranking"

driver.get(url)

a = driver.find_element_by_class_name("d_table_font_size")
items = a.find_elements_by_class_name("w3-hover-sand")

Conference = []
Abbr = []
Grade = []


for item in items:
    c = item.find_elements_by_tag_name("td")
    Conference.append(c[0].find_element_by_tag_name("b").text)
    Abbr.append(c[1].find_element_by_tag_name("b").text)
    Grade.append(c[2].find_element_by_tag_name("b").text)


data = list(zip(Conference,Abbr, Grade))
df = pd.DataFrame(data,columns=['Conference','Abbreviation','Grade'])
df.to_csv('./conference_ranks')