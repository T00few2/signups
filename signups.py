import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(
        cred, {"databaseURL": f"https://{st.secrets['firebase']['project_id']}.firebaseio.com"}
    )

# Firestore instance
admin_db = firestore.client()

# Fetch data from Firestore
collection_name = "raceSignups"
docs = admin_db.collection(collection_name).stream()
data = [doc.to_dict() for doc in docs]
data = pd.DataFrame(data)

# Transform the 'zwiftID' column
data['zwiftID'] = 'https://zwiftpower.com/profile.php?z=' + data['zwiftID'].astype(str)

# Select and rename columns
data = data[['group', 'displayName', 'phenotypeValue', 'currentRating', 'max30Rating', 'max90Rating', 'zwiftID']]
data.columns = ['Pen', 'Navn', 'Ryttertype', 'vELO', '30d vELO', '90d vELO', 'zwiftID']

# Inject custom CSS to set text color to white
st.markdown(
    """
    <style>
    /* Change text color in all tables */
    table, th, td {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.dataframe(data)

# Display the DataFrame
st.dataframe(
    data,
    hide_index=True,
    column_config={
        'zwiftID': st.column_config.LinkColumn('ZP profile', display_text='ZwiftPower'),
        'vELO': st.column_config.NumberColumn(format='%d', help='Current vELO rating'),
        '30d vELO': st.column_config.NumberColumn(format='%d', help='30 days max vELO rating'),
        '90d vELO': st.column_config.NumberColumn(format='%d', help='90 days max vELO rating'),
    }
)
