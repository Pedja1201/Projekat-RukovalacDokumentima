from datetime import datetime


class ComponentSpecification:
    def __init__(self, version="1.0.0", app_version="1.0.0", author="Predrag Radak", description="", 
        creation_date=datetime.now(), last_update_date=datetime.now(), licence="", name="Component", 
        development_status="Unfinished"):
        self.version = version
        self.app_version = app_version
        self.author = author
        self.description = description
        self.creation_date = creation_date
        self.last_update_date = last_update_date
        self.licence = licence
        self.name = name
        self.development_status = development_status