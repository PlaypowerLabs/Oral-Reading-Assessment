import streamlit as st

x = st.slider('Range',min_value=10,max_value=100)
st.write(f'Selected Value : {x}')
button = st.button('Click', key='button_val')
st.write(f'Button State : {button}')
st.write(st.session_state.button_val)

# if 'key1' not in st.session_state:
#     st.session_state.key1 = True

# st.write(st.session_state)