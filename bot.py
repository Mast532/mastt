import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== 1. НАСТРОЙКА ЛОГИРОВАНИЯ =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== 2. КОМАНДА /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для автоматизации.\n"
        f"Мой ID: {user.id}\n"
        "Отправь мне любое сообщение."
    )

# ===== 3. ОБРАБОТКА ЛЮБЫХ ТЕКСТОВЫХ СООБЩЕНИЙ =====
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    user = update.effective_user

    # Простая логика автоответа
    answer = f"Вы написали: {user_text}\nДлина: {len(user_text)} символов."
    await update.message.reply_text(answer)

    # Логирование в консоль (будет видно в логах Railway)
    logger.info(f"User {user.id} (@{user.username}) wrote: {user_text}")

# ===== 4. ГЛАВНАЯ ФУНКЦИЯ =====
def main() -> None:
    """Запуск бота."""
    # Способ 1 (рекомендуемый): Получение токена из переменной окружения Railway
    token = os.environ.get("8426954483:AAE79w8rvSI9AiLRbeGE1EjVCeAfPjJ4KeM")
    # Способ 2: Прямое указание токена в коде (менее безопасно, только для теста)
    # token = "8426954483:AAE79w8rvSI9AiLRbeGE1EjVCeAfPjJ4KeM"

    if not token:
        logger.error("Переменная окружения BOT_TOKEN не установлена!")
        raise ValueError("Установите переменную BOT_TOKEN в настройках Railway.")

    # Создание и настройка приложения
    application = Application.builder().token(token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота в режиме polling
    logger.info("Бот запущен и ожидает сообщений...")
    application.run_polling()

# ===== 5. ТОЧКА ВХОДА =====
if __name__ == '__main__':
    main()
