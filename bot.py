import os
import logging
import asyncio
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from aiohttp import web

from database import get_all_plants, get_plant_by_id, get_plants_by_category, get_categories

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Информационные разделы для главного меню
INFO_SECTIONS = {
    "digestive_system": {
        "title": "Общая информация о пищеварительной системе",
        "text": "🐹 **Пищеварительная система морской свинки**\n\n"
                "Морские свинки — травоядные животные с особой пищеварительной системой.\n\n"
                "📌 **Ключевые особенности:**\n"
                "• Желудок однокамерный, небольшой объём\n"
                "• Слепая кишка очень большая — в ней происходит ферментация клетчатки\n"
                "• Кишечник длинный, пища проходит быстро\n"
                "• Не могут синтезировать витамин С самостоятельно\n\n"
                "⚠️ **Важно:** Пищеварение работает только при постоянном поступлении пищи!",
        "image_url": "https://raw.githubusercontent.com/hvazdouski/plants/main/images/start.jpg"
    },
    "hay": {
        "title": "Сено - основа рациона",
        "text": "🌾 **Сено — основа рациона морской свинки**\n\n"
                "Сено должно составлять **80-90%** рациона и быть доступно **постоянно**!\n\n"
                "✅ **Почему сено так важно:**\n"
                "• Стачивает постоянно растущие зубы\n"
                "• Содержит необходимую клетчатку для пищеварения\n"
                "• Предотвращает ожирение\n"
                "• Даёт чувство сытости\n\n"
                "🥇 **Лучшее сено:** тимофеевка, овсяное, луговое\n"
                "❌ **Избегать:** пыльное, плесневелое, слишком зелёное",
        "image_url": "https://raw.githubusercontent.com/hvazdouski/plants/main/images/start.jpg"
    },
    "vitamin_c": {
        "title": "Почему витамин С особенно важен?",
        "text": "🍊 **Витамин С — жизненно необходим!**\n\n"
                "Морские свинки **не могут синтезировать витамин С** и должны получать его ежедневно!\n\n"
                "⚠️ **Признаки дефицита:**\n"
                "• Слабость, вялость\n"
                "• Опухшие суставы\n"
                "• Выпадение шерсти\n"
                "• Кровоточащие дёсны\n"
                "• В тяжёлых случаях — цинга\n\n"
                "💊 **Суточная норма:** 10-30 мг\n\n"
                "🥬 **Источники:** болгарский перец, свежая зелень, специальные добавки",
        "image_url": "https://raw.githubusercontent.com/hvazdouski/plants/main/images/start.jpg"
    },
    "feeding_rules": {
        "title": "Главные правила кормления",
        "text": "📋 **Главные правила кормления морской свинки**\n\n"
                "1️⃣ **Сено** — всегда в неограниченном количестве\n"
                "2️⃣ **Свежие овощи** — 1 стакан в день (разнообразные)\n"
                "3️⃣ **Вода** — чистая, свежая, всегда доступна\n"
                "4️⃣ **Гранулы** — 1-2 ст. ложки в день (не больше!)\n"
                "5️⃣ **Витамин С** — ежедневно\n\n"
                "❌ **Нельзя:** мясо, молочные продукты, сладости, хлеб\n"
                "⚠️ **Осторожно:** капуста, бобовые (вызывают газы)",
        "image_url": "https://raw.githubusercontent.com/hvazdouski/plants/main/images/start.jpg"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - приветствие и главное меню"""
    
    # Создаем клавиатуру с информационными разделами
    keyboard = [
        [InlineKeyboardButton("📚 Общая информация о пищеварительной системе", callback_data="info_digestive_system")],
        [InlineKeyboardButton("🌾 Сено - основа рациона", callback_data="info_hay")],
        [InlineKeyboardButton("🍊 Почему витамин С особенно важен?", callback_data="info_vitamin_c")],
        [InlineKeyboardButton("📋 Главные правила кормления морской свинки", callback_data="info_feeding_rules")],
        [InlineKeyboardButton("🌿 База растений", callback_data="plants_menu")]
    ]
    
    # Ссылка на изображение для приветствия
    start_image_url = "https://raw.githubusercontent.com/hvazdouski/plants/main/images/start.jpg"
    
    caption_text = (
        f"Привет, {update.effective_user.first_name}! 🐹\n\n"
        f"Я бот-справочник по уходу за морскими свинками.\n\n"
        f"Выберите раздел ниже:"
    )
    
    try:
        await update.message.reply_photo(
            photo=start_image_url,
            caption=caption_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.warning(f"Не удалось отправить фото в start: {e}")
        await update.message.reply_text(
            caption_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help - справка"""
    await update.message.reply_text("📚 **Команды:**\n/start - начать\n/plants - список растений\n/help - справка")

async def plants_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /plants - список всех растений по категориям"""
    categories = get_categories()
    
    # Создаем клавиатуру с категориями
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(f"🌿 {category.capitalize()}", callback_data=f"category_{category}")])
    
    await update.message.reply_text(
        "📂 **Выберите категорию:**\n\n" + 
        "\n".join(f"• {cat.capitalize()}" for cat in categories),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def plants_list_from_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'База растений' из главного меню (callback)"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    categories = get_categories()
    
    # Создаем клавиатуру с категориями
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(f"🌿 {category.capitalize()}", callback_data=f"category_{category}")])
    
    text = "📂 **Выберите категорию:**\n\n" + "\n".join(f"• {cat.capitalize()}" for cat in categories)
    
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_category_plants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать растения выбранной категории"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    # Извлекаем категорию из callback_data (формат: category_название)
    category = query.data.split('_', 1)[1]
    plants = get_plants_by_category(category)
    
    if not plants:
        await query.message.reply_text(f"В категории '{category}' нет растений.")
        return
    
    text = f"🌱 **Растения категории '{category.capitalize()}':**\n\n"
    text += "\n".join(f"{p['id']}. {p['name']}" for p in plants)
    
    keyboard = [[InlineKeyboardButton(p['name'], callback_data=f"plant_{p['id']}")] for p in plants]
    # Кнопка "Назад к категориям"
    keyboard.append([InlineKeyboardButton("⬅️ Назад к категориям", callback_data="back_to_categories")])
    
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вернуться к списку категорий"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    categories = get_categories()
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(f"🌿 {category.capitalize()}", callback_data=f"category_{category}")])
    
    text = "📂 **Выберите категорию:**\n\n" + "\n".join(f"• {cat.capitalize()}" for cat in categories)
    
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_info_section(update: Update, context: ContextTypes.DEFAULT_TYPE, section_key: str):
    """Показать информационный раздел с текстом и картинкой"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    if section_key not in INFO_SECTIONS:
        await query.message.reply_text("Раздел не найден.")
        return
    
    section = INFO_SECTIONS[section_key]
    text = section["text"]
    image_url = section["image_url"]
    
    # Кнопка "Назад в главное меню"
    keyboard = [[InlineKeyboardButton("⬅️ Назад в главное меню", callback_data="back_to_main")]]
    
    try:
        await query.message.reply_photo(
            photo=image_url,
            caption=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.warning(f"Не удалось отправить фото: {e}")
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вернуться в главное меню"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    # Создаем клавиатуру с информационными разделами
    keyboard = [
        [InlineKeyboardButton("📚 Общая информация о пищеварительной системе", callback_data="info_digestive_system")],
        [InlineKeyboardButton("🌾 Сено - основа рациона", callback_data="info_hay")],
        [InlineKeyboardButton("🍊 Почему витамин С особенно важен?", callback_data="info_vitamin_c")],
        [InlineKeyboardButton("📋 Главные правила кормления морской свинки", callback_data="info_feeding_rules")],
        [InlineKeyboardButton("🌿 База растений", callback_data="plants_menu")]
    ]
    
    caption_text = "🐹 **Главное меню**\n\nВыберите раздел:"
    
    # Пробуем отредактировать сообщение, если не получится - удаляем и отправляем новое
    try:
        await query.message.edit_text(caption_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        logger.warning(f"Не удалось отредактировать сообщение: {e}")
        # Если редактирование не удалось (например, сообщение с фото), удаляем и отправляем новое
        try:
            await query.message.delete()
        except Exception:
            pass
        await query.message.chat.send_text(
            caption_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок с информацией о растении и категориями"""
    query = update.callback_query
    
    # Обработка кнопки "Назад в главное меню"
    if query.data == "back_to_main":
        await back_to_main(update, context)
        return
    
    # Обработка кнопки "Назад к категориям" (База растений)
    if query.data == "back_to_categories":
        await back_to_categories(update, context)
        return
    
    # Обработка кнопки "База растений" из главного меню
    if query.data == "plants_menu":
        await plants_list_from_callback(update, context)
        return
    
    # Обработка информационных разделов
    if query.data.startswith("info_"):
        section_key = query.data.replace("info_", "")
        await show_info_section(update, context, section_key)
        return
    
    # Обработка выбора категории
    if query.data.startswith("category_"):
        await show_category_plants(update, context)
        return
    
    # Получаем ID растения (формат: plant_ID)
    if not query.data.startswith("plant_"):
        logger.warning(f"Неизвестный формат callback_data: {query.data}")
        return
        
    try:
        plant_id = int(query.data.split('_')[1])
    except (ValueError, IndexError) as e:
        logger.error(f"Ошибка разбора plant_id из {query.data}: {e}")
        return
    
    # Безопасный ответ на нажатие кнопки
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback (возможно, истекло время): {e}")
    
    plant = get_plant_by_id(plant_id)
    
    if not plant:
        try:
            await query.message.reply_text("Растение не найдено.")
        except Exception:
            pass # Игнорируем ошибки отправки, если сообщение уже устарело
        return
        
    name = plant.get('name', 'Без названия')
    description = plant.get('description', 'Описание отсутствует')
    care = plant.get('care', 'Уход не указан')
    
    response_text = f"🌿 **{name}**\n\n📝 {description}\n\n💧 {care}"
    
    if plant.get('image_url'):
        try:
            # Отправляем фото по прямой ссылке (Telegram сам скачает его)
            # Это обходит проблему 403 Forbidden при скачивании с нашей стороны
            await query.message.reply_photo(
                photo=plant['image_url'], 
                caption=response_text
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить фото по ссылке: {e}")
            await query.message.reply_text(response_text)
    else:
        await query.message.reply_text(response_text)

async def webhook_handler(request):
    """Обработчик входящих обновлений от Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, request.app['bot'])
        await request.app['application'].process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        logger.error(f"Ошибка в webhook_handler: {e}")
        return web.Response(text="Error", status=500)

async def post_init(app):
    """Настройка webhook после инициализации приложения"""
    webhook_url = app['webhook_url']
    await app['bot'].set_webhook(webhook_url)
    logger.info(f"Webhook установлен на: {webhook_url}")

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    port = int(os.environ.get('PORT', 8080))
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден!")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("plants", plants_list))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запускаем веб-сервер aiohttp вместе с приложением telegram
    async def run_bot():
        # Инициализируем бота
        await application.initialize()
        
        # Создаем веб-приложение
        app = web.Application()
        app['application'] = application
        app['bot'] = application.bot
        app['webhook_url'] = webhook_url
        
        app.router.add_post('/webhook', webhook_handler)
        
        # Устанавливаем webhook если URL предоставлен
        if webhook_url:
            await post_init(app)
        
        logger.info(f"Бот запущен на порту {port}")
        
        # Запускаем веб-сервер
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        
        # Держим приложение запущенным
        while True:
            await asyncio.sleep(3600)
    
    asyncio.run(run_bot())

if __name__ == '__main__':
    main()
