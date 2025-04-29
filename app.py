import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- Google Drive Connect ---
@st.cache_resource
def connect_drive():
    raw_secrets = st.secrets["gdrive"]
    secrets_dict = dict(raw_secrets)
    secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\\\n", "\\n")

    credentials = service_account.Credentials.from_service_account_info(
        secrets_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build('drive', 'v3', credentials=credentials)

drive_service = connect_drive()

# --- 測試 GAMES_FOLDER_ID ---
GAMES_FOLDER_ID = "1G2VWwDHOHhnOKBNdnlut1oG5BOoUYAuf"  # 你的資料夾ID

try:
    query = f"'{GAMES_FOLDER_ID}' in parents and trashed=false"
    result = drive_service.files().list(q=query, spaces='drive').execute()
    files = result.get('files', [])
    st.success(f"✅ 測試成功！找到 {len(files)} 個檔案")
except Exception as e:
    st.error(f"❌ 測試失敗：{e}")
