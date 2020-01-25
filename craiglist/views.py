from django.shortcuts import render
from bs4 import BeautifulSoup

import requests
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_URL = "https://sfbay.craigslist.org/search/?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"

def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(quote_plus(search))

    final_url = BASE_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listing = soup.find_all('li', {'class':'result-row'})
    
    # post_title = post_listing[2].find(class_='result-title').text
    # post_url = post_listing[2].find('a').get('href')
    # post_price = post_listing[2].find(class_='result-price').text
    # post_rext = post_listing[0]

    # print(post_title)
    # print(post_url)
    # print(post_price)
    
    final_posting = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'not available'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            # print(post_image_id)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/e15/c0.0.1079.1079a/s640x640/73457388_149577386375751_8680299658761032833_n.jpg?_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=103&_nc_ohc=7DhwcTjo3yMAX8cQ-c1&oh=eaed25f488fdfac1cecaf81041f6ee13&oe=5EAE8898'
            

        # print('aa')

        # if post.find(class_='result-image').get('data_ids'):
        #     post_image = post.find(class_='result-image').get('data_ids')
        #     print(post_image)

            
        # else:
        #     post_image = 'https://scontent-atl3-1.cdninstagram.com/v/t51.2885-15/e15/c0.0.1079.1079a/s640x640/73457388_149577386375751_8680299658761032833_n.jpg?_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_cat=103&_nc_ohc=7DhwcTjo3yMAX8cQ-c1&oh=eaed25f488fdfac1cecaf81041f6ee13&oe=5EAE8898'


        final_posting.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_posting,
    }
    return render(request, 'craiglist/new_search.html', stuff_for_frontend)