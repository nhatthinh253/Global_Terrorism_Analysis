import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pydeck as pdk
from plotly.subplots import make_subplots

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    return data




# Title
st.markdown(f'<h1 style="text-align: center; color: darkred;">Global Terrorism Analysis</h1>', 
                unsafe_allow_html=True) 

st.sidebar.header("Global Terrorism Analysis")

content = [  "Terrorist activities", 
             "Attacks by region",
              "Terrorist groups",
              "Target of terrorist groups",
              "Military Spending vs. Casualties",
              ]
nag = st.sidebar.radio("Go to:",content)

st.sidebar.header("About")
st.sidebar.info(
        "This project is contributed by:\n\n"   
        "Thinh Cao,  " 
        "Dom Brett, " 
        "Phat Nguyen \n\n"
        "[GitHub](https://github.com/nhatthinh253) | "
        "[LinkedIn](https://linkedin.com/in/nhatthinh253)"
    )

github = '[GitHub](https://github.com/nhatthinh253)'
linkedin = '[LinkedIn](https://linkedin.com/in/nhatthinh253)'
st.sidebar.markdown(github, unsafe_allow_html=True)
st.sidebar.markdown(linkedin, unsafe_allow_html=True)
# Import data_1
data1 = load_data('./data1.csv')

# data2 with a new col
data2 = data1.copy()
data2.nkill.fillna(0,inplace = True)
data2.nwound.fillna(0,inplace = True)
data2['ncasualty'] = data2.nkill + data2.nwound

if nag == "Terrorist activities":
    
    st.markdown('## **1. Terrorist activities from 1970 to 2017**')


    # Slider, set default 2014
    year = st.slider('Year', 1970,2017, 2014)

    # prepare data
    map_data = data1[~data1.longitude.isnull()][data1.iyear ==year]
    map_data = map_data[map_data['longitude'] > -180][['latitude','longitude','nkill', 'nwound']]

    map_data.nkill.fillna(0, inplace = True)
    map_data.nwound.fillna(0, inplace = True)
    map_data['ncasualty'] = map_data['nkill'] + map_data['nwound']

    
    st.markdown(f'- Total number of attacks: {map_data.shape[0]}')
    st.markdown(f'- Total number of casualties: {int(map_data.ncasualty.sum())}')


    # Severity of attacks

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9", 
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position=["longitude", "latitude"],
            pickable=False,
                opacity=0.4,
                stroked=True,
                filled=True,
                radius_scale=100,
                radius_min_pixels=4,
                radius_max_pixels=40,
                line_width_min_pixels=0.5,
                get_radius= 'ncasualty',
                get_fill_color=[252, 136, 3],
                get_line_color=[255,0,0],
                tooltip="test test",
            
            ),
        ],
    ))
    st.subheader(f'Map of terrorist activities in {year}')
    if st.checkbox('Show sample raw data'):
        st.write(map_data[0:10])

    # Key takeaways
    st.markdown('''Up to 2011, the number of attacks never exceeded 5000 per year.
    However, there has been a major increase in the number of attacks since 2012,
    with a spike to almost 17k attacks in 2014''')

    # Bar graph to visualize terrorism around the globe

    year_casualties = data2.groupby('iyear').agg({'eventid':'count','ncasualty':'sum'}).rename(columns={'eventid':'Number of attacks'})
    year_casualties['Casualties/attack'] = year_casualties['ncasualty']/ year_casualties['Number of attacks']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=year_casualties.index, y=year_casualties['ncasualty'], mode='lines+markers',name='casualties'))
    fig.add_trace(go.Bar(x=year_casualties.index, y=year_casualties['Number of attacks'],name='Number of attacks'))

    fig.update_layout(title_text="Attacks vs. Casualties from 1970 to 2017", xaxis_title="Year", yaxis_title="Total number", width = 780, height=500)
    fig.update_layout(legend=dict( orientation = 'h', yanchor="top",y= 1.15,xanchor="right", x=1))

    st.plotly_chart(fig)


    # Show data with checkbox
    if st.checkbox('Show data'):
        year_casualties

