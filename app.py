# نسخة نظيفة من مشروع تيليجرام + ريديت بدون أي أوامر إنشاء مجلد (تعمل مباشرة على Streamlit Cloud)
import os
import zipfile

project_path = "/mnt/data/telegram_reddit_streamlit_clean"
os.makedirs(project_path, exist_ok=True)

# كود التطبيق
app_code = '''import streamlit as st
import requests
import pandas as pd

# إعدادات Telegram bot
BOT_TOKEN = "7850779767:AAEt52D2I1OE38X-rNDRqC2ifah3OXefFDo"

# Telegram Scraper
def get_telegram_info(link):
    if "t.me/" in link:
        username = link.split("t.me/")[-1].strip().replace("/", "")
    else:
        username = link.strip()
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat?chat_id=@{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["ok"]:
            chat = data["result"]
            return {
                "Platform": "Telegram",
                "Account Name": chat.get("title", "N/A"),
                "Account Bio": chat.get("description", "N/A"),
                "Status": "Active",
                "Link": link
            }
    return {
        "Platform": "Telegram",
        "Account Name": "N/A",
        "Account Bio": "N/A",
        "Status": "Failed or Not Found",
        "Link": link
    }

# Reddit Scraper using Pushshift API
def get_reddit_info(link):
    if "reddit.com/user/" in link:
        username = link.split("reddit.com/user/")[-1].strip("/").split("/")[0]
    else:
        username = link.strip()
    try:
        url = f"https://api.pushshift.io/reddit/comment/search/?author={username}&size=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.json().get("data"):
            return {
                "Platform": "Reddit",
                "Account Name": username,
                "Account Bio": "N/A (Pushshift API)",
                "Status": "Active",
                "Link": f"https://www.reddit.com/user/{username}/"
            }
        else:
            return {
                "Platform": "Reddit",
                "Account Name": username,
                "Account Bio": "N/A",
                "Status": "Not Found",
                "Link": f"https://www.reddit.com/user/{username}/"
            }
    except:
        return {
            "Platform": "Reddit",
            "Account Name": username,
            "Account Bio": "N/A",
            "Status": "Error",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# واجهة Streamlit
st.set_page_config(page_title="Account Scraper", layout="centered")
st.title("🌐 Telegram & Reddit Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
user_input = st.text_area("أدخل الروابط (رابط في كل سطر):")

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ"):
    links = [link.strip() for link in user_input.split("\\n") if link.strip()]
    for link in links:
        if platform == "Telegram":
            result = get_telegram_info(link)
        elif platform == "Reddit":
            result = get_reddit_info(link)
        else:
            result = {
                "Platform": platform,
                "Account Name": "N/A",
                "Account Bio": "N/A",
                "Status": "Unsupported",
                "Link": link
            }
        st.session_state.results.append(result)

if st.session_state.results:
    st.markdown("---")
    st.subheader("📊 النتائج:")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 تحميل النتائج CSV", csv, "accounts.csv", "text/csv")
'''

# requirements.txt
reqs = "streamlit\nrequests\npandas\n"

# كتابة الملفات
with open(f"{project_path}/app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

with open(f"{project_path}/requirements.txt", "w", encoding="utf-8") as f:
    f.write(reqs)

# ضغط المشروع
zip_path = "/mnt/data/telegram_reddit_streamlit_clean.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.write(f"{project_path}/app.py", arcname="app.py")
    zipf.write(f"{project_path}/requirements.txt", arcname="requirements.txt")

zip_path
