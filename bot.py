import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from aiohttp import web

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PLANTS_DB = [
    {
        'id': 1,
        'name': 'Алоэ Вера',
        'description': 'Суккулент с лекарственными свойствами.',
        'care': 'Полив раз в 2-3 недели, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Aloe_vera_%28L%29_Burman.jpg/440px-Aloe_vera_%28L%29_Burman.jpg'
    },
    {
        'id': 2,
        'name': 'Монстера',
        'description': 'Тропическое растение с большими листьями.',
        'care': 'Полив 1-2 раза в неделю, рассеянный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Monstera_deliciosa_leaf.jpg/440px-Monstera_deliciosa_leaf.jpg'
    },
    {
        'id': 3,
        'name': 'Фикус Бенджамина',
        'description': 'Популярное комнатное дерево.',
        'care': 'Полив 2-3 раза в неделю, яркий непрямой свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ficus_benjamina_02.jpg/440px-Ficus_benjamina_02.jpg'
    },
    {
        'id': 4,
        'name': 'Сансевиерия',
        'description': 'Неприхотливое растение "тещин язык".',
        'care': 'Полив раз в 2 недели, теневынослива',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Sansevieria_trifasciata_var._laurentii.jpg/440px-Sansevieria_trifasciata_var._laurentii.jpg'
    },
    {
        'id': 5,
        'name': 'Спатифиллум',
        'description': '"Женское счастье" с белыми цветами.',
        'care': 'Полив 2-3 раза в неделю, умеренный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Spathiphyllum_wallisii_flower.jpg/440px-Spathiphyllum_wallisii_flower.jpg'
    }
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = f"Привет, {update.effective_user.first_name}! 🌿\n\nЯ бот-справочник по растениям.\n\n/plants - список растений\n/help - справка"
    
    keyboard = [[InlineKeyboardButton(p['name'], callback_data=f"plant_{p['id']}")] for p in PLANTS_DB]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "📚 **Команды:**\n/start - начать\n/plants - список растений\n/help - справка"
    await update.message.reply_text(help_text)


async def plants_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🌱 **Список растений:**\n\n" + "\n".join(f"{p['id']}. {p['name']}" for p in PLANTS_DB)
    
    keyboard = [[InlineKeyboardButton(p['name'], callback_data=f"plant_{p['id']}")] for p in PLANTS_DB]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    plant_id = int(query.data.split('_')[1])
    plant = next((p for p in PLANTS_DB if p['id'] == plant_id), None)
    
    if plant:
        response_text = f"🌿 **{plant['name']}**\n\n📝 {plant['description']}\n\n💧 {plant['care']}"
        
        if plant.get('image_url'):
            try:
                await query.message.reply_photo(photo=plant['image_url'], caption=response_text)
            except Exception as e:
                logger.error(f"Ошибка фото: {e}")
                await query.message.reply_text(response_text)
        else:
            await query.message.reply_text(response_text)


async def webhook_handler(request):
    """Обработчик входящих обновлений от Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(text="OK") # Явно возвращаем OK
    except Exception as e:
        logger.error(f"Ошибка в webhook_handler: {e}")
        return web.Response(text="Error", status=500)


def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    port = int(os.environ.get('PORT', 8080))
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден!")
        return
    
    # Создаем приложение
    global application
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("plants", plants_list))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Настраиваем webhook при запуске
    webhook_url = os.environ.get('WEBHOOK_URL')
    if webhook_url:
        async def post_init(app):
            await app.bot.set_webhook(webhook_url)
            logger.info(f"Webhook установлен на: {webhook_url}")
        application.post_init = post_init
    
    # Запускаем веб-сервер aiohttp
    app = web.Application()
    app.router.add_post('/webhook', webhook_handler)
    
    logger.info(f"Бот запущен на порту {port}")
    web.run_app(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
