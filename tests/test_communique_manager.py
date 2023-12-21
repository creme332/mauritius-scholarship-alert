from src.communique_manager import CommuniqueManager
from src.models.communique import Communique
import pytest

DATA_PATH = "tests/data/scrape.json"


class TestCommuniqueManager:

    def test_invalid_file_path(self):
        with pytest.raises(FileNotFoundError):
            CommuniqueManager("invalid-path").get_last_communique()

    def test_read_empty_file(self):
        # clear file contents
        open(DATA_PATH, 'w').close()

        # attempt to read communique in it
        x = CommuniqueManager(DATA_PATH).get_last_communique()
        assert x is None

    def test_read_file_with_empty_dict(self):
        # write
        with open(DATA_PATH, 'w') as f:
            f.write('{}')

        # attempt to read communique in it
        x = CommuniqueManager(DATA_PATH).get_last_communique()
        assert x is None

    def test_rw_normal_communique(self):
        write_communique = Communique("Communique test",
                                      "12 December 2023", ["a.com", "b.com"])
        # write communique
        CommuniqueManager(DATA_PATH).save(write_communique)

        # read communique
        read_communique = CommuniqueManager(DATA_PATH).get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_rw_communique_without_urls(self):
        write_communique = Communique("Communique test",
                                      "12 December 2023")
        # write communique
        CommuniqueManager(DATA_PATH).save(write_communique)

        # read communique
        read_communique = CommuniqueManager(DATA_PATH).get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_rw_empty_communique(self):
        write_communique = Communique()
        # write communique
        CommuniqueManager(DATA_PATH).save(write_communique)

        # read communique
        read_communique = CommuniqueManager(DATA_PATH).get_last_communique()

        assert read_communique.to_dict() == write_communique.to_dict()

    def test_filter_for_empty_lsc(self):
        """
        Test filter_new() when last scraped communique is empty.
        Expected result is that no communiques are removed.
        """
        # clear file contents of last scraped communique
        open(DATA_PATH, 'w').close()

        all_coms = ['com1', 'com2', 'com3']
        result = CommuniqueManager(DATA_PATH).filter_new(
            all_coms)
        assert set(result) == set(all_coms)

        all_coms = []
        result = CommuniqueManager(DATA_PATH).filter_new(
            all_coms)
        assert set(result) == set(all_coms)

    @pytest.mark.parametrize("all_coms,expected_coms", [
        (['last'], []),
        (['com1', 'com2', 'last', 'com3', 'com4'], ['com1', 'com2']),
        (['com1', 'com2', 'last'], ['com1', 'com2']),
        (['com1', 'com2', 'com3'], ['com1', 'com2', 'com3']),

    ])
    def test_filter_for_nonempty_lsc(self, all_coms, expected_coms):
        """
        Test filter_new() when last scraped communique is non-empty.
        Expected result is that all communiques including and
        after last communique are removed.
        """
        # write last communique to file
        last_scraped_communique = Communique("last")
        CommuniqueManager(DATA_PATH).save(last_scraped_communique)

        # create an array of communiques
        all_communique_array = [Communique(title) for title in all_coms]

        # filter out old communiques
        result = CommuniqueManager(DATA_PATH).filter_new(
            all_communique_array)

        # get only titles from result
        result_titles = [c.title for c in result]

        assert set(result_titles) == set(expected_coms)
