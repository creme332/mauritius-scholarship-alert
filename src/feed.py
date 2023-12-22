from feedgen.feed import FeedGenerator
import pickle
import os.path
from models.communique import Communique
from bs4 import BeautifulSoup


class Feed:
    """
    A class for managing atom feed.

    Raises:
        FileNotFoundError: `feed.obj` file missing
        FileNotFoundError: `feed.xml` file missing
    """

    def __init__(self,
                 generator_file_path: str = "data/feed.obj",
                 feed_file_path: str = "frontend/feed.xml") -> None:
        self.xml_file_path = feed_file_path
        self.generator_file_path = generator_file_path
        self.feed_self_link = ('https://creme332.github.io/mauritius'
                               '-scholarship-alert/feed.xml')
        # define a global author for feed
        author_name = ('Ministry of Education, Tertiary Education,'
                       ' Science and Technology')
        self.feed_author = {'name': author_name, 'email': 'moeps@govmu.org'}

        # validate file paths
        if not os.path.isfile(self.generator_file_path):
            raise FileNotFoundError("feed.obj file missing")

        if not os.path.isfile(self.xml_file_path):
            raise FileNotFoundError("feed.xml file missing")

        self._load_generator()

    def reset(self) -> None:
        """
        Resets feed generator and feed file to their initial state.
        """
        # clear file contents
        open(self.generator_file_path, 'w').close()
        open(self.xml_file_path, 'w').close()

        # create a new feed generator
        self._init_new_generator()
        self._save_feed()

    def _init_new_generator(self) -> None:
        """
        Initializes a new feed generator.
        """

        self.fg = FeedGenerator()

        self.fg.id(
            'https://education.govmu.org/Pages/Downloads/Scholarships/'
            'Scholarships-for-Mauritius-Students.aspx')
        self.fg.title('Scholarships for Mauritius Students')
        self.fg.subtitle('A list of scholarships for Mauritian students')

        # define author as ministry of education
        self.fg.author(self.feed_author)

        # define myself as feed contributor
        self.fg.contributor(
            {"name": "creme332", "email": "c34560814@gmail.com"})

        # define link back to feed itself
        self.fg.link(
            href=self.feed_self_link,
            rel='self')

        # define language as english
        self.fg.language('en')

    def _load_generator(self) -> None:
        """
        Fetches generator object from file and saves it to
        class variable.
        """
        try:
            with open(self.generator_file_path, 'rb') as f:
                self.fg = pickle.load(f)
        except EOFError:
            # if no previous generator found, create a new one
            self._init_new_generator()

    def _save_generator(self) -> None:
        """
        Saves current state of generator to file.
        """
        with open(self.generator_file_path, 'wb') as f:
            pickle.dump(self.fg, f)

    def _save_feed(self) -> None:
        """
        Saves current atom feed to file.
        """
        # save atom feed to file
        self.fg.atom_file(self.xml_file_path, pretty=True)

    def get_total_feed_entries(self):
        """
        Returns the number of entries in the atom feed.

        Note: python-feedgen library does not have a method for getting
        the number of entries in feed.
        """
        with open(self.xml_file_path, 'r') as f:
            soup = BeautifulSoup(f, 'xml')

        return len(soup.find_all('entry'))

    def delete_old_entries(self, max_entry_count: int = 30) -> None:
        """
        Deletes old entries. This prevents files from becoming too large.

        Args:
            max_entry_count (int, optional): Max number of entries to
            keep after deletion. Defaults to 30.
        """
        assert (max_entry_count >= 0)
        total_entries = self.get_total_feed_entries()

        # count the number of entries to be deleted
        delete_count = total_entries - min(max_entry_count, total_entries)

        # starting from last entry,
        # delete until the required number of entries is deleted
        for i in range(0, delete_count):
            entry_index = total_entries - i - 1
            self.fg.remove_entry(entry_index)

        self._save_generator()
        self._save_feed()

    def add_entry(self, communique: Communique, pdf_text: str) -> None:
        """
        Adds a new entry to atom feed.

        Args:
            communique (Communique): Communique to be saved.
            pdf_text (_type_): _description_
        """
        # create entry object
        fe = self.fg.add_entry()

        # set required entries
        fe.id(communique.urls[0])
        fe.title(communique.title)
        # the feed <updated> attribute is automatically added

        # set some recommended elements
        fe.author(self.feed_author)

        # set summary
        summary = pdf_text.strip()[:250]+'...'
        fe.summary(summary)

        # save main file
        fe.link(
            {"href": communique.urls[0], "rel": "alternate",
             "type": "application/pdf"})

        # add other links present for communique
        for i in range(1, len(communique.urls)):
            fe.link(
                {"href": communique.urls[i],
                 "rel": "related",
                 "type": "application/pdf"})

        # update file state
        self._save_generator()
        self._save_feed()
