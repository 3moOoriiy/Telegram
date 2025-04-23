import streamlit as st
import requests
import pandas as pd

# إعدادات البوت
BOT_TOKEN = "7850779767:AAEt52D2I1OE38X-rNDRqC2ifah3OXefFDo"

# دالة سحب بيانات قناة تيليجرام باستخدام الرابط
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
                "Account Name": chat.get("title", "N/A"),
                "Account Bio": chat.get("description", "N/A"),
                "Status": "Active",
                "Link": link
            }
    return {
        "Account Name": "N/A",
        "Account Bio": "N/A",
        "Status": "Failed or Not Found",
        "Link": link
    }

# واجهة Streamlit
st.set_page_config(page_title="Telegram Scraper", layout="centered")
st.title("📢 Telegram Channel Scraper")

user_input = st.text_area("أدخل روابط القنوات (كل رابط في سطر):")

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ"):
    links = [u.strip() for u in user_input.split("\n") if u.strip()]
    if links:
        for link in links:
            result = get_channel_info_from_url(link)
            st.session_state.results.append(result)
    else:
        st.warning("يرجى إدخال رابط واحد على الأقل")

if st.session_state.results:
    st.markdown("---")
    st.subheader("📊 النتائج:")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 تحميل النتائج CSV", csv, "telegram_channels.csv", "text/csv")
