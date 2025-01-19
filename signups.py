import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase Admin
if not firebase_admin._apps:  # Prevent reinitialization in Streamlit
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(
        cred, {"databaseURL": f"https://{st.secrets['firebase']['project_id']}.firebaseio.com"}
    )

# Firestore instance
admin_db = firestore.client()

# Example: Fetch data from a Firestore collection
collection_name = "raceSignups"
docs = admin_db.collection(collection_name).stream()

data = []
for doc in docs:
    data.append(doc.to_dict())
    
data = pd.DataFrame(data)

data['zwiftID'] = 'https://zwiftpower.com/profile.php?z=' + data['zwiftID']

data = data[['group','displayName','phenotypeValue','currentRating','max30Rating','max90Rating','zwiftID']]
data.columns = ['Pen','Navn','Ryttertype','vELO','30d vELO','90d vELO','zwiftID']

# Display data in Streamlit
st.dataframe(
    data,
    hide_index=True,
    column_config={
        'zwiftID': st.column_config.LinkColumn('ZP profile', display_text='ZwiftPower'),
        'vELO': st.column_config.NumberColumn(format='%d', help='Current vELO rating'),
        '30d vELO': st.column_config.NumberColumn(format='%d', help='30 days max vELO rating'),
        '90d vELO': st.column_config.NumberColumn(format='%d', help='90 days max vELO rating'),
    
    })