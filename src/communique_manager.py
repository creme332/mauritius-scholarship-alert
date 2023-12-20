
from __future__ import annotations
import json

from models.communique import Communique


class CommuniqueManager:
    def __init__(self, file_name="data/scrape.json"):
        self.file_name = file_name

    def get_last_communique(self) -> Communique | None:
        # ! file is guaranteed to contain at least an empty dictionary
        last_scraped_communique = None

        with open(self.file_name, 'r') as f:
            x = json.load(f)
            last_scraped_communique = Communique(
                x['title'], x['closing_date'], x['urls'])
            return last_scraped_communique

    def save(self, new_communique: Communique):
        """Saves the most recently scraped communique to `scrape.json`

        Args:
            new_communique (Communique): The most recently recently scraped
            communique
        """
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(new_communique.to_dict(), f,
                      ensure_ascii=False, indent=4)
