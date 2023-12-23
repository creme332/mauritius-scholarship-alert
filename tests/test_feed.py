from src.feed import Feed
from src.models.communique import Communique
import pytest
import os

GENERATOR_FILE_PATH = "tests/data/feed.obj"
FEED_FILE_PATH = "tests/data/feed.xml"
DEFAULT_COMMUNIQUE = Communique("communique", "33 january", ["a.com"])


@pytest.fixture
def manager() -> Feed:
    # create required test files before test
    open(GENERATOR_FILE_PATH, 'a').close()
    open(FEED_FILE_PATH, 'a').close()

    # return valid initialized communique manager
    manager = Feed(GENERATOR_FILE_PATH, FEED_FILE_PATH)
    manager.reset()
    return manager


@pytest.fixture(autouse=True)
def clean_up():
    yield
    # after each test delete files
    if os.path.isfile(GENERATOR_FILE_PATH):
        os.remove(GENERATOR_FILE_PATH)

    if os.path.isfile(FEED_FILE_PATH):
        os.remove(FEED_FILE_PATH)


class TestFeed:
    def test_invalid_file_paths(self):
        with pytest.raises(FileNotFoundError):
            Feed("invalid.obj", "invalid.xml")

        with pytest.raises(FileNotFoundError):
            Feed(GENERATOR_FILE_PATH, "invalid.xml")

        with pytest.raises(FileNotFoundError):
            Feed("invalid.obj", FEED_FILE_PATH)

        with pytest.raises(FileNotFoundError):
            Feed(GENERATOR_FILE_PATH, FEED_FILE_PATH)

    def test_reset(self, manager: Feed):
        manager.reset()
        assert manager.get_total_feed_entries() == 0

    def test_get_total_feed_entries(self, manager: Feed):
        assert manager.get_total_feed_entries() == 0

        manager.add_entry(DEFAULT_COMMUNIQUE, "as")
        manager.add_entry(DEFAULT_COMMUNIQUE, "sds")

        assert manager.get_total_feed_entries() == 2

    def test_delete_old_entries(self, manager: Feed):
        assert manager.get_total_feed_entries() == 0

        for _ in range(0, 10):
            manager.add_entry(DEFAULT_COMMUNIQUE, "sds")

        manager.delete_old_entries(5)
        assert manager.get_total_feed_entries() == 5
