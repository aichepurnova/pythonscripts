#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import requests as req
import re


# In[2]:


print("Please input link to book like this: http://loveread.ec/read_book.php?id=18173&p=27")
link_to_book = input('Input link: ')


# In[3]:


def not_found_hanler():
    while True:
        try:
            max_page = int(input('Input page count: '))
            return max_page
        except: 
            print("That's not a number :(")


# In[4]:


try:
    book_id = re.findall(r"id=[0-9]*", link_to_book)
    book_id = book_id[0].replace('id=', '')
    print(f'Book ID: {book_id}')

except:
    print('Book ID not found, please input id from url')
    book_id = not_found_hanler()


# In[5]:


try:
    resp = req.get(f"http://loveread.ec/read_book.php?id={book_id}")
    soup = BeautifulSoup(resp.text, 'lxml')
    max_page = soup.find("a", text="Вперед").previous_sibling.get_text(strip=True)
    print(f'Page count: {max_page}')
except:
    print('Could not find page count. Please input page count here')
    max_page = not_found_hanler()


# In[6]:


print('Parsing your book.....')

full_book = f'Book copied from loveread.ec, id = {book_id}.'
for page in range(1,int(max_page)+1):
    try:
        resp = req.get(f"http://loveread.ec/read_book.php?id={book_id}&p={page}")
        soup = BeautifulSoup(resp.text, 'lxml')
        text = soup.find('div', {'class': 'MsoNormal'}).getText().replace('\n\n\n\nСтраница\n\n\n\n\n', '')
        full_book = full_book + '\n' + text
    except:
        full_book = full_book + 'PAGE ' + max_page + ' missing!'


# In[7]:


text_file = open(f"{book_id}.txt", "w")
n = text_file.write(full_book)
text_file.close()

print(f"Saved to {book_id}.txt")


# In[8]:


# # if you have Windows you can convert txt to epub.
# # If not, use some online converters

# # Firstly, install aspose-words package using this command:
# pip install aspose-words


# In[9]:


# # Then run the following 

# import aspose.words as aw

# doc = aw.Document(f"{book_id}.txt")
# doc.save(f"{book_id}.epub")

