from src.scraper.scraper import get_all_communiques


class TestScraper:
    def testPositiveLimit(self):
        x = get_all_communiques(2)
        assert len(x) == 2
