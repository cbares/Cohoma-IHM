class Settings:
    PROJECT_NAME: str = "Theseus IHM"
    PROJECT_VERSION: str = "0.1.0"
    TERRAIN: str = "terrain.csv"
    DATABASE_URL: str = "sqlite:///./sql_app.db"


settings: Settings = Settings()
