from src.communique_manager import CommuniqueManager
from src.models.communique import Communique
import pytest
import os

SCRAPED_DATA_PATH = "tests/data/scrape.json"
INTEREST_DATA_PATH = "tests/data/interests.txt"
REMINDERS_DATA_PATH = "tests/data/reminders.txt"


@pytest.fixture
def manager():
    # create required test files
    open(SCRAPED_DATA_PATH, 'a').close()
    open(INTEREST_DATA_PATH, 'a').close()
    open(REMINDERS_DATA_PATH, 'a').close()

    # return valid communique manager
    return CommuniqueManager(
        SCRAPED_DATA_PATH,
        INTEREST_DATA_PATH,
        REMINDERS_DATA_PATH)


@pytest.fixture(autouse=True)
def test_cleanup():
    yield
    # after each test delete files
    if os.path.isfile(SCRAPED_DATA_PATH):
        os.remove(SCRAPED_DATA_PATH)

    if os.path.isfile(INTEREST_DATA_PATH):
        os.remove(INTEREST_DATA_PATH)

    if os.path.isfile(REMINDERS_DATA_PATH):
        os.remove(REMINDERS_DATA_PATH)


class TestCommuniqueManager:

    def test_invalid_file_names(self):
        with pytest.raises(FileNotFoundError):
            CommuniqueManager("/file.tx", "/ile.tx",
                              "/ile.tx")
        with pytest.raises(FileNotFoundError):
            CommuniqueManager("/ile.tx", INTEREST_DATA_PATH,
                              REMINDERS_DATA_PATH)

    def test_read_empty_scraped_file(self, manager: CommuniqueManager):
        # clear file contents
        open(SCRAPED_DATA_PATH, 'w').close()

        # attempt to read communique in it
        x = manager.get_last_communique()
        assert x is None

    def test_read_file_with_empty_dict(self, manager: CommuniqueManager):
        # write
        with open(SCRAPED_DATA_PATH, 'w') as f:
            f.write('{}')

        # attempt to read communique in it
        x = manager.get_last_communique()
        assert x is None

    def test_rw_normal_communique(self, manager: CommuniqueManager):
        write_communique = Communique("Communique test",
                                      "12 December 2023", ["a.com", "b.com"])
        # write communique
        manager.save(write_communique)

        # read communique
        read_communique = manager.get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_rw_communique_without_urls(self, manager: CommuniqueManager):
        write_communique = Communique("Communique test",
                                      "12 December 2023")
        # write communique
        manager.save(write_communique)

        # read communique
        read_communique = manager.get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_rw_empty_communique(self, manager: CommuniqueManager):
        write_communique = Communique()
        # write communique
        manager.save(write_communique)

        # read communique
        read_communique = manager.get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_get_new_communiques_when_scrape_empty(self,
                                                   manager: CommuniqueManager):
        """
        Test get_new_communiques() when last scraped communique is empty.
        Expected result is that no communiques are removed.
        """
        # clear file contents of last scraped communique
        open(SCRAPED_DATA_PATH, 'w').close()

        all_coms = ["com1", "com2"]
        result = manager.get_new_communiques(all_coms)
        assert set(all_coms) == set(result)

    @pytest.mark.parametrize("all_coms,expected_coms", [
        (['last'], []),
        (['com1', 'com2', 'last', 'com3', 'com4'], ['com1', 'com2']),
        (['com1', 'com2', 'last'], ['com1', 'com2']),
    ])
    def test_filter_for_nonempty_lsc(self, all_coms, expected_coms, manager):
        """
        Test filter_new() when last scraped communique is non-empty.
        Expected result is that all communiques including and
        after last communique are removed.
        """
        # write last communique to file
        last_scraped_communique = Communique("last")
        manager.save(last_scraped_communique)

        # create an array of communiques
        all_communique_array = [Communique(title) for title in all_coms]

        # filter out old communiques
        result = manager.get_new_communiques(
            all_communique_array)

        # get only titles from result
        result_titles = [c.title for c in result]

        assert set(result_titles) == set(expected_coms)

    def test_lst_missing_from_website(self, manager: CommuniqueManager):
        # write last communique to file
        last_scraped_communique = Communique("last")
        manager.save(last_scraped_communique)

        all_coms = ['com1', 'com2', 'com3']
        # create an array of communiques
        all_communique_array = [Communique(title) for title in all_coms]

        # filter out old communiques
        with pytest.raises(
                SystemExit,
                match="Last scraped communique is missing from website."):
            manager.get_new_communiques(
                all_communique_array)

    def test_read_empty_reminder_file(self, manager: CommuniqueManager):
        # clear file contents
        open(REMINDERS_DATA_PATH, 'w').close()

        assert len(manager.get_reminder_settings()) == 0

    def test_read_normal_reminder_file(self, manager: CommuniqueManager):
        reminders = ["com1", "com2", "COM3"]
        # save new settings to reminder
        with open(REMINDERS_DATA_PATH, "w") as f:
            f.write('\n'.join(reminders))

        result = manager.get_reminder_settings()
        assert set(result) == set(reminders)

    def test_read_empty_interests_file(self, manager: CommuniqueManager):
        # clear file contents
        open(INTEREST_DATA_PATH, 'w').close()

        assert len(manager.get_user_interests()) == 0

    def read_normal_interests_file(self, manager: CommuniqueManager):
        # clear file contents
        open(INTEREST_DATA_PATH, 'w').close()

        # add new interests
        interests = ["masters", "uk"]
        with open(REMINDERS_DATA_PATH, "w") as f:
            f.write('\n'.join(interests))

        result = manager.get_user_interests()
        assert set(result) == result(interests)
