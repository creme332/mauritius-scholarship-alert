
from __future__ import annotations
import json
from utils import clean_string
from models.communique import Communique
import os.path


class CommuniqueManager:
    def __init__(self, past_communique_filename="data/scrape.json",
                 interests_filename="data/interests.txt",
                 reminder_filename="data/reminders.txt"):
        """
        Initializes path to files.

        Args:
            past_communique_filename (str, optional): filename where last
            scraped communique is stored. Defaults to "data/scrape.json".
            interests_filename (str, optional): filename where user interests
            are defined. Defaults to "data/interests.txt".
            reminder_filename (str, optional): filename where user defined
            communiques with important deadlines.
            Defaults to "data/reminders.txt".
        """
        self.interests_filename = interests_filename
        self.past_communique_filename = past_communique_filename
        self.reminder_filename = reminder_filename

        # validate file names
        if (not os.path.isfile(self.past_communique_filename) or
                not os.path.isfile(self.interests_filename) or
                not os.path.isfile(self.reminder_filename)):
            raise FileNotFoundError

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

        with open(self.past_communique_filename, 'r') as f:
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

    def reset_last_communique(self) -> None:
        open(self.past_communique_filename, 'w').close()

    def save(self, new_communique: Communique):
        """Saves the most recently scraped communique to `scrape.json`

        Args:
            new_communique (Communique): The most recently recently scraped
            communique
        """
        with open(self.past_communique_filename, 'w', encoding='utf-8') as f:
            json.dump(new_communique.to_dict(), f,
                      ensure_ascii=False, indent=4)

    def get_new_communiques(
            self,
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
        last_scraped_communique = self.get_last_communique()

        # if last scraped communique does not exist, this means that
        # the website was scraped for the first time
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

    def get_user_interests(self) -> list[str]:
        """
        Returns a list of user interests in lowercase.

        Args:
            filename (str, optional): _description_.
            Defaults to 'data/interests.txt'.

        Returns:
            list[str]: _description_
        """
        interests = []
        with open(self.interests_filename, 'r') as f:
            for keyword in f:
                keyword = clean_string(keyword).lower()
                interests.append(keyword)
        return interests

    def get_reminder_settings(self) -> list[str]:
        """
        Get list of user-defined important communiques

        Returns:
            list[str]: list of user-defined communiques with
            important deadlines
        """
        user_reminders = []
        with open(self.reminder_filename, 'r') as f:
            for scholarship in f:
                user_reminders.append(clean_string(scholarship))
        return user_reminders