if nag == "Attacks by region":
    
    st.markdown('## **2. Attacks by region from 1970 to 2017**')

    # Create multiple selecter with  st.multiselect 
    st.markdown("#### " +"Which region would you like to see?")

    regions = data1.region_txt.unique()
    selected_region = st.multiselect(
        label="Choose a region", options= regions
    )

    # prepare data to plot
    df = pd.crosstab(data1.iyear,data1.region_txt)

    # Create traces
    fig = go.Figure()
    if selected_region:
        for region in  regions:
            if region in selected_region :

                fig.add_trace(go.Scatter(x=df.index, y=df[region], mode='lines+markers', name= region ))
        
        fig.update_layout(title=f"Attacks in {', '.join(selected_region)} from 1970 to 2017", xaxis_title="Year", yaxis_title="Number of attacks", legend_title="Regions",
        autosize=False, width=780, height=600,legend=dict( yanchor="top", y=1, xanchor="left", x=0.01))

        st.plotly_chart(fig)
    else:
        for region in  regions:
            fig.add_trace(go.Scatter(x=df.index, y=df[region], mode='lines', name= region))

        fig.update_layout(title="Attacks by region from 1970 to 2017", xaxis_title="Year", yaxis_title="Number of attacks", legend_title="Regions",
        autosize=False, width=780, height=600,legend=dict( yanchor="top", y=1, xanchor="left", x=0.01))

        st.plotly_chart(fig)


    # key takeaways
    st.markdown('MENA (Middle East & North Africa) and South Asia were the most affected regions by this increase in global terrorism, followed by Sub-Saharan Africa.')


