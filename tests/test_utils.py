from src.utils import clean_string


class TestCleanString:

    def test_empty_string(self):
        assert (clean_string("") == "")

    def test_string_with_leading_trailing_spaces(self):
        assert (clean_string("  hello world") == "hello world")

    def test_string_with_special_chars(self):
        assert (clean_string(
            "\xa0\n  hello\xa0world\r\n      \u200b") == "hello world")

    def test_string_with_special_apostrophe(self):
        assert clean_string(
            "IORA - MASTER’S SCHOLARSHIP") == "IORA - MASTER'S SCHOLARSHIP"
