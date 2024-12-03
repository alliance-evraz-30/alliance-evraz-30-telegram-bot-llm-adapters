from pathlib import Path
from telebot import TeleBot
from adapters.file_storage import save_file, generate_unique_file_name
from constants.excludes import excludes
from entryponts.entrypoint import runLLM


def process_zip_file(bot: TeleBot, file_id: str, file_name: str, chat_id: int) -> str:
    local_file_path = save_file(bot, file_id, generate_unique_file_name(chat_id, file_name))
    
    bot.send_message(chat_id, "Я отправил ваш проект на code-review. " +
                     "Это займет несколько минут. Пожалуйста, не беспокойте меня в это время. " + 
                     "Когда работа завершится, я отправлю вам результат в чат."
    )

    result = runLLM(local_file_path, excludes)
    print(result)

    return result

