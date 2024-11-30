import telebot
from telebot.types import Message
from services.process_file import process_zip_file

bot = telebot.TeleBot("8121352331:AAHoZPsN1c471o1_MV1vPGEVKMhT8g58Y_s")


@bot.message_handler(content_types=['document'])
def handle_document(message: Message) -> None:
    if message.document.file_name.endswith('.py'):
        bot.reply_to(message, "Вы отправили мне единственный файл." + 
                     "Напоминаю, что я занимаюсь решением архитектурных проблем." +
                     "Если проект слишком мал, архитектура не имеет значения — оставьте все как есть." +
                     "Если же весь проект помещен в один файл, то это не ошибка, а бедствие. Поверьте, его проще переписать, чем исправить.\n\n" +
                     "Пришлите zip-архив, когда будете готовы."
        )

        return

    if not message.document.file_name.endswith('.zip'):
        bot.reply_to(message, "Мои алгоритмы считают, что специализация — ключ к успеху." +
                     "Поэтому я работаю только с архитектурными проблемами и принимаю только Python-проекты. Спасибо за понимание!"
        )

        return

    bot.reply_to(message, "Я получил файл проекта. Спасибо!")

    try:
        result = process_zip_file(
            bot=bot,
            file_id=message.document.file_id,
            file_name=message.document.file_name,
            chat_id=message.chat.id,
        )

        bot.send_message(chat_id=message.chat.id, text=result, parse_mode="markdown")
        bot.send_message(
            chat_id=message.chat.id, 
            text="Code-review завершено! Спасибо, что обратились ко мне. Если потребуется помощь, дайте знать."
        )

        # with open(pdf_path, "rb") as pdf_file:
        #     bot.send_document(message.chat.id, pdf_file)
    except Exception as e:
        bot.reply_to(message, f"Ошибка обработки файла: {str(e)}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message) -> None:
        bot.reply_to(message, "Мои алгоритмы считают, что специализация — ключ к успеху." +
                     "Поэтому я работаю только с архитектурными проблемами и принимаю только Python-проекты. Спасибо за понимание!"
        )

@bot.message_handler(commands=['start'])
def start_message(message: Message) -> None:
    bot.reply_to(message, 
                 "👋 Привет!\n\n" +
                 "Я — дроид Альянса. Моя задача — найти архитектурные ошибки в вашем проекте и помочь их исправить. " +
                 "Я не пишу код за вас, не отслеживаю мелкие нарушения и не являюсь линтером. Вместо этого я анализирую проект" +
                 "комплексно и помогаю избежать фундаментальных проблем.\n\n" +
                 "Я был создан специально для хакатона Евраза, поэтому полагаюсь на следующие вводные:\n" +
                 "— Проект написан на Python\n" +
                 "— В проекте используется гексагональная архитектура" +
                 "\n— Проект приходит в формате zip-архива"
    )

@bot.message_handler(func=lambda message: True)
def unknown_command(message: Message) -> None:
    bot.reply_to(message, "Извините, но я не обрабатываю эту команду." +
                 "Пожалуйста, отправьте архив с Python-проектом, чтобы я мог сделать" +
                 "code-review, или введите /start, чтобы увидеть приветственное сообщение."
    )

if __name__ == "__main__":
    print("Бот запущен.")
    bot.infinity_polling()
