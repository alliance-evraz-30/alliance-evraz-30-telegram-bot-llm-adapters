import time
from typing import Optional
from telebot import TeleBot
from adapters.file_storage import save_file, generate_unique_file_name, get_output_path


def process_zip_file(bot: TeleBot, file_id: str, file_name: str, chat_id: int) -> str:
    local_file_path = save_file(bot, file_id, generate_unique_file_name(chat_id, file_name))
    
    bot.send_message(chat_id, "Файл сохранен. Начинаем обработку...")

    pdf_path = simulate_pdf_creation(local_file_path)
    
    return pdf_path


def simulate_pdf_creation(input_zip_path: str) -> str:
    time.sleep(5) # for test

    output_pdf_path = get_output_path(input_zip_path, ".pdf")

    with open(output_pdf_path, "w") as pdf_file:
        pdf_file.write("Содержимое PDF файла.")
    return output_pdf_path
