class Communique(object):
    def __init__(self, title="", closingDate="",timestamp="", urls=[], keywords=[]):
        self.title = title # main title as displayed on website
        self.closingDate = closingDate # as displayed on website
        self.urls = urls # all links available for current communique
        self.keywords = keywords 
        self.timestamp = timestamp # time at which communique was scraped

    def to_dict(self):
        return vars(self)

    def __repr__(self):
        return (
            f"""City(
                name={self.name}, 
                country={self.country}, 
                population={self.population}, 
                capital={self.capital}, 
                regions={self.regions}
            )"""
        )
