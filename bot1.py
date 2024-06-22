from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ConversationHandler, CallbackContext
import os
# Определение состояний беседы
CHOOSING_IPHONE, CHOOSING_MODEL, CHOOSING_MEMORY, REPAIR_STATUS, REPAIR_DETAILS, ORIGINAL_PARTS = range(6)
# Функция для пересылки сообщений администратору
async def forward_to_admin(update: Update, context: CallbackContext):
    admin_chat_id = '772222924'  
    user_message = update.message
    try:
        context.bot.forward_message(chat_id=admin_chat_id, from_chat_id=user_message.chat_id, message_id=user_message.message_id)
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")
# Функция для начала диалога
async def start(update: Update, context: CallbackContext) -> int:
    # Ваш код для обработки команды /start
    keyboard = [
        [InlineKeyboardButton("X", callback_data='X')],
        [InlineKeyboardButton("11", callback_data='11')],
        [InlineKeyboardButton("12", callback_data='12')],
        [InlineKeyboardButton("13", callback_data='13')], 
        [InlineKeyboardButton("14", callback_data='14')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите модель iPhone:', reply_markup=reply_markup)
    return CHOOSING_IPHONE

async def cancel(update: Update, context: CallbackContext) -> int:
    # Ваш код для обработки команды /cancel
    await update.message.reply_text('Операция отменена.')
    return ConversationHandler.END

# Функция для выбора модели iPhone
async def choose_model(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    iphone = query.data
    context.user_data['iphone'] = iphone
    models = {
        'X': ['X', 'XS', 'XS Max', 'XR'],
        '11': ['11', '11 Pro', '11 Pro Max'], 
        '12': ['12', 'Pro', 'Pro Max', 'mini'],
        '13': ['13', 'Pro', 'Pro Max', 'mini'],
        '14': ['14', 'Pro', 'Pro Max', 'plus'],
        # Добавьте модели для других версий iPhone
    }
    keyboard = [[InlineKeyboardButton(model, callback_data=model)] for model in models[iphone]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Какая модель iPhone {iphone}?", reply_markup=reply_markup)
    return CHOOSING_MODEL
# Функция для выбора объема памяти
async def choose_memory(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    model = query.data
    context.user_data['model'] = model 
    memories = {
        'X': ['64 GB', '128 GB', '256 GB', '512 GB'],
        '11': ['64 GB', '128 GB', '256 GB'],
        '12': ['64 GB', '128 GB', '256 GB'],
        '13': ['128 GB', '256 GB', '512 GB'],
        '14': ['128 GB', '256 GB', '512 GB'],'XS': ['64 GB', '256 GB', '512 GB'],
'11 Pro': ['64 GB', '256 GB', '512 GB'],
        '12 Pro': ['128 GB', '256 GB', '512 GB'], 
        '13 Pro': ['128 GB', '256 GB', '512 GB', '1 TB'],
        '14 Pro': ['128 GB', '256 GB', '512 GB', '1 TB'],
'XS Max': ['64 GB', '256 GB', '512 GB'],
'11 Pro Max': ['64 GB', '256 GB', '512 GB'],
        '12 Pro Max': ['128 GB', '256 GB', '512 GB'], 
        '13 Pro Max': ['128 GB', '256 GB', '512 GB', '1 TB'],
        '14 Pro Max': ['128 GB', '256 GB', '512 GB', '1 TB'],
'XR': ['128 GB'],
        '12 mini': ['128 GB', '256 GB'],
        '13 mini': ['256 GB', '512 GB'],
        '14 plus': ['256 GB', '512 GB']
        # Добавьте объемы памяти для других моделей
}
    memory_options = memories.get(model, [])
    keyboard = [[InlineKeyboardButton(memory, callback_data=memory)] for memory in memory_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Какой объем памяти у iPhone {model}?", reply_markup=reply_markup)
    return CHOOSING_MEMORY
# Функция для определения емкости аккумулятора
async def battery_capacity(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    # Сохранение предыдущего выбора пользователя
    context.user_data['repair'] = query.data
    keyboard = [
        [InlineKeyboardButton("100%-90%", callback_data='100%-90%')],
        [InlineKeyboardButton("89%-70%", callback_data='89%-70%')],
        [InlineKeyboardButton("69%-0%", callback_data='69%-0%')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Емкость аккумулятора:", reply_markup=reply_markup)
    return BATTERY_CAPACITY
# Функция для определения статуса ремонта
async def repair_status(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='yes')],
        [InlineKeyboardButton("Нет", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='Был ли ваш iPhone ранее в ремонте?', reply_markup=reply_markup)
    return REPAIR_DETAILS
# Переход к следующему состоянию
# Функция для определения деталей ремонта после ответа "Нет"
async def repair_details_no(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if query.data == 'no':
        return external_appearance(update, context)
# Переход к определению внешнего вида
    # Если ответ "Да", продолжаем с текущей логикой
    async def repair_details(update: Update, context: CallbackContext) -> int:
        pass
# Функция для определения внешнего вида
async def external_appearance(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Идеальное", callback_data='Идеальное')],
        [InlineKeyboardButton("Потертости/мелкие царапины", callback_data='Потертости')],
        [InlineKeyboardButton("Сколы/глубокие царапины/разбит", callback_data='Сколы')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Какое состояние экрана iPhone?", reply_markup=reply_markup)
    return SCREEN_CONDITION
# Функция для определения состояния задней панели
async def back_panel_condition(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    # Сохранение предыдущего выбора пользователя
    context.user_data['screen_condition'] = query.data
    keyboard = [
        [InlineKeyboardButton("Идеальное", callback_data='Идеальное')],
        [InlineKeyboardButton("Потертости/мелкие царапины", callback_data='Потертости')],
        [InlineKeyboardButton("Сколы/глубокие царапины/разбит", callback_data='Сколы')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Состояние задней панели:", reply_markup=reply_markup)
    return BACK_PANEL_CONDITION
# Функция для определения деталей ремонта
async def repair_details_yes(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Замена Экрана", callback_data='Экран')],
        [InlineKeyboardButton("Замена задней крышки", callback_data='Крышка')],
        [InlineKeyboardButton("Замена аккумулятора", callback_data='Аккумулятор')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Какой был ремонт?", reply_markup=reply_markup)
    return REPAIR_DETAILS_YES
# Функция для определения использования оригинальных запчастей
async def original_parts(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Оригинал", callback_data='Оригинал')],
        [InlineKeyboardButton("Не оригинал", callback_data='Не оригинал')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Использовались ли оригинальные запчасти при ремонте?", reply_markup=reply_markup)
    return ORIGINAL_PARTS
# Функция для расчета предложения цены
async def calculate_price_offer(user_data):
        # Ваши цены для различных моделей и объемов памяти
    base_prices = {
    ('X', '64 GB'): 10000,
    ('X', '256 GB'): 12000,
    ('11', '64 GB'): 14000,
    ('11', '128 GB'): 16000,
    ('11', '256 GB'): 18000,
    ('12', '64 GB'): 18000,
    ('12', '128 GB'): 20000,
    ('12', '256 GB'): 22000,
    ('13', '128 GB'): 22000,
    ('13', '256 GB'): 24000,
    ('13', '512 GB'): 26000,
    ('14', '128 GB'): 30000,
    ('14', '256 GB'): 32000,
    ('14', '512 GB'): 34000,
    ('XR', '128 GB'): 12000,
    ('12 mini', '128 GB'): 16000,
    ('12 mini', '256 GB'): 18000,
    ('13 mini', '256 GB'): 24000,
    ('13 mini', '512 GB'): 26000,
    ('14 plus', '256 GB'): 32000,
    ('14 plus', '512 GB'): 34000,
    ('XS', '64 GB'): 12000,
    ('XS', '256 GB'): 13000,
    ('XS', '512 GB'): 14000,
    ('11 Pro', '64 GB'): 13000,
    ('11 Pro', '256 GB'): 16000,
    ('11 Pro', '512 GB'): 18000,
    ('12 Pro', '128 GB'): 22000,
    ('12 Pro', '256 GB'): 24000,
    ('12 Pro', '512 GB'): 26000,
    ('13 Pro', '128 GB'): 30000,
    ('13 Pro', '256 GB'): 32000,
    ('13 Pro', '512 GB'): 36000,
    ('13 Pro', '1 TB'): 38000,
    ('14 Pro', '128 GB'): 40000,
    ('14 Pro', '256 GB'): 44000,
    ('14 Pro', '512 GB'): 46000,
    ('14 Pro', '1 TB'): 50000,
    ('XS Max', '64 GB'): 14000,
    ('XS Max', '256 GB'): 16000,
    ('XS Max', '512 GB'): 18000,
    ('11 Pro Max', '64 GB'): 20000,
    ('11 Pro Max', '256 GB'): 24000,
    ('11 Pro Max', '512 GB'): 28000,
    ('12 Pro Max', '128 GB'): 30000,
    ('12 Pro Max', '256 GB'): 34000,
    ('12 Pro Max', '512 GB'): 36000,
    ('13 Pro Max', '128 GB'): 40000,
    ('13 Pro Max', '256 GB'): 42000,
    ('13 Pro Max', '512 GB'): 46000,
    ('13 Pro Max', '1 TB'): 48000,
    ('14 Pro Max', '128 GB'): 50000,
    ('14 Pro Max', '256 GB'): 54000,
    ('14 Pro Max', '512 GB'): 56000,
    ('14 Pro Max', '1 TB'): 60000
    }
    base_price = base_prices.get((user_data.get('iphone'), user_data.get('memory')), 0)
    repair_cost = calculate_repair_cost(user_data)
    price_offer = base_price - repair_cost
    return price_offer

# Функция для определения стоимости ремонта
async def calculate_repair_cost(user_data) -> int:
    # Начальная стоимость ремонта
    base_cost = 5000
    # Получение данных из user_data
    screen_condition = user_data.get('screen_condition', 'Идеальное')
    back_panel_condition = user_data.get('back_panel_condition', 'Идеальное')
    repair_type = user_data.get('repair_type', 'Экран')
    original_parts = user_data.get('original_parts', 'Оригинал')
    # Стоимость в зависимости от состояния экрана
    if screen_condition == 'Потертости':
        base_cost *= 0.9
    elif screen_condition == 'Сколы':
        base_cost *= 0.5
    # Стоимость в зависимости от состояния задней панели
    if back_panel_condition == 'Потертости':
        base_cost *= 0.9
    elif back_panel_condition == 'Сколы':
        base_cost *= 0.5
    # Стоимость в зависимости от типа ремонта
    if repair_type == 'Экран':
        base_cost -= 3000  # Пример стоимости ремонта экрана
    elif repair_type == 'Крышка':
        base_cost -= 2000  # Пример стоимости ремонта крышки
    elif repair_type == 'Аккумулятор':
        base_cost -= 1500  # Пример стоимости замены аккумулятора
    # Дополнительная стоимость за использование оригинальных запчастей
    if original_parts == 'Не оригинал':
        base_cost *= 0.9  # Скидка 10%

    return base_cost

# Функция для завершения диалога и предложения цены
async def end(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    price_offer = calculate_price_offer(user_data)
    query = update.callback_query
    query.edit_message_text(text=f'Предложенная цена за ваш iPhone: {price_offer} рублей.')  
    return ConversationHandler.END

# Создание Updater и передача ему токена вашего бота
app = ApplicationBuilder().token('7389584259:AAEp7fcj3VA-87_og4JRu1tTs1xFPk8krTk').build()
# Добавление обработчика беседы в диспетчер
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start, pattern='^start$')],
    states={
        CHOOSING_IPHONE: [CallbackQueryHandler(choose_model)],
        CHOOSING_MODEL: [CallbackQueryHandler(choose_memory)],
        CHOOSING_MEMORY: [CallbackQueryHandler(repair_status)],
        REPAIR_STATUS: [CallbackQueryHandler(original_parts)],
        ORIGINAL_PARTS: [CallbackQueryHandler(end)],
        # Добавьте обработчики для других состояний
    },
    fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel$')],
    per_message=True
)

app.add_handler(conv_handler)


# Запуск бота
app.run_polling()


if __name__ == '__main__':
    main()


