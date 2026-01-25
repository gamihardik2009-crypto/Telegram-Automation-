import time
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ========= CONFIG =========
CHANNEL_ID = "-3480265168"
TELEGRAM_URL = "https://web.telegram.org/k/"
SESSION_DIR = Path(__file__).parent / "telegram_session"

RANDOM_MESSAGES = [
    "Nice update",
    "Thanks for sharing",
    "Interesting post",
    "Good information",
    "Helpful post"
]

SCROLL_MESSAGE_INDEX = 8   # how old message to scroll to (bigger = more up)
# ==========================

options = Options()
options.add_argument(f"user-data-dir={SESSION_DIR}")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

try:
    # 1️⃣ Open Telegram
    print("⏳ Opening Telegram...")
    driver.get(TELEGRAM_URL)
    wait.until(EC.presence_of_element_located((By.ID, "column-center")))
    time.sleep(4)

    # 2️⃣ Open Channel
    print("⏳ Opening Channel...")
    driver.execute_script(f"""
        window.location.hash = '{CHANNEL_ID}';
        setTimeout(() => window.location.reload(), 800);
    """)
    time.sleep(6)

    wait.until(EC.presence_of_element_located((By.ID, "column-center")))
    print("✅ Channel Opened")

    # 3️⃣ FORCE scroll UP using message node (Telegram-safe)
    print("🔼 Scrolling up (message based)...")

    messages = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.message")
        )
    )

    if len(messages) > SCROLL_MESSAGE_INDEX:
        target_msg = messages[-SCROLL_MESSAGE_INDEX]
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            target_msg
        )
        time.sleep(3)
    else:
        print("⚠️ Not enough messages to scroll")

    # 4️⃣ Send ONE random message
    print("✉️ Sending message...")
    msg_box = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[contenteditable='true']")
        )
    )

    message = random.choice(RANDOM_MESSAGES)
    msg_box.click()
    time.sleep(0.5)
    msg_box.send_keys(message)
    time.sleep(0.5)
    msg_box.send_keys(Keys.ENTER)

    print(f"✅ Sent: {message}")
    time.sleep(5)

finally:
    driver.quit()
