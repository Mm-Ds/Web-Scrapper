import requests
from bs4 import BeautifulSoup
from io import open

url='https://www.monster.fr/emploi/recherche/?q=Intelligence-Artificielle&where=Lyon__2C-Auvergne__2DRh__C3__B4ne__2DAlpes&jt=Stage-Apprentissage-Alternance&cy=fr&rad=20'
page= requests.get(url)
#print(page.content)
soup= BeautifulSoup(page.content,'html.parser')
results = soup.find(id='ResultsContainer')
#print(results.prettify().encode("utf-8"))
job_elems= results.find_all(lambda tag: tag.name == 'section' and tag.get('class') == ['card-content']) #returns an iterable , furthermore , the anonymous function is used because not only exact matchs are returned when using "results.find_all('section', class_='card-content')" (card-content ads... for expl are also returned)
print('\n_________________________________________________\n')
with open("Job list.log", "w", encoding="utf-8") as j_log:    # the job list is stored in a file (contrary to when using encode(utf) below in this case text is well written in the file )
     for job in job_elems:   # Each job_elem is a new BeautifulSoup object.
         
         title=job.find('h2',class_='title')   # you precise the node name and the attribute + its value you want to get 
         location= job.find('div',class_='location')
         company= job.find('div',class_='company')
 
         j_log.write(title.text.strip()+'\n')            # strip() removes any heading and trailing whitespace 
         j_log.write(location.text.strip()+'\n')
         j_log.write(company.text.strip()+'\n')
         j_log.write(u'\n---------------------------\n') #when the 'u' is not added there's an error: write() argument 1 must be unicode, not str 
         
         print(title.text.encode('utf-8').strip())   # there is an error with character \u2019 without encode(utf) and with the latter there are special characters    
         print(location.text.strip()) 
         print(company.text.strip())
         print('----------------\n'*2)
#find elemnts based on wether or not they contain a string in their title
#Beautiful Soup allows use of either exact strings or functions as arguments for filtering text in Beautiful Soup objects, we're gonna use a function
data_jobs = results.find_all('h2',string=lambda text: 'data' in text.lower())  # an anonymous function is passed in for the string argument , this lambda fct looks at the h2 elemnt's text , converts it into lower case and checks wether the sbstr data is found within it
print(len(data_jobs)) 

# getting the offer url. it is contained in the href attribute of the nested <a> tag 
for job_d in data_jobs:
     print('\n----------\n'+ str(job_d.text.encode('utf-8').strip()))
     link= job_d.find('a')['href'] # when using ('a',class_='href') returnes none objects
     print(link.encode('utf-8'))
     
# adding comment 1