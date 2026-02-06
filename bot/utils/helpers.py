import matplotlib.pyplot as plt
from io import BytesIO
from datetime import date, timedelta
from aiogram.types import BufferedInputFile

from bot.database.session import async_session_maker
from bot.database.crud.summary import get_daily_summary


from bot.services.user_service import get_user_by_telegram_id


async def generate_progress_graph(telegram_id: int):
    async with async_session_maker() as session:
        user = await get_user_by_telegram_id(session, telegram_id)
        if not user:
            return None

        labels = []
        water_data = []
        calorie_data = []

        for i in range(6, -1, -1):
            day = date.today() - timedelta(days=i)
            labels.append(day.strftime("%d.%m"))

            summary = await get_daily_summary(session, user.id, day)

            water_data.append(summary["water_ml"])
            calorie_data.append(summary["net_calories"])

    fig, ax = plt.subplots(2, 1, figsize=(8, 8))

    ax[0].plot(labels, water_data, marker="o")
    ax[0].set_title("Прогресс воды за 7 дней")
    ax[0].set_ylabel("мл")
    ax[0].grid(True)

    ax[1].plot(labels, calorie_data, marker="o")
    ax[1].set_title("Баланс калорий")
    ax[1].set_ylabel("ккал")
    ax[1].grid(True)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()

    return BufferedInputFile(buf.getvalue(), filename="progress.png")
