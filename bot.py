import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def get_fakexy_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://www.fakexy.com/fake-address-generator-usa'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm các thẻ chứa thông tin
        info_blocks = soup.find_all('div', class_='col-md-6 col-lg-4')
        
        result_text = "📦 Thông tin lấy từ Fakexy:\n\n"
        for block in info_blocks:
            title = block.find('h5')
            value = block.find('p')
            if title and value:
                result_text += f"🔹 {title.text.strip()}: {value.text.strip()}\n"

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
