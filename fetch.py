from seleniumbase import Driver
import time

driver = Driver(uc=True)
url = "https://www.bravopokerlive.com/venues/"
driver.uc_open_with_reconnect(url, 4)
driver.uc_gui_click_captcha()
time.sleep(20)
driver.quit()
