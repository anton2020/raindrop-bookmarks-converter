#!/usr/bin/env python
# coding: utf-8

# # Bookmarks Archive

# Goal: write a script to transform HTML file from Raindrop to readable HTML table
# 
# Further: download linked webpages, replace dead links with Web Archive, deploy and autorun every week...

# In[272]:


from bs4 import BeautifulSoup
import codecs
import pandas as pd
import datetime # to format time added


# In[273]:


filename = "Raindrop.io.html"


# In[274]:


f=codecs.open(filename, 'r', 'utf-8')
doc_html = f.read()
# f.write(html_str)
f.close()


# In[268]:


# make soup object with HTML
soup = BeautifulSoup(doc_html, 'html5') # TODO consider using format='html5lib' parser to avoid ambiguity warning? 


# In[271]:


# main process: HTML -> dict -> dataframe

dt_soup = soup.find_all('dt')
df = pd.DataFrame()

for i in range(2, len(dt_soup)): # TODO starting from index 2 is not pretty, any alternatives? 
  # o/w the first row of the df is duplicated, as second DT tag includes the whole html body
    
    if dt_soup[i].a != None:
        dict = dt_soup[i].a.attrs
        dict['title'] = dt_soup[i].a.string
        
        if (dt_soup[i].next_sibling != None) and (dt_soup[i].next_sibling.name == 'dd'):
            dict['description'] = dt_soup[i].next_sibling.string
            
        df_add = pd.DataFrame([dict])
        df_add.rename(index={0:i}, inplace=True) # TODO fix row indices (starting at 2)
        df = df.append(df_add)


# In[262]:


# clean up the table

df = df.sort_index(axis=1)

mycol = df['title']
df.drop(labels=['title'], axis=1, inplace = True)
df.insert(1, 'title', mycol)

df['add_date'] = pd.to_datetime(df['add_date'], unit='s')
df['last_modified'] = pd.to_datetime(df['last_modified'], unit='s')


# In[263]:


# HTML export

html = df.to_html(index=False, render_links=True, show_dimensions=True, border=1, justify='left', col_space=150)
html = "<table  style= \" width:100%; word-break: break-all; \" " + html[7:]
with open("output_table.html", "w") as f:
    f.write(html)


# In[264]:


# ### Alternative: table properties
# # TODO: consider using this alternative approach to flexibly change table styles

# # format links
# df['href'] = df['href'].apply(lambda x: '<a href="{0}">{0}</a>'.format(x))

# # format table

# html = df.style.set_properties(**{'font-size': '20pt', 
#                                     'font-family': 'Calibri',
#                                     'border-collapse': 'collapse',
#                                     'border': '1px solid black',
#                                     'width' : '100px',
#                                    }).render()

# #export table
# with open('myhtml.html','w') as f:
#     f.write(html)  

