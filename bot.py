import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# База данных растений (5 элементов)
PLANTS_DB = [
    {
        'id': 1,
        'name': 'Алоэ Вера',
        'description': 'Суккулент с лекарственными свойствами. Используется для лечения ожогов и проблем с кожей.',
        'care': 'Полив раз в 2-3 недели, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Aloe_vera_%28L%29_Burman.jpg/440px-Aloe_vera_%28L%29_Burman.jpg'
    },
    {
        'id': 2,
        'name': 'Монстера',
        'description': 'Тропическое растение с большими резными листьями. Отлично очищает воздух.',
        'care': 'Полив 1-2 раза в неделю, рассеянный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Monstera_deliciosa_leaf.jpg/440px-Monstera_deliciosa_leaf.jpg'
    },
    {
        'id': 3,
        'name': 'Фикус Бенджамина',
        'description': 'Популярное комнатное дерево. Символизирует гармонию и спокойствие.',
        'care': 'Полив 2-3 раза в неделю, яркий непрямой свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ficus_benjamina_02.jpg/440px-Ficus_benjamina_02.jpg'
    },
    {
        'id': 4,
        'name': 'Сансевиерия',
        'description': 'Неприхотливое растение, известное как "тещин язык". Выделяет кислород ночью.',
        'care': 'Полив раз в 2 недели, теневынослива',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Sansevieria_trifasciata_var._laurentii.jpg/440px-Sansevieria_trifasciata_var._laurentii.jpg'
    },
    {
        'id': 5,
        'name': 'Спатифиллум',
        'description': '"Женское счастье" - растение с белыми цветами. Увлажняет воздух.',
        'care': 'Полив 2-3 раза в неделю, умеренный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Spathiphyllum_wallisii_flower.jpg/440px-Spathiphyllum_wallisii_flower.jpg'
    }
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = (
        f"Привет, {update.effective_user.first_name}! 🌿\n\n"
        "Я бот-справочник по комнатным растениям.\n\n"
        "Доступные команды:\n"
        "/plants - показать список всех растений\n"
        "/help - справка по командам"
    )
    
    # Создаем клавиатуру со списком растений
    keyboard = []
    for plant in PLANTS_DB:
        keyboard.append([InlineKeyboardButton(plant['name'], callback_data=f"plant_{plant['id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "📚 **Справка по командам:**\n\n"
        "/start - начать работу с ботом\n"
        "/plants - показать список всех растений\n"
        "/help - эта справка\n\n"
        "Нажмите на название растения, чтобы узнать подробности!"
    )
    await update.message.reply_text(help_text)


async def plants_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать список всех растений"""
    text = "🌱 **Список растений:**\n\n"
    
    keyboard = []
    for plant in PLANTS_DB:
        text += f"{plant['id']}. {plant['name']}\n"
        keyboard.append([InlineKeyboardButton(plant['name'], callback_data=f"plant_{plant['id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID растения из callback_data
    plant_id = int(query.data.split('_')[1])
    
    # Ищем растение в базе
    plant = next((p for p in PLANTS_DB if p['id'] == plant_id), None)
    
    if plant:
        response_text = (
            f"🌿 **{plant['name']}**\n\n"
            f"📝 **Описание:**\n{plant['description']}\n\n"
            f"💧 **Уход:**\n{plant['care']}"
        )
        
        # Отправляем фото если есть URL
        if plant.get('image_url'):
            try:
                await query.message.reply_photo(
                    photo=plant['image_url'],
                    caption=response_text
                )
            except Exception as e:
                logger.error(f"Ошибка отправки фото: {e}")
                await query.message.reply_text(response_text)
        else:
            await query.message.reply_text(response_text)
    else:
        await query.message.reply_text("Растение не найдено 😕")


def main():
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.environ.get('plant_home_bot')
    
    if not token:
        logger.error("plant_home_bot не найден в переменных окружения!")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("plants", plants_list))
    
    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
