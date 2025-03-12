from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from pathlib import Path
import pandas as pd

from keyboards.default.menu import menu
from keyboards.inline.inlinekeyboards import scheduler, control_call
from data.config import GROUPS, ADMINS

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize scheduler globally
scheduler = AsyncIOScheduler()

# Paths
download_path = Path("downloads") / "fayllar"
download_path.mkdir(parents=True, exist_ok=True)
data_path = Path("data") / "jadval"
data_path.mkdir(parents=True, exist_ok=True)

# Load schedule from Excel
def load_schedule():
    """Load the schedule from the Excel file."""
    try:
        df = pd.read_excel(f"{data_path}/jadval.xlsx", index_col=0)
        df["sana"] = pd.to_datetime(df["sana"], dayfirst=True)
        return df
    except Exception as e:
        logging.error(f"Error loading Excel file: {e}")
        return None

# Send Daily Reminder
async def send_daily_reminder():
    df = load_schedule()
    
    if df is None:
        logging.error("No valid schedule found. Skipping reminder.")
        return

    # Compute tomorrow's date
    tomorrow_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    logging.info(f"Target reminder date: {tomorrow_date}")

     
    for index, row in df.iterrows():
        fish = row["FISH"]
        user_id = row["user_id"]
        sana = row["sana"].date()  # Extract the date part from the datetime
        if sana == tomorrow_date:
            try:
                chat_id = -1002430267801  # Group chat ID

                # Create the mention link
                mention_link = f"<a href='tg://user?id={user_id}'>{fish}</a>"

                # Send the reminder message to the group
                await bot.send_message(
                    int(GROUPS[1]), 
                    f"<i>Assalomu aleykum</i>\n"
                    f"🗓 {sana} sanasi kuni,\n"
                    f"🫡 <b>{mention_link}</b>aka navbatchilikka siz tayinlangansiz!\n"
                    f"Navbatchilikni yaxshi va tinch o'tkazib oling! 🤲",
                    parse_mode="HTML"
                )

                # Notify the admin that the message was sent
                await bot.send_message(ADMINS[0], f"Guruhga xabar muvaffaqiyatli yuborildi ✅\nErtangi navbatchi: {fish}")
                logging.info(f"Reminder sent for {fish} at {sana}")
            except Exception as e:
                logging.error(f"Error sending message for {fish} at {sana}: {e}")
                return

async def start_scheduler():
    soat = 5
    minut = 00
    scheduler.add_job(send_daily_reminder, "cron", hour=soat, minute=minut)
    scheduler.start()
    msg = f"Avtomatik eslatma: {soat} : {minut} ga o'rnatilgan!"
    await bot.send_message(chat_id=ADMINS[0],text=msg)
    logging.info(msg)
    
