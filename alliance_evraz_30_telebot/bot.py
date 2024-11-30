import telebot
from telebot.types import Message
from services.process_file import process_zip_file

bot = telebot.TeleBot("8121352331:AAHoZPsN1c471o1_MV1vPGEVKMhT8g58Y_s")


@bot.message_handler(content_types=['document'])
def handle_document(message: Message) -> None:
    if message.document.file_name.endswith('.py'):
        bot.reply_to(message, "Мы проверяем комплексно проект, пожалуйста, отправьте zip-архив. Мы не обрабатываем файлы")
        return

    if not message.document.file_name.endswith('.zip'):
        bot.reply_to(message, "Пожалуйста, отправьте zip-архив")
        return

    bot.reply_to(message, "Файл загружается...")

    try:
        pdf_path = process_zip_file(
            bot=bot,
            file_id=message.document.file_id,
            file_name=message.document.file_name,
            chat_id=message.chat.id,
        )

        with open(pdf_path, "rb") as pdf_file:
            bot.send_document(message.chat.id, pdf_file)
    except Exception as e:
        bot.reply_to(message, f"Ошибка обработки файла: {str(e)}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message) -> None:
    bot.reply_to(message, "Пожалуйста, загрузки файл с расширением .zip")

@bot.message_handler(commands=['start'])
def start_message(message: Message) -> None:
    bot.reply_to(message, "Привет! Я бот для проверки проектов. Отправьте мне архив для обработки.")

@bot.message_handler(func=lambda message: True)
def unknown_command(message: Message) -> None:
    bot.reply_to(message, "Я не знаю такой команды :(")

if __name__ == "__main__":
    print("Бот запущен.")
    bot.infinity_polling()
