import numpy as np
import pandas as pd

# Reading DataFrame
df=pd.read_csv("Product.csv")

l=[]
with open('AllLinks.txt','r') as f:
    l=f.readlines()

df['links']=l
df.to_csv('Product_New.csv')