import streamlit as st
import pandas as pd
import numpy as np
####################### CALCULATOR ########################

offset = 8.5
one_year = 7.35
two_year = 7.05

f = 26.0555
m = 12
w = 52



def get_calculated_payments(rate, amount,T):
    r = rate/100
    sqr_brackets_m = (1-(1+r/m)**(-m*T))/(r/m)
    sqr_brackets_f = (1-(1+r/f)**(-f*T))/(r/f)
    sqr_brackets_w = (1-(1+r/w)**(-w*T))/(r/w)

    monthly_payment = round(amount/sqr_brackets_m,2)
    fortnightly_payment = round(amount/sqr_brackets_f,2)
    weekly_payment = round(amount/sqr_brackets_w,2)

    return weekly_payment, fortnightly_payment, monthly_payment


def get_calculated_dataframe(split_ratio,mortgage_amount,term):
    total_weekly = 0.0
    total_fornight = 0.0
    total_month = 0.0
    col_names = ['Type', 'Amount','Rate', 'Weekly','Forthnight', 'Monthly']
    my_df  = pd.DataFrame(columns = col_names)
    print(split_ratio)

    for row in split_ratio:
        ratio = row[0]
        percentage = row[1]
        name = row[2]
        print('{}-{}:{}'.format(name,ratio, percentage))
        amount = ratio/100 * mortgage_amount
        payments = get_calculated_payments(percentage,amount,term)
        w_ins = round(payments[0],2)
        f_ins = round(payments[1],2)
        m_ins = round(payments[2],2)
        my_df.loc[len(my_df.index)] = [name, amount,percentage,w_ins,f_ins,m_ins] 
        
        total_weekly += payments[0]
        total_fornight += payments[1]
        total_month += payments[2]
    my_df.loc[len(my_df.index)] = ['Totals', mortgage_amount,'',
                                   round(total_weekly,2),round(total_fornight,2),round(total_month,2)]
    return my_df 

####################### STREAMLIT SECTION ########################

loan_terms = [ 'Select','Off Set','One Year','Two Year','Three Year','Four Year','Five Year','Variable']

st.title(' 🎯 :blue[MORTGAGE CALCULATOR] 🎯')

with st.sidebar:
    st.header('🎯 Mortgage Calculator 🎯', divider='blue')
    st.markdown('Introducing our **Mortgage Calculator** tool — your key to informed home financing decisions! Input your loan details such as the loan amount and term period, and effortlessly visualize weekly, fortnightly and monthly payments')
    st.subheader('Mortgage Split', divider='blue')
    st.markdown('You can use this section to split your mortgage into different loan options offered by your financial provide. **Ensure** that your total split adds up to 100')
    st.header('☕ Support Us ☕', divider='blue')
    st.markdown('Love our Mortgage Calculator? Support our work by **[buying us a coffee](https://www.buymeacoffee.com/jaanakaaree)**. Your generosity fuels more financial tools for you')
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input('Loan Amount',value=300000,help="Enter the total loan amount")
with col2:
    term = st.number_input('Term Duration',min_value=1, max_value=30,value=25,
                       help="Enter the term of the loan, maximum is 30 years")


st.write('#### Mortgage Split')

r1_col1, r1_col2,r1_col3 = st.columns([2,1,1])
row1mortage_type = r1_col1.selectbox("Select Mortgage Type",loan_terms,key='row1mortage_type',
                                     label_visibility='visible',index=1)
row1mortage_split = r1_col2.number_input("Mortgage Split",min_value=5, max_value=100,value=50,key='row1mortage_split',
                     label_visibility='visible')
row1mortage_rate = r1_col3.number_input("Mortgage Rate",min_value=0.0, max_value=20.0, value=8.5,key='row1mortage_rate',
                     label_visibility='visible')

r2_col1, r2_col2,r2_col3 = st.columns([2,1,1])
row2mortage_type = r2_col1.selectbox("",loan_terms,index=2,key='row2mortage_type',label_visibility='collapsed')
row2mortage_split = r2_col2.number_input("",min_value=0, max_value=100,value=50,key='row2mortage_split',
                     label_visibility='collapsed')
row2mortage_rate = r2_col3.number_input("Mortgage Rate",min_value=0.0, max_value=20.0, value=7.35,key='row2mortage_rate',
                     label_visibility='collapsed')

r3_col1, r3_col2,r3_col3 = st.columns([2,1,1])
row3mortage_type = r3_col1.selectbox("",loan_terms,key='row3mortage_type',
                  label_visibility='collapsed')
row3mortage_split = r3_col2.number_input("",min_value=0, max_value=100,value=0,key='row3mortage_split',
                     label_visibility='collapsed')
row3mortage_rate = r3_col3.number_input("Mortgage Rate",min_value=0.0, max_value=20.0, value=8.5,key='row3mortage_rate',
                     label_visibility='collapsed')

r4_col1, r4_col2,r4_col3 = st.columns([2,1,1])
row4mortage_type = r4_col1.selectbox("",loan_terms,key='row4mortage_type',
                  label_visibility='collapsed')
row4mortage_split = r4_col2.number_input("",min_value=0, max_value=100,value=0,key='row4mortage_split',
                     label_visibility='collapsed')
row4mortage_rate = r4_col3.number_input("Mortgage Rate",min_value=0.0, max_value=20.0, value=8.5,key='row4mortage_rate',
                     label_visibility='collapsed')


def generate_split_ration():
    my_split_ratio = [[]] 
    if row1mortage_type != 'Select':
        my_split_ratio[0].append(row1mortage_split)  
        my_split_ratio[0].append(row1mortage_rate)              
        my_split_ratio[0].append(row1mortage_type)

    if row2mortage_type != 'Select':
        my_split_ratio.append([])
        my_split_ratio[1].append(row2mortage_split)  
        my_split_ratio[1].append(row2mortage_rate)              
        my_split_ratio[1].append(row2mortage_type)   

    if row3mortage_type != 'Select':
        my_split_ratio.append([])
        my_split_ratio[2].append(row3mortage_split)  
        my_split_ratio[2].append(row3mortage_rate)              
        my_split_ratio[2].append(row3mortage_type) 

    if row4mortage_type != 'Select':
        my_split_ratio.append([])
        my_split_ratio[3].append(row4mortage_split)  
        my_split_ratio[3].append(row4mortage_rate)              
        my_split_ratio[3].append(row4mortage_type)             

    return my_split_ratio

split_ratio = [
    [20,offset,'Off Set'],
    [30,one_year,'One Year'],
    [50,two_year,'Two Year']
]
if st.button('Calculate'):
    calculated_df = get_calculated_dataframe(generate_split_ration(),amount,term)
    # st.write("You selected:", generate_split_ration())
    st.dataframe(calculated_df,use_container_width=True,hide_index =True)


