from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import requests
import joblib

# Popularity based prediction dataframe
popular_data=joblib.load("Popular.sav")
df=pd.read_csv('Product.csv')
# Collabarative Filtering
collabarative=joblib.load("Collabarative.sav")
similarity=joblib.load("similarity.sav")
# Content Based
new_df=joblib.load("content.sav")
indexs=joblib.load("Indexs.sav")

searches=[]


def pop_recommend(category):
    popularity_df=popular_data[popular_data['Category']==category].head(5)
    popularity_df=popularity_df.sort_values('Avg_Rating',ascending=False)
    return popularity_df


def giverecomm(title):
  idx=indexs[indexs['title']==title].index[0]
  print(idx)
  sig=np.load(f"Sigmoid/sig{idx}.npy")
  sig_scores=list(enumerate(sig))
  sig_scores=sorted(sig_scores,key= lambda x:x[1],reverse=True)
  sig_scores=sig_scores[1:13]
#   print(sig_scores)
  product_index=[i[0] for i in sig_scores]
  print(product_index)
#   print(df.iloc[product_index])
  return new_df.iloc[product_index]

def recommend(product_title,similarity,collabarative):
    try:
        index=np.where(collabarative.index==product_title)[0][0]
        similar_products=sorted(list(enumerate(similarity[index])),key= lambda x:x[1],reverse=True)[1:6]
        l=[]
        for i in similar_products:
            a=df[df['title']==collabarative.index[i[0]]].head(1).index[0]
            l.append(a)
        flag=True
    except:
        flag=False
        l=[]
    return l,flag

#Creating Flask App

app= Flask(__name__)
global Category

@app.route('/')
def index():
    global searches
    if(len(searches)>=3):
        c1=pop_recommend(searches[-3])
        c2=pop_recommend(searches[-2])
        c3=pop_recommend(searches[-1])
        frames=[c1,c2,c3]
        temp=pd.concat(frames).head(12)
        return render_template('index.html',promy=temp.reset_index())
    else:
        temp=popular_data.head(12)
        return render_template('index.html',promy=temp)
    

@app.route('/shop/<category>')
def shop(category=""):
    c=str(category)
    if(c=="Baby"):
        filtered_df=df[df['Category'].str.contains(c, case=False)]
        filtered_df=filtered_df.sort_values('product_rating',ascending=False)
        return render_template('shop.html',products=filtered_df.head(150))
    elif(c=="Clothing"):
        filtered_df=df[df['Category'].str.contains("Clothing", case=False)]
        filtered_df=filtered_df.sort_values('product_rating',ascending=False)
        return render_template('shop.html',products=filtered_df[50:150])
    elif(c=="Electronics"):
        filtered_df=df[df['Category'].str.contains("Electronics", case=False)]
        filtered_df=filtered_df.sort_values('product_rating',ascending=False)
        return render_template('shop.html',products=filtered_df[50:150])
    elif(c=="Home_and_Furniture"):
        filtered_df=df[df['Category'].str.contains("Furniture", case=False)]
        filtered_df=filtered_df.sort_values('product_rating',ascending=False)
        return render_template('shop.html',products=filtered_df[20:150])
    elif(c=="other"):
        exclude=["Baby","Clothing","Electronics","Furniture"]
        filtered_df = df[~df['Category'].str.contains('|'.join(exclude), case=False)]
        filtered_df=filtered_df.sort_values('product_rating',ascending=False)
        return render_template('shop.html',products=filtered_df.head(150))


@app.route('/sproduct/<index>')
def specific(index=""):
    global searches
    a=int(index)
    category=df['Category'][a]
    searches.append(category)
    product=df[df.index==a]
    title=product['title'][a]
    same,flag=recommend(title,similarity,collabarative)
    similar_pr=giverecomm(title)
    return render_template("sproduct.html",flag=flag,product=product,similar=same,i=a,total=df,simi=similar_pr)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__=="__main__":
    app.run(debug=True)
# 