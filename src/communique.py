class Communique(object):
    def __init__(self, title="", closingDate="", timestamp="", urls=[]):
        self.title = title  # main title as displayed on website
        self.closingDate = closingDate  # as displayed on website
        self.urls = urls  # all links available for current communique
        self.timestamp = timestamp  # time at which communique was scraped

    def to_dict(self):
        return vars(self)

    def to_list(self):
        return [self.title, self.closingDate, self.urls, self.keywords,
                self.timestamp]
