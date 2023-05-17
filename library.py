from link import Link

class Library:
    def __init__(self):
        self.links = []

    def insert(self, original_link, shortened_link):
        link = Link(original_link, shortened_link)
        self.links.append(link)

    def list(self):
        return self.links

