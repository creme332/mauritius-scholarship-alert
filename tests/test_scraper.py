from src.scraper.scraper import get_all_communiques
import pytest


# @pytest.mark.skip(reason="no need to repeatedly to make request to server")
class TestScraper:
    def test_default_limit(self):
        x = get_all_communiques()
        assert len(x) > 0

    def test_positive_limit(self):
        x = get_all_communiques(2)
        assert len(x) == 2

    def test_negative_limit(self):
        with pytest.raises(SystemExit, match="Invalid limit of communiques."):
            get_all_communiques(-1)
