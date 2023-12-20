import datetime


class Communique:
    def __init__(self, title: str = "", closing_date: str = "",
                 urls: list[str] = []):
        self.title = title  # main title as displayed on website
        self.closing_date = closing_date  # as displayed on website
        self.urls = urls  # all links available for current communique

        # save time at which object was created
        self.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                          format(datetime.datetime.now()))

    def to_dict(self):
        return vars(self)

    def to_list(self):
        return [self.title, self.closing_date, self.urls, self.timestamp]
