from typing import Tuple, Set


class Settings:
    PROJECT_NAME: str = "Theseus IHM"
    PROJECT_VERSION: str = "0.1.0"
    TERRAIN: str = "terrain.csv"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SATELLITES_ID: dict[str,str] = {
        "000ENSEATHESEUS202300000000001": "1_AIR_DAO",  # bleu
        "000ENSEATHESEUS202300000000002": "2_AIR_DAO",  # rouge
        "000ENSEATHESEUS202310000000002": "2_AIR_DAO",  # rouge
        "1581F67PB22B800307Z6": "SOU_AIR_DLR",  # DJI
        "1_TER_HERCULE": "1_TER_HERCULE",
        "2_TER_HERCULE": "2_TER_HERCULE",
        "1_TER_PETIT-POUCET": "1_TER_PETIT-POUCET",
        "2_TER_PETIT-POUCET": "2_TER_PETIT-POUCET",
        "SOU_TER_VAB": "SOU_TER_VAB",
    }
    SATELLITES: Set[str] = set(SATELLITES_ID.values())
    FRILEUSE: Tuple[Tuple, int] = ((48.8645, 1.89201), 16)
    ENSEA: Tuple[Tuple, int]  = ((49.039, 2.072), 18)
    HOME: Tuple[Tuple, int]  = ((49.18485, 2.412570), 20)
    ORIGIN: Tuple[Tuple, int]  = FRILEUSE


settings: Settings = Settings()
