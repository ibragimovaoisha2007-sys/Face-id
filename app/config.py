from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hikvision Attendance"
    database_url: str = "postgresql+psycopg2://faceid:faceid@db:5432/faceid"
    redis_url: str = "redis://redis:6379/0"
    telegram_bot_token: str = ""
    telegram_admin_chat_id: int = 0
    hikvision_device_username: str = "admin"
    hikvision_device_password: str = "CHANGE_ME"
    hikvision_isapi_base_url: str = "http://DEVICE_IP"
    hikvision_event_token: str = "CHANGE_ME"
    allowed_device_ips: str = "127.0.0.1,10.0.0.0/8"
    late_after_time: str = "08:05"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
