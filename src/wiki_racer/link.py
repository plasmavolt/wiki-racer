

class Link:
    def __init__(self, url, path):
        self.url = url # string
        self.path = path # list
    
    def __str__(self):
        str_path = ""
        for url in self.path:
            str_path += url + " --> "
        return str_path
        