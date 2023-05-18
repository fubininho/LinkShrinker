class Library:
    def __init__(self):
        self.links = []

    def insert(self, link):
        self.links.append(link)

    def list(self):
        return self.links

    def find_link(self, shortened_link):
        for link in self.links:
            if link.shortened_link == shortened_link:
                return link
        return None

    def delete_link(self, shortened_link):
        for link in self.links:
            if link.shortened_link == shortened_link:
                self.links.remove(link)
                return True
        return False

