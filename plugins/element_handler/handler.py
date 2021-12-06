class Handler():
    def __init__(self, widget, successor = None, input = None, parent = None):
        self.widget = widget
        self.parent = parent
        self.widget.parent = parent
        self.successor = successor
        self.input = input
        
    def handle(self):
        try:
            self.widget.handle()
        except:
            self.successor.handle()
