import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# إعدادات البوت لتليجرام
BOT_TOKEN = "7850779767:AAEt52D2I1OE38X-rNDRqC2ifah3OXefFDo"

# دالة لجلب بيانات قناة تيليجرام

def get_channel_info_from_url(link):
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

# دالة لجلب بيانات حساب ريديت

def get_reddit_info_from_url(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find("title")
            bio = ""
            if title_tag:
                account_name = title_tag.text.replace("u/", "").split(" - ")[0].strip()
            else:
                account_name = "N/A"
            desc_meta = soup.find("meta", {"name": "description"})
            if desc_meta:
                bio = desc_meta.get("content", "N/A")
            return {
                "Platform": "Reddit",
                "Account Name": account_name,
                "Account Bio": bio,
                "Status": "Active",
                "Link": link
            }
    except Exception as e:
        print("Error:", e)

    return {
        "Platform": "Reddit",
        "Account Name": "N/A",
        "Account Bio": "N/A",
        "Status": "Failed or Not Found",
        "Link": link
    }

# واجهة Streamlit
st.set_page_config(page_title="Account Scraper", layout="centered")
st.title("🌐 Account Scraper (Telegram + Reddit)")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
user_input = st.text_area("أدخل الروابط (كل رابط في سطر):")

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ"):
    links = [u.strip() for u in user_input.split("\n") if u.strip()]
    if links:
        for link in links:
            if platform == "Telegram":
                result = get_channel_info_from_url(link)
            elif platform == "Reddit":
                result = get_reddit_info_from_url(link)
            else:
                result = {
                    "Platform": platform,
                    "Account Name": "N/A",
                    "Account Bio": "N/A",
                    "Status": "Unsupported",
                    "Link": link
                }
            st.session_state.results.append(result)
    else:
        st.warning("يرجى إدخال رابط واحد على الأقل")

if st.session_state.results:
    st.markdown("---")
    st.subheader("📊 النتائج:")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 تحميل النتائج CSV", csv, "accounts.csv", "text/csv")
