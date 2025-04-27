import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def get_fakexy_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://www.fakexy.com/fake-address-generator-us'  # <-- Link đúng bạn cần
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        def get_value_by_id(id_name):
            element = soup.find('input', {'id': id_name})
            if element and 'value' in element.attrs:
                return element['value']
            return 'Không có dữ liệu'

        full_name = get_value_by_id('fullName')
        street = get_value_by_id('street')
        city = get_value_by_id('city')
        state = get_value_by_id('state')
        zip_code = get_value_by_id('zip')
        phone = get_value_by_id('phone')
        email = get_value_by_id('email')

        result_text = f"""📦 Thông tin lấy từ Fakexy:

👤 Full Name: {full_name}
🏠 Address: {street}
🏙️ City: {city}
🛣️ State: {state}
📮 ZIP: {zip_code}
📞 Phone: {phone}
📧 Email: {email}
"""

        await update.message.reply_text(result_text)

    except Exception as e:
        await update.message.reply_text("❗ Có lỗi xảy ra khi lấy thông tin từ Fakexy.")

def main():
    import os
    TOKEN = os.getenv('BOT_TOKEN')
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('fakexy', get_fakexy_info))
    
    application.run_polling()

if __name__ == '__main__':
    main()
