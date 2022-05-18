import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import pymysql
import s3fs










icon=Image.open("icon.png")

st.set_page_config(page_title="Web Banners Stats",layout="wide",page_icon=icon,initial_sidebar_state="collapsed")

fs = s3fs.S3FileSystem()



st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


hide_menu_style="""
               <style>
               #MainMenu {visibility : hidden ;}
               footer {visibility : hidden ;}
               </style>
               """


st.markdown(hide_menu_style, unsafe_allow_html=True)












def occurence_page():
    r1, r2, r3 ,r4= st.columns((0.2,0.5,1, 0.25))
    r1.image(icon)
    r3.title("Web Banners Stats")


    i1, i2, i3, i4 = st.columns(4)
    o1, o2 = st.columns(2)


    Start_day = i1.selectbox('select starting day ', options=df['day'].unique())

    End_day = i2.selectbox('select ending day', options=df['day'].unique())

    Start_hour = i3.selectbox('select starting hour ', options=df['hour'].unique(),index=8)
    End_hour = i4.selectbox('select ending hour', options=df['hour'].unique(),index=18)

    page = o1.multiselect('select banners page level', options=df['page'].unique(), default=df['page'].unique())
    type = o2.multiselect('select banners type', options=df['type'].unique(), default=df['type'].unique())
    s1,s2 =st.columns(2)


    df_advertiser = df.query(
        "page==@page & type==@type  & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour  "
    )



    advertiser= s1.multiselect('select advertiser', options=df_advertiser['advertiser'].unique(),
                default=df_advertiser['advertiser'].unique())




    Editor = s2.multiselect('select editor', options=df_advertiser['site'].unique(), default=df_advertiser['site'].unique())


    NumberOfAdvertisers = st.selectbox('select number of advertisers ', options=['5', '10', '15', '20'])

    df_selection = df.query(
        "page==@page & type==@type & advertiser ==@advertiser & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour & site==@Editor "
    )


    dfResume = pd.DataFrame(columns=['advertiser', 'occurence'])
    dfsites = pd.DataFrame(columns=['site', 'occurence'])

    count1 = pd.Series(df_selection['advertiser']).value_counts()
    count2 = pd.Series(df_selection['site']).value_counts()
    advertiserresults = {}
    sitesoccurence = {}
    for item in df_selection['advertiser']:
        advertiserresults[item] = count1[item]
    for item in df_selection['site']:
        sitesoccurence[item] = count2[item]
    i = 0
    for key in advertiserresults:
        dfResume.loc[i] = [key, advertiserresults[key].astype(float)]
        i += 1
    i = 0
    for key in sitesoccurence:
        dfsites.loc[i] = [key, sitesoccurence[key]]
        i += 1



    st.markdown('#')


    if len(dfResume['advertiser'])>0:
        b = alt.Chart(dfResume.nlargest(int(NumberOfAdvertisers), 'occurence'), title="Nombre d'impressions des top "+NumberOfAdvertisers+" annonceurs").mark_bar().encode(x=alt.X("occurence", axis=alt.Axis(title="Nb d'impressions")), y=alt.Y("advertiser",sort='-x'),
                                                                                  tooltip=["advertiser", "occurence"]).properties(height=300)





        p = alt.Chart(dfsites, title="Nombre d'impressions des sites").mark_arc().encode(theta=alt.Theta(field="occurence", type="quantitative"),
        color=alt.Color(field="site", type="nominal"),
                                                                         tooltip=["site", "occurence"])
        f1,f2=st.columns((1,2))
        f1.altair_chart(p, use_container_width=True)
        f2.altair_chart(b, use_container_width=True)
        advertisers = df_selection["advertiser"].unique()
        response = st.text_input('insert advertiser here for a sample of ads:')
        adsNumber=5
        advertisername=response

        if response in advertisers:
            A1, A2 , A3 = st.columns(3)
            B1, B2 , B3 = st.columns(3)

            if adsNumber > int(dfResume.loc[dfResume['advertiser'] == advertisername]['occurence']):

                # ads=df_selection.loc[df['advertiser']==advertisername]['adlink']
                ads2 = fs.ls("detectedads/" + advertisername)

                w = 0
                for ad in ads2:

                    with fs.open(ad) as f:

                        f = Image.open(f)
                        if f.size[1]>500:

                            f=f.resize((int((f.size[0]*f.size[1])/500),500))
                            if w == 0:
                                A1.image(f)
                            if w == 1:
                                A2.image(f)
                            if w == 2:
                                A3.image(f)
                            if w == 3:
                                B1.image(f)
                            w += 1
                        else :
                            if w == 0:
                                A1.image(f)
                            if w == 1:
                                A2.image(f)
                            if w == 2:
                                A3.image(f)
                            if w == 3:
                                B1.image(f)
                            w += 1
            else:

                # ads=df_selection.loc[df_selection['advertiser']==advertisername]['adlink'][:adsNumber]
                ads2 = fs.ls("detectedads/" + advertisername)
                ads2 = ads2[:adsNumber]
                w = 0
                for ad in ads2:

                    with fs.open(ad) as f:
                        f = Image.open(f)
                        if f.size[1]>500:
                            f = f.resize((int((f.size[0] * f.size[1]) / 500), 500))
                            if w == 0:
                                A1.image(f)
                            if w == 1:
                                A2.image(f)
                            if w == 2:
                                A3.image(f)
                            if w == 3:
                                B1.image(f)

                            if w == 4:
                                B2.image(f)
                            w += 1
                        else :
                            if w == 0:
                                A1.image(f)
                            if w == 1:
                                A2.image(f)
                            if w == 2:
                                A3.image(f)
                            if w == 3:
                                B1.image(f)

                            if w == 4:
                                B2.image(f)
                            w += 1










conn=pymysql.connect(host='bannersdet.cbai1qawgjuw.us-east-2.rds.amazonaws.com',port=int(33066),user='admin',passwd='s0nF8#v!1',db='bannersDetections')


cursor=conn.cursor()


sql="SELECT * FROM Detections1"
cursor.execute(sql)
df = cursor.fetchall()
df=pd.DataFrame(df,columns=['advertiser', 'type', 'page', 'site', 'day','hour','adlink'])









occurence_page()



