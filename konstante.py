import os
from datetime import date, timedelta

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_value")
TODAY = date.today()
TOMOROW = date.today() + timedelta(days = 1)
MESEC_KASNIJE = date.today() + timedelta(days = 30)


gmail = 'miroslavzeljkovic@gmail.com'
mail_primalac = 'miroslav.zeljkovic@ems.rs'
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "default_value")

