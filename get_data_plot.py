import pandas as pd 
import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from datetime import datetime as dt
import time


url='http://pokemondb.net/pokedex/all'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))

#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]

    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=10:
        break

    #i is the index of our column
    i=0

    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
df = df[['Name','Speed']]
speed = pd.DataFrame(df['Speed'].value_counts().reset_index()[:20])
speed = speed.rename(columns={'index': 'speed', 'Speed': 'count'})
print(speed)

curr_timestamp = int(time.time())
print(curr_timestamp)
# path = os.path.abspath(f'output/speed_{curr_timestamp}.csv')
# save(users=users, path=path)

plt.figure(figsize=(12,6))
ax = sns.barplot(x="speed", y="count", data=speed)
ax.set_title('Most frequent Pokemon players speed at time{}'.format(curr_timestamp), fontsize = 20)
ax.set_ylabel('frequncy', fontsize = 15)
ax.set_xlabel('speed', fontsize = 15)
plt.savefig('speed_{}.format(curr_timestamp).png')
plt.show()

