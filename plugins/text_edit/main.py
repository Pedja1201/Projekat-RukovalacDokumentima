import json
from datetime import datetime
from plugin_framework.component import Component
from plugin_framework.component_specification import ComponentSpecification

class Main(Component):
    def __init__(self, actions, menu, toolbar, widget, specification):
        super().__init__(actions, menu, toolbar, widget, specification)
        if self.specification is None:
            self._load_specification("plugins/text_edit/spec.json")

    # TODO: dodati metode specificne za komponentu
    def _load_specification(self, path):
        # FIXME: sta ako putanja ne postoji (nedostaje datoteka) os.path.exists
        with open(path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            self.specification = ComponentSpecification(data["version"], data["app_version"], data["author"],
                data["description"], datetime.strptime(data["creation_date"]), datetime.strptime(data["last_update_date"]),
                data["licence"], data["name"], data["development_status"])

