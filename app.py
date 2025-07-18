#pip install google-search-results
import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": "4ae5a74eafbd10c44e07ce266240e2a95f9e46f322e87bf9e5bd00b35d13bad4",
        "gl": "In"
    }
    search=serpapi.GoogleSearch(params)
    result=search.get_dict()
    shopping_results=result["shopping_results"]
    return shopping_results

c1,c2=st.columns(2)
c1.image("e_pharmacy.png",width=200)
c2.header("E-Commerce Comparision System")

st.sidebar.title("Product Details Input")
med_name=st.sidebar.text_input("Enter The Name Of Product")
med_no=st.sidebar.text_input("Enter the No For Comparision")



if med_name is not None:
    if st.sidebar.button("Comp Price"):
        shopping_results=compare(med_name)
        lowest_price=float((shopping_results[0].get('price').replace(",","").replace(" ",""))[1:])
        lowest_price_index=0
        med_cmp=[]
        med_price=[]

        for i in range(int(med_no)):
            st.title(f"Option{i+1}")
            st.sidebar.image(shopping_results[i].get('thumbnail'))
            med_cmp.append(shopping_results[i].get('source'))


            current_price=float((shopping_results[i].get('price').replace(",","").replace(" ",""))[1:])
            med_price.append(current_price)
            c1, c2 = st.columns(2)
            c1.write("Company")
            c2.write(shopping_results[i].get('source'))

            c1.write("Title")
            c2.write(shopping_results[i].get('title'))

            c1.write("Price")
            c2.write(current_price)

            url=shopping_results[i].get('product_link')
            c1.write("Buy Link")
            c2.write("[Click Here For Details](%s)"%url)
            """........................................................................................................."""

            if current_price<lowest_price:
                lowest_price=current_price
                lowest_price_index=i

        st.title("Best Option")
        c1, c2 = st.columns(2)
        c1.write("Company")
        c2.write(shopping_results[lowest_price_index].get('source'))

        c1.write("Title")
        c2.write(shopping_results[lowest_price_index].get('title'))

        c1.write("Price")
        c2.write(float((shopping_results[lowest_price_index].get('price').replace(",","").replace(" ",""))[1:]))

        url=shopping_results[lowest_price_index].get('product_link')
        c1.write("Buy Link")
        c2.write("[link](%s)"%url)

        st.title("Comparision")
        df=pd.DataFrame(med_price,med_cmp)
        st.bar_chart(df)

        fig,ax=plt.subplots()
        ax.pie(med_price,labels=med_cmp,shadow=True,autopct="%0.1f%%")
        ax.axis("equal")
        st.pyplot(fig)
