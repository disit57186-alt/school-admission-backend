import os

class Config:
    SECRET_KEY = "CHANGE_THIS_SECRET"
    JWT_SECRET_KEY = "CHANGE_THIS_JWT_SECRET"

    MYSQL_HOST = "68.178.149.21"
    MYSQL_USER = "school_admin"
    MYSQL_PASSWORD = "davinci@2016"
    MYSQL_DB = "school_admission_app"

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day
