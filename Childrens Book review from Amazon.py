import requests
from bs4 import BeautifulSoup
import pandas as pd

# outside our functions i'm going to create a  review list
reviewlist = []

    #say the first function is going to be our get soup function so we're going to our soup function

#function it's going to take in the amazon page url and it's going to return the soup for us
def get_soup(url):
    url = f'https://www.amazon.co.uk/product-reviews/1407170708/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
    

    #so we need to say define our new function and we'll say get reviews and in here we want to give it the soup that we have just returned from this function
def get_reviews(soup):
  #um find always going to return us a list which we can then loop through
  #actually just start looping through each one of those reviews usinf for item in reviews
    reviews = soup.find_all('div', {'data-hook': 'review'})

    try:
        for item in reviews:
            review = {
                #the next piece of information that we should find is the reviews & the  rating. going to do dot strip afterwards to remove any extra white space
            'UserName': item.find('span', class_='a-profile-name').text.strip(),
            'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            #so i'm going to turn that into a float but to do that we need to remove some of the excess text. i'm replacing the end part of the string which we don't want with nothing then i'm stripping off all of the white text and in the hop the white space and then around that i'm asking it to turn it into a float value which is a decimal point number
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'date':  item.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in the United Kingdom on ', '').strip(),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip()
            
            }
            reviewlist.append(review)

    except:
        pass

        #review and we're going to create our dictionary around the whole of this and then we're going to turn title rating and body into our keys
# range: to generate the next url for the page that we want 
#x in range so our x becomes our page number
for x in range(1,50):
  #have this page number at the end so we can add our new number to that each time we loop through
    soup = get_soup(f'https://www.amazon.co.uk/product-reviews/1407170708/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    
    #if the element on the page that we look for for the next button is there break out the loop
    # if it is not the last page of reviews carry on scraping
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
      # if it finds 'a-disabled a-last' the scraping stops
        break

      # we're going to export the informations that we get into an ecel file . we're going to use our reviewlist as dataframe 
df = pd.DataFrame(reviewlist)
print(df)
df.to_excel('Child_Book.xlsx', index=False)
print('End.')