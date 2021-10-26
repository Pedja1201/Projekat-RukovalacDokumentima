class Author:
    def __init__(self, first_name, last_name, email, web_page):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.web_page = web_page

    @property
    def first_name(self):
        return self.first_name
    
    @first_name.setter
    def firstname(self, value):
        self.first_name = value

    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, value):
        self.last_name = value
    
    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        self.email = value
    
    @property
    def web_page(self):
        return self.web_page

    @web_page.setter
    def web_page(self, value):
        self.web_page = value

    @property
    def name(self):
        return self.first_name + " " + self.last_name + " " + self.email + " " + self.web_page

    @name.setter
    def name(self, value):
        fl = value.split(" ")
        if len(fl) < 2:
            print("Nevalidno ime!")
            return
        self.first_name = fl[0]
        self.last_name = fl[1]