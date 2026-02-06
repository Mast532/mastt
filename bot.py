import logging
import csv
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== НАСТРОЙКИ ====================
TOKEN = "8426954483:AAE79w8rvSI9AiLRbeGE1EjVCeAfPjJ4KeM"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Клавиатура с ПРОСТЫМ текстом (без эмодзи в начале)
reply_keyboard = [
    ["Цены и стоимость", "Контакты и связь"],
    ["Примеры работ", "Частые вопросы"]
]
KEYBOARD_MARKUP = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

# ==================== ФУНКЦИИ БОТА ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветствие и показывает кнопки."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {user_name}! 👋\nЯ бот для автоматизации бизнеса. Выберите действие ниже:",
        reply_markup=KEYBOARD_MARKUP
    )

def log_user_action(user, user_text: str):
    """Записывает обращение в файл leads.csv."""
    try:
        with open('leads.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Дата/Время', 'ID', 'Username', 'Имя', 'Сообщение'])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user.id,
                f"@{user.username}" if user.username else "Нет username",
                user.first_name or "Не указано",
                user_text[:200]
            ])
    except Exception as e:
        logger.error(f"Ошибка записи в CSV: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ВСЕ текстовые сообщения."""
    user = update.effective_user
    original_text = update.message.text  # Текст как есть
    
    # 1. ЛОГИРУЕМ ВСЁ для ясности
    logger.info(f"[DEBUG] Получено: '{original_text}'")
    
    # 2. СОХРАНЯЕМ в лог-файл
    log_user_action(user, original_text)
    
    # 3. ГЛАВНОЕ: Обработка кнопок через ТОЧНОЕ СРАВНЕНИЕ
    if original_text == "Цены и стоимость":
        answer = (
            "💰 *Цены на основные услуги:*\n\n"
            "• Базовый аудит + отчёт — 5 000 руб.\n"
            "• Настройка ИИ-воронки — 15 000 руб.\n"
            "• Создание Telegram-бота — от 10 000 руб.\n\n"
            "Точный расчёт после консультации. Напишите @Prost0_Yarik"
        )
    elif original_text == "Контакты и связь":
        answer = (
            "👨‍💼 *Контакты:*\n\n"
            "• Менеджер: @Prost0_Yarik\n"
            "• Email: aroslavmeserakov9@gmail.com\n"
            "• Отвечаем в Telegram в течение 5-15 минут."
        )
    elif original_text == "Примеры работ":
        answer = (
            "📁 *Примеры работ:*\n\n"
            "1. Бот для записи в стоматологию — -70% нагрузки на администратора\n"
            "2. Автоворонка для кофейни — +15% к повторным продажам\n"
            "3. Парсинг отзывов — анализ 1000+ отзывов в день\n\n"
            "Подробные кейсы по запросу."
        )
    elif original_text == "Частые вопросы":
        answer = (
            "❓ *Частые вопросы:*\n\n"
            "1. *Сроки?* — От 1 до 3 дней\n"
            "2. *Гарантия?* — 14 дней на исправление ошибок\n"
            "3. *Оплата?* — По реквизитам или ЮKassa"
        )
    else:
        # 4. Обработка ОСТАЛЬНЫХ сообщений (не кнопок) по ключевым словам
        text_lower = original_text.lower()
        
        if any(word in text_lower for word in ['привет', 'здравств', 'хай']):
            answer = "Здравствуйте! Выберите кнопку или задайте вопрос."
        elif any(word in text_lower for word in ['оплат', 'карт', 'сбер']):
            answer = "💳 Оплата по реквизитам (Сбер/Тинькофф) или через ЮKassa."
        else:
            # Стандартный ответ для всего остального
            answer = "Спасибо за ваше сообщение! 🤖\nЯ передал его менеджеру. Ответим вам в течение 15 минут."
    
    # 5. Отправляем ответ
    await update.message.reply_text(answer)
    logger.info(f"[DEBUG] Отправлен ответ на: '{original_text}'")

# ==================== ЗАПУСК БОТА ====================
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("=" * 60)
    logger.info("Бот запущен! Используется ТОЧНОЕ сравнение текста кнопок.")
    logger.info("Ожидаю нажатия кнопок: 'Цены и стоимость', 'Контакты и связь' и т.д.")
    logger.info("=" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()