import streamlit as st
import pandas as pd 
import plotly.express as px 
from itertools import combinations 
from colledtions import Counter


st.title('Amazon Analytics Report')
#filename=st.selectbox(label='choose Data',options=['Shipped - Delivered to Buyer.csv','Cancelled.csv','Shipped - Damaged.csv','Shipped - Lost in Transit.csv','Shipped - Rejected by Buyer.csv','Shipped - Returned to Seller.csv'])
                                                

#delivered_df = pd.read_csv(filename)
#st.dataframe(delivered_df)
data = pd.read_csv('Shipped - Delivered to Buyer')
st.header('Shipped Order Analytics Report')

col1,col2,col3 = st.columns(3)

with col1:
    total_revenue = int(data['revenue'].sum())
    st.metric(label='Total Revenue',value=total_revenue)

with col2:
    total_orders = len(data['Order ID'].unique())
    st.metric(label='Total Orders',value=total_orders)

with col3:
    item_sold = data['Qty'].sum()
    st.metric(label='Qty',value=item_sold)
    
col4,col5 = st.coloumns(2)

with col4:
    total_state = len(data['ship-state'].unique())-1
    st.metric(label='State',value=total_state)
        
with col5:
    total_city = len(data['ship-city'].unique())-1
    st.metric(label='City',value=total_city)
    
st.divider()
st.header('State Wise Total Orders')
    
newdata = data.groupby('ship-state').agg(
total_quantity = ('Qty','sum')

)
newdata = newdata.reset_index()
newdata = newdata.sort_values(by='total_quantity',ascending=False)

fig = px.bar(newdata, x='ship-state',y='total_quantity',title='Total Quantity by Ship State')
st.plotly.chart(fig)

st.divider()
st.header('Month wise revenue')
mdf = data.groupby('Month').agg(
    month_revenue=('revenue','sum')
).reset_index()

fig = px.bar(mdf, x='Month',y='month_revenue',title='Monthly revenue')
st.plotly_chart(fig)

st.divider()
st.header('Number of Orders by Category')
fig = px.histogram(data, x='Category',title='Count of Categories',color='Size')
st.plotly_chart(fig)

st.divider()
st.header('B2B Vs B2C Order Chart')
bdf = data['B2B'].value_counts().reset_index()

bdf.loc[bdf['B2B']==False,'B2B'] = 'B2C'
bdf.loc[bdf['B2B']==True,'B2B'] = 'B2B'
fig=px.pie(bdf,values='count',names='B2B',title='B2B vs B2C')
st.plotly_chart(fig)

st.divider()
st.header('Average Revenue By Weekday and Weekend')
data['Day type'] = 'weekday'
data.loc[ (data['Day']=='Saturday') | (data['Day']=='sunday'), 'Day type' ]='Weekend'

wdf=data.groupby('Day type').agg(
    avg_revenue = ('revenue','mean')
).reset_index()
fig = px.bar(wdf,x='Day type',y='avg_revenue')
st.plotly_chart(fig)

st.title('Unsuccessful Delivery Data Analytics')
st.divider()
st.header('Product Combinations')
df=pd.read_csv('Amazon Sale Report.csv')
mdf = df.loc[data.duplicated(subset='Order ID',keep=False)]
mdf.to_excel('newdata.xlsx',index=False)

rdf=pd.read_excel('newdata.xlsx')
rdf['Product'] = rdf['Category']+'-'+ rdf['Size']
rdf  = rdf[['Order ID','Product']]
rdf['Product'] = rdf['Product']+','  #given coma between product sizes
rdf = rdf.groupby('Order ID').agg(
    group=('Product','sum')
).reset_index()
rdf['group'] = rdf['group'].str.strip(',')  #remove coma from last 
rdf['group'] = rdf['group'].str.split(',')
list3 = list(rdf['group'])
list3
count = Counter()

for i in list3:
    count.update((Counter(combinations(i,2))))
    
d=dict(count)
col1_data = list(d.keys())
col2_data = list(d.values())
qdf = pd.DataFrame()  #empty dataframe
qdf['Product Combinations'] = col1_data
qdf['Count'] = col2_data
st.dataframe(qdf)
