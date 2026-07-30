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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - приветствие и меню"""
    plants = get_all_plants()
    keyboard = [[InlineKeyboardButton(p['name'], callback_data=f"plant_{p['id']}")] for p in plants]
    
    # Ссылка на изображение для приветствия (можно заменить на свою)
    start_image_url = "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    
    caption_text = (
        f"Привет, {update.effective_user.first_name}! 🌿\n\n"
        f"Я бот-справочник по растениям.\n\n"
        f"/plants - список растений\n"
        f"/help - справка"
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

async def show_category_plants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать растения выбранной категории"""
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")
    
    category = query.data.split('_')[1]
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

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок с информацией о растении и категориями"""
    query = update.callback_query
    
    # Обработка кнопки "Назад к категориям"
    if query.data == "back_to_categories":
        await back_to_categories(update, context)
        return
    
    # Обработка выбора категории
    if query.data.startswith("category_"):
        await show_category_plants(update, context)
        return
    
    # Безопасный ответ на нажатие кнопки
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback (возможно, истекло время): {e}")
        # Если не удалось ответить, продолжаем работу, но игнорируем ошибку ответа
    
    plant_id = int(query.data.split('_')[1])
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
