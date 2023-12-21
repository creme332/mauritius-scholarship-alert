
from __future__ import annotations
import json

from models.communique import Communique


class CommuniqueManager:
    def __init__(self, file_name="data/scrape.json"):
        self.file_name = file_name

    def get_last_communique(self) -> Communique | None:
        """
        Returns the communique which was scraped the last time the program
        was run. This communique is saved in `data/scrape.json`.

        Returns:
            Communique | None: If scraping is now taking place for the
            first time, return None. Else return a Communique object.
        """
        # ! file is guaranteed to contain at least an empty dictionary
        last_scraped_communique = None

        with open(self.file_name, 'r') as f:
            try:
                x = json.load(f)
                # check if data is a non-empty dictionary before
                # converting to Communique
                if x:
                    last_scraped_communique = Communique(
                        x['title'], x['closing_date'], x['urls'])
                    return last_scraped_communique
                return None
            except json.decoder.JSONDecodeError:
                return None

    def save(self, new_communique: Communique):
        """Saves the most recently scraped communique to `scrape.json`

        Args:
            new_communique (Communique): The most recently recently scraped
            communique
        """
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(new_communique.to_dict(), f,
                      ensure_ascii=False, indent=4)

    def filter_new(self,
                   all_communiques: list[Communique]) -> list[Communique]:
        """
        Given a list of communiques scraped from top to bottom of website,
        return the communiques which were
        not encountered the last time the website was scraped.

        Args:
            all_communiques (list[Communique]): A list of communiques scraped
            from website. List is ordered by closing date since website is
            scraped from top to bottom.

        Returns:
            list[Communique]: New communiques discovered
        """
        new_communiques = []

        # read last scraped communique from file
        last_scraped_communique = self.get_last_communique()

        # if website is being scraped for the first time,
        # last_scraped_communique will be None so all scraped communiques
        # are new
        if not last_scraped_communique:
            return all_communiques

        # compare the last scraped communique with each communique
        # in all_communiques. keep only communiques which are found before
        # the last communique
        for communique in all_communiques:
            if communique.title == last_scraped_communique.title:
                return new_communiques
            new_communiques.append(communique)

        # if last scraped communique is not present on website,
        # there is a problem which requires manual verification
        raise SystemExit("Last scraped communique is missing from website.")
