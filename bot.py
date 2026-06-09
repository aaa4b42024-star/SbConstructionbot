import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# បើកដំណើរការ Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8231478096:AAG5HIzX6iL5l5UpQbJNJmC-TjYxi4NAJ6g"

# ប៊ូតុងសម្រាប់ជម្រើសបន្ទាប់ពីគណនារួច
def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 គណនាផ្នែកផ្សេង", callback_data="main_menu")],
        [InlineKeyboardButton("📝 កែទិន្នន័យ", callback_data="re_input")]
    ])

# មុខងារគណនា
def calculate_material(l, w, h, count, type):
    volume = l * w * h * count
    bags = round(volume * 7, 2)
    cement_kg = round(bags * 50, 0)
    sand_m3 = round(volume * 0.45, 2)
    sand_kg = round(sand_m3 * 1500, 0)
    stone_m3 = round(volume * 0.9, 2)
    stone_kg = round(stone_m3 * 1600, 0)
    
    return (f"🏗️ *Sb Design & Decor*\n"
            f"📞 *ទូរស័ព្ទ:* 011 234 599 / 096 2 234 599\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📊 *ផ្នែក:* {type}\n\n"
            f"🧱 *បរិមាណបេតុង:* {round(volume, 2)} m³\n"
            f"🧪 *ស៊ីម៉ង់ត៍:* {bags} បេ ({int(cement_kg)} kg)\n"
            f"🏜️ *ខ្សាច់:* {sand_m3} m³ ({int(sand_kg)} kg)\n"
            f"🪨 *ថ្ម:* {stone_m3} m³ ({int(stone_kg)} kg)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"_បញ្ជាក់៖ លទ្ធផលនេះជាការប៉ាន់ប្រមាណ។_")

# ចាប់ផ្តើម Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # សម្អាតទិន្នន័យទាំងអស់មុនពេលចាប់ផ្តើម
    context.user_data.clear()
    
    keyboard = [
        [InlineKeyboardButton("ជើងតាំង", callback_data="ជើងតាំង")],
        [InlineKeyboardButton("សរសរ", callback_data="សរសរ")],
        [InlineKeyboardButton("ធ្នឹម", callback_data="ធ្នឹម")],
        [InlineKeyboardButton("ប្លង់សេ", callback_data="ប្លង់សេ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.reply_text("🏗️ សូមជ្រើសរើសផ្នែកដែលចង់គណនា៖", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🏗️ សូមជ្រើសរើសផ្នែកដែលចង់គណនា៖", reply_markup=reply_markup)

# គ្រប់គ្រងការចុចប៊ូតុង
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # លុបប៊ូតុងចេញពីសារចាស់រាល់ពេលចុច
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except:
        pass
    
    if query.data == "main_menu":
        # សម្អាតទិន្នន័យចាស់ទាំងស្រុង
        context.user_data.clear()
        await start(update, context)
        
    elif query.data == "re_input":
        prev = context.user_data.get('last_input', '1 1 0.5 1')
        await query.message.reply_text(f"📝 សូមបញ្ចូលលេខថ្មី (បណ្តោយ ទទឹង កម្ពស់ ចំនួន)៖\nច្បាប់ចម្លងទិន្នន័យចាស់៖ `{prev}`", parse_mode='Markdown')
        
    else:
        context.user_data['type'] = query.data
        await query.message.reply_text(
            f"📝 *ជ្រើសរើស៖* {query.data}\nសូមបញ្ចូលលេខ៖ បណ្តោយ ទទឹង កម្ពស់ ចំនួន\nឧទាហរណ៍៖ `1 1 0.5 4`", 
            parse_mode='Markdown'
        )

# គ្រប់គ្រងការវាយលេខ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input_text = update.message.text
        user_input = [float(x) for x in user_input_text.split()]
        
        if len(user_input) == 4:
            if 'type' not in context.user_data:
                await update.message.reply_text("⚠️ សូមជ្រើសរើសផ្នែកសិនតាមរយៈ /start")
                return
                
            l, w, h, count = user_input
            context.user_data['last_input'] = user_input_text
            res = calculate_material(l, w, h, count, context.user_data['type'])
            await update.message.reply_text(res, parse_mode='Markdown', reply_markup=get_main_menu_keyboard())
        else:
            await update.message.reply_text("❌ សូមបញ្ចូលលេខឱ្យបាន ៤ ខ្ទង់!")
    except:
        await update.message.reply_text("⚠️ បញ្ចូលតែលេខតាមទម្រង់៖ 1 1 0.5 4")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot កំពុងដំណើរការ...")
    # កែវាទៅជា៖
app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
