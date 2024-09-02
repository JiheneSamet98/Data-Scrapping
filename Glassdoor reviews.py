import requests
from bs4 import BeautifulSoup
import pandas as pd 



def extract(pg): 
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.80 Safari/537.36'}
    url = f'https://www.glassdoor.com/Reviews/Google-Engineering-Reviews-EI_IE9079.0,6_DEPT1007_IP{pg}.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng'
    #Change the link for every company you want to extract the reviews for.
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')# this a soup function that return the whole html
    return soup

    #so we need to say define our new function and we'll say get reviews and in here we want to give it the soup that we have just returned from this function
def transform(soup): #to get reviews
  

    divs = soup.find_all('div', class_='gdReview')
    for item in divs:

        try:
          Title = item.find('h2', class_= 'mb-xxsm mt-0 css-93svrw el6ke055').text
        except:
          Title = None

        try:
          Rating = item.find('span', class_= 'ratingNumber mr-xsm').text.replace('<span class="ratingNumber mr-xsm">', '').strip()
        except:
          Rating = None    

        try:
          Employee_Situation= item.find('span', class_= 'pt-xsm pt-md-0 css-1qxtz39 eg4psks0').text.replace('<span class="pt-xsm pt-md-0 css-1qxtz39 eg4psks0">', '').strip()
        except:
          Employee_Situation = None  

        try:   
          Pros = item.find('span',  {'data-test':'pros'}).text.replace('<span data-test="pros">', '').strip()
        except:
          Pros = None

        try:  
          Cons = item.find('span',  {'data-test':'cons'}).text.replace('<span data-test="cons">', '')
        except:
          Cons: None

        try:
          Auhtor_Info = item.find('span', class_= 'common__EiReviewDetailsStyle__newUiJobLine').text.replace('<span class="common__EiReviewDetailsStyle__newUiJobLine"><span><span class="middle common__EiReviewDetailsStyle__newGrey">', '').strip()
        except:  
          Auhtor_Info = None

        Reviews = {
            'Title' : Title,
            'Rating': Rating,
            'Employee_Situation' : Employee_Situation,
            'Pros' : Pros,
            'Cons' : Cons,
            'Auhtor_Info' : Auhtor_Info,
        } 

        ReviewsList.append(Reviews) # To add reviews elements to our list 'ReviewList'
    return
   

ReviewsList = []
#c= extract(3)
#transform(c)


#loop into pages
for i in range(101,201,1):
    soup = extract( f'https://www.glassdoor.com/Reviews/Google-Engineering-Reviews-EI_IE9079.0,6_DEPT1007_IP{i}.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng')
    print(f' page {i}')
    
    #c= extract(i)
    transform(soup)
    
    print(len(ReviewsList))
    if not soup.find("data-test", class_ = "nextButton css-1hq9k8 e13qs2071"):
        pass
    else:
        break




df = pd.DataFrame(ReviewsList)

#print(df.head(1))
df.to_csv('DUP.csv')

print(len(ReviewsList))
#print(ReviewsList)

df2 = df.drop_duplicates(subset=["Title", "Rating", "Employee_Situation", "Pros", "Cons", "Auhtor_Info"], keep='first')

df2.to_csv('Google2.csv')
print(len(df2))
