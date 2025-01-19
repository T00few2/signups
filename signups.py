import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(
            cred, {"databaseURL": f"https://{st.secrets['firebase']['project_id']}.firebaseio.com"}
        )
        st.success("Firebase initialized successfully.")
    except Exception as e:
        st.error(f"Firebase initialization failed: {e}")
else:
    st.info("Firebase already initialized.")

# Firestore instance
try:
    admin_db = firestore.client()
except Exception as e:
    st.error(f"Failed to create Firestore client: {e}")

# Fetch data from Firestore
collection_name = "raceSignups"
try:
    docs = admin_db.collection(collection_name).stream()
    data = [doc.to_dict() for doc in docs]
    st.write(f"Number of documents fetched: {len(data)}")
except Exception as e:
    st.error(f"Error fetching documents: {e}")

# Create DataFrame
if data:
    df = pd.DataFrame(data)
    st.write("Data fetched from Firestore:", df)
else:
    st.warning("No data found in Firestore collection.")

# Validate columns
expected_columns = ['group', 'displayName', 'phenotypeValue', 'currentRating', 'max30Rating', 'max90Rating', 'zwiftID']
missing_columns = [col for col in expected_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing columns in data: {missing_columns}")
else:
    st.success("All expected columns are present.")

# Transform 'zwiftID' column
try:
    df['zwiftID'] = 'https://zwiftpower.com/profile.php?z=' + df['zwiftID'].astype(str)
    st.success("zwiftID column transformed successfully.")
except Exception as e:
    st.error(f"Error transforming 'zwiftID' column: {e}")

# Select and rename columns
try:
    df = df[['group', 'displayName', 'phenotypeValue', 'currentRating', 'max30Rating', 'max90Rating', 'zwiftID']]
    df.columns = ['Pen', 'Navn', 'Ryttertype', 'vELO', '30d vELO', '90d vELO', 'zwiftID']
    st.write("Final DataFrame:", df)
except Exception as e:
    st.error(f"Error selecting or renaming columns: {e}")

# Check for valid URLs
invalid_urls = df[~df['zwiftID'].str.startswith('https://zwiftpower.com/profile.php?z=')]
if not invalid_urls.empty:
    st.warning("Some zwiftID entries do not form valid URLs.")

# Display DataFrame
if not df.empty:
    try:
        st.dataframe(
            df,
            hide_index=True,
            column_config={
                'zwiftID': st.column_config.LinkColumn('ZP profile', display_text='ZwiftPower'),
                'vELO': st.column_config.NumberColumn(format='%d', help='Current vELO rating'),
                '30d vELO': st.column_config.NumberColumn(format='%d', help='30 days max vELO rating'),
                '90d vELO': st.column_config.NumberColumn(format='%d', help='90 days max vELO rating'),
            }
        )
    except Exception as e:
        st.error(f"Error displaying DataFrame: {e}")
else:
    st.warning("Final DataFrame is empty.")
