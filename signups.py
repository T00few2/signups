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

st.title("Firebase Firestore with Streamlit")

# Example: Fetch data from a Firestore collection
collection_name = "raceSignups"
docs = admin_db.collection(collection_name).stream()

data = []
for doc in docs:
    data.append(doc.to_dict())
    
data = pd.DataFrame(data)

# Display data in Streamlit
st.write("Data from Firestore:", data)