if nag == "Terrorist groups":
    
    st.markdown('## **3. Notorious Terrorist Groups from 1970 to 2017**')

    # Top 10 all-time terrorist groups
    top_10_data = data1['gname'].value_counts()[1:11]
    fig = px.bar(x = top_10_data, y = top_10_data.index, title = "Top 10 Notorious Groups from 1970 - 2017",
        labels = {'y':'Terrorist Group', 'x':'Number of attacks'} )

    fig.update_layout( autosize=False, width=780, height=400,legend=dict(yanchor="top", y=1, xanchor="left", x=0.01))

    st.plotly_chart(fig)

    # show data top 10
    if st.checkbox('Show top 10 terrorist groups data'):
        top_10_data

    # Activities of top 5 notorious groups across the period
    terror_group = pd.crosstab(data1.iyear, data1.gname)
    top_10= top_10_data.index

    selected_groups = st.multiselect(
        label="Choose a terrorist group", options= top_10
    )
    fig = go.Figure()
    if selected_groups:
        for group in  top_10:
            if group in selected_groups :
                fig.add_trace(go.Scatter(x= terror_group[top_10].index, y=terror_group[top_10][group],mode='lines + markers',
                        name=group))

    else:
        for group in  top_10:
            fig.add_trace(go.Scatter(x= terror_group[top_10].index, y=terror_group[top_10][group],mode='lines + markers',
                        name=group))

    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01), autosize=False, width=800, height=600,
        title = 'Activities of top notorious groups from 1970 to 2017', xaxis_title="Year", yaxis_title="Number of attacks", legend_title="Terrorist groups")
    st.plotly_chart(fig, use_container_width = False)

    # Key takeaways
    st.markdown('''Before 2000, Farabundo Marti National Liberation Front (FMLN) and Shining Path (SL) 
    were the two major groups. These groups gradually weakened and seemed to stop in 1990s. 
    Taliban, Islamic State of Iraq and the Levant (ISIL) and Al-Shabaab emerged in 2000s and 
    have quickly become dominant in their own regions: South Asia, MENA, 
    and Sub-Saharan Africa respectively.''' )

    # Scope of operation
    st.subheader('Which regions do the terrorist groups operate in?')
    scope_top_10 = pd.crosstab(data1.region_txt,data1.gname )[top_10]
    scope_top_10.columns = ['Taliban', 'ISIL', 'SL', 'FMLN', 'Al-Shabaab', 'NPA', 'IRA', 'FARC','Boko Haram', 'PKK']
    st.dataframe(scope_top_10.style.highlight_max(axis=0))


    # Middle East & North Africa

    st.markdown('### **3.1 Middle East & North Africa**')

    # Prepare data
    MENA = data2[(data2.region_txt == 'Middle East & North Africa')]
    MENA_casualty = MENA.pivot_table(values='ncasualty', index=['iyear'], columns=['country_txt'], aggfunc='sum')


    MENA_countries = MENA.country_txt.value_counts()[0:5].index

    fig = go.Figure()
    for country in MENA_countries:
            fig.add_trace(go.Scatter(x=MENA_casualty.index, y=MENA_casualty[country],mode='lines+markers',
                        name=country))
    fig.update_layout(title="Casualties by country in MENA from 1970 to 2017", xaxis_title="Year", yaxis_title="Number of casualties", legend_title="Countries",
        autosize=False, width=780, height=400,legend=dict( bgcolor = 'rgba(255,255,255, 0.5)', yanchor="top", y=1, xanchor="left", x=0.01))
    st.plotly_chart(fig)


    # key takeaways
    st.markdown('**ISIL is responsible for most of the attacks in the region**')

    ISIL_data = data2[(data2.gname == 'Islamic State of Iraq and the Levant (ISIL)')
        & (data2.region_txt == 'Middle East & North Africa')]

    ISIL_casualty = ISIL_data.groupby(['country_txt'])['ncasualty'].sum().sort_values(ascending = False)
    ISIL_weapon = ISIL_data.attacktype1_txt.value_counts()
    ISIL_target = ISIL_data.targtype1_txt.value_counts()

    #  create subplots
    fig = make_subplots(rows=1, cols=3, shared_yaxes=False, horizontal_spacing= 0.1)

    # plot each subplot
    fig.add_trace(go.Bar(x = ISIL_casualty[0:5].index, y=ISIL_casualty[0:5], name = "Casualty"),1, 1)
    fig.add_trace(go.Bar(x = ISIL_weapon[0:5].index, y = ISIL_weapon[0:5], name = 'Weapon'),1, 2)
    fig.add_trace(go.Bar(x = ISIL_target[0:5].index, y = ISIL_target[0:5], name = "Target"), 1,3)

    # styling
    fig.update_layout(title_text="ISIL in Middle East & North Africa ", width = 780, height=500)
    fig.update_layout(legend=dict( orientation = 'h', yanchor="top",y= 1.2,xanchor="right", x=1))
    st.plotly_chart(fig)

    # key  takeways
    st.markdown('- Since 2003 bombings in Iraq have killed thousands of people, mostly Iraqi civilians by suicide bombings')

    st.markdown('''- The War in Iraq was an armed conflict. 
    the Iraqi insurgency escalated into a full-scale war with the conquest of Ramadi, 
    Fallujah, Mosul, Tikrit and in the major areas of northern Iraq by the ISIS''')

    # South Asia
    st.markdown('### **3.2 South Asia**')

    # prepare data
    South_asia = data2[(data2.region_txt == 'South Asia')]
    South_asia_casualty = South_asia.pivot_table(values='ncasualty', index=['iyear'], columns=['country_txt'], aggfunc='sum')
    SAsia_countries = South_asia.country_txt.value_counts()[0:5].index

    fig = go.Figure()
    for country in SAsia_countries:
            fig.add_trace(go.Scatter(x=South_asia_casualty.index, y=South_asia_casualty[country],mode='lines+markers',
                        name=country))

    fig.update_layout(title="Casualties by country in South Asia from 1970 to 2017", xaxis_title="Year", yaxis_title="Number of casualties", legend_title="Countries",
        autosize=False, width=780, height=400,legend=dict(  bgcolor = 'rgba(255,255,255, 0.5)', yanchor="top", y=1, xanchor="left", x=0.01))
    st.plotly_chart(fig)

    st.markdown('**Taliban is responsible for most of the attacks in Afghanistan and Pakistan**')

    Taliban_data = data2[(data2.gname == 'Taliban') & (data2.region_txt == 'South Asia')]
    Taliban_casualty = Taliban_data.groupby(['country_txt'])['ncasualty'].sum().sort_values(ascending = False)
    Taliban_target = Taliban_data.attacktype1_txt.value_counts()
    Taliban_weapon = Taliban_data.targtype1_txt.value_counts()

    #  create subplots
    fig = make_subplots(rows=1, cols=3, shared_yaxes=False, horizontal_spacing= 0.1)

    # plot each subplot
    fig.add_trace(go.Bar(x = Taliban_casualty[0:5].index, y=ISIL_casualty[0:5], name = "Casualty"),1, 1)
    fig.add_trace(go.Bar(x = Taliban_weapon[0:5].index, y = Taliban_weapon[0:5], name = 'Weapon'),1, 2)
    fig.add_trace(go.Bar(x = Taliban_target[0:5].index, y = Taliban_target[0:5], name = "Target"), 1,3)

    # styling
    fig.update_layout(title_text="Taliban in South Asia ", width = 780, height=500)
    fig.update_layout(legend=dict( orientation = 'h', yanchor="top",y= 1.2,xanchor="right", x=1))
    st.plotly_chart(fig)

    # key takeaways
    st.markdown('**1. Afghanistan:**')
    st.markdown("- Followed by Afghan Civil War's 1996–2001 phase when the U.S. aimed to dismantle al-Qaeda's safe operational base in Afghanistan by removing the power of Taliban after the 9/11 attack in NYC")
    st.markdown('- Over 100k have been killed in the war: 4k ISAF soldiers and civilian contractors, 60k+ Afghan national security forces, 30k+ civilians and even more Taliban')

    st.markdown('**2. Pakistan:**')
    st.markdown('- The Kashmir issue and across the border terrorism have been the cause of conflicts between the two countries mostly with the exception of the Indo-Pakistani War of 1971')



if nag == "Target of terrorist groups":
    
    st.markdown('## **4. Target of top 10 nororious terrorist groups**')
    ReT= {'Government (Diplomatic)':'Government','Government (General)':'Government',
      'Police':'Police & Military',  
      'Military':'Police & Military',
      'Airports & Aircraft':'Business and Utilities',
      'Business':'Business and Utilities',
      'Utilities':'Business and Utilities',
      'Food or Water Supply':'Business and Utilities',
      'Tourists':'Private Citizens & Property',
      'Journalists & Media':'Telecoms and Journalism',     
      'Telecommunication':'Telecoms and Journalism',    
      'Transportation':'Business and Utilities',  
      'Violent Political Party':'Other Violent Group',  
      'Terrorists/Non-State Militia':'Other Violent Group',    
      'Other':'Private Citizens & Property', 
      'Abortion Related':'Private Citizens & Property', 
      'Maritime':'Business and Utilities',
      'Religious Figures/Institutions':'Religious, Educational, Political',
      'Educational Institution':'Religious, Educational, Political',
      'NGO':'Religious, Educational, Political'}
      
    data2['targtype1_txt'].replace(ReT, inplace = True)

    
    gkk = data2.groupby(['gname'])

    all_groups = data2.gname.unique()
    top_10_data = data1['gname'].value_counts()[1:11]
    top_10= top_10_data.index


    selected_group = st.selectbox(
        label="Choose a terrorist group", options= top_10
        # or all_groups
    )

    group =  gkk.get_group(selected_group) 


    pd.crosstab(group.iyear,group.targtype1_txt).plot.bar(stacked=True,width=0.8)
    fig=plt.gcf()
    fig.set_size_inches(12,8)
    st.pyplot(fig)





if nag == "Military Spending vs. Casualties":
    
    st.markdown('## **5. Military Spending vs. Casualties**')
    # load new data
    warspending = pd.read_csv(r'./Militaryspending.csv',encoding='ISO-8859-1')

    # Cleaning for world spending
    warspending = warspending.drop(['Indicator Name'], axis=1)
    World = warspending[warspending['Name']=='World']
    World = World.drop(['Code', 'Type'], axis=1)
    World = World.set_index('Name')
    World.index = World.index.rename('Year')
    World = World.T
    World = World[:]

    # cleaning for individual Nations
    Nations = warspending[warspending['Type']=='Country']
    Nations = Nations.drop(['Code', 'Type'], axis=1)
    Nations = Nations.set_index('Name')
    Nations.index = Nations.index.rename('Year')
    Nations = Nations.dropna(axis=0, how='all')
    Nations = Nations.T

    casualties = data2.groupby('iyear')['ncasualty'].sum()

    # plot data
    fig = go.Figure()
    fig.add_trace(go.Bar(x=casualties.index, y=casualties, name='casualties'))

    fig.add_trace(go.Scatter(x=Nations.index, y=Nations['Nigeria']/1e5,
                        mode='lines+markers',
                        name='Nigeria Spending in $100,000'))
    fig.add_trace(go.Scatter(x=Nations.index, y=Nations['Iraq']/1e5,
                        mode='lines+markers',
                        name='Iraq Spending in $100,000'))
    fig.add_trace(go.Scatter(x=Nations.index, y=Nations['United States']/1e7,
                        mode='lines+markers',
                        name='US Spending in $10,000,000'))

    fig.update_layout(title_text="Spending vs Casualties ", width = 780, height=500)
    fig.update_layout(legend=dict( orientation = 'h', yanchor="top",y= 1.15,xanchor="right", x=1))
    st.plotly_chart(fig)


