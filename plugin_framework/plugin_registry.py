import os
import inspect
import importlib
import json
from plugin_framework.plugin_specification import PluginSpecification


class PluginRegistry:
    def __init__(self, plugins=[]):
        self.plugins = plugins
        # self._plugins = list()


    def get_by_name(self, name):
        """
        Vraca plugin koji ima naziv name. Ukoliko se podesi da vise pluginova ima isti symbolic_name, vraca
        se samo prvi.

        :param name: naziv spram kog pretrazujemo sve dostupne pluginove.
        :type name: str
        :returns: Plugin -- pronadjeni plugin.
        :raises: IndexError -- ukoliko ne postoji ni jedan plugin koji je zadovoljio filter.
        """
        return list(filter(lambda x: x.name == name, self.plugins))[0]

    def install(self, plugin):
        """
        Dodaje plugin u instalirane. Isti plugin se ne moze dodati dva puta.

        :param plugin: instanca plugina kojeg dodajemo.
        :type plugin: Plugin
        :returns: bool -- podatak o uspesnosti dodavanja.
        """
        if plugin not in self.plugins:
            self.plugins.append(plugin)
            return True
        return False


    def uninstall(self, plugin):
        """
        Brise plugin u instalirane. Isti plugin se ne moze brisati dva puta.

        :param plugin: instanca plugina kojeg brisemo.
        :type plugin: Plugin
        :returns: bool -- podatak o uspesnosti brisanja.
        """
        if plugin in self.plugins:
            self.plugins.remove(plugin)
            return True
        return False

    def activate(self, plugin, value):
        if plugin in self.plugins:
            plugin.activate = value
            return True
        return False


    def deactivate(self, plugin, value):
        if plugin in self.plugins:
            plugin.deactivate = value
            return True
        return False
    
    # @property
    # def plugins(self):
    #     return self._plugins

    def install_plugins(self, path="plugins"):
        """
        Sve komponente nalaze u plugins folderu, svaka ima svoj zaseban folder, a unjemu
        obavezno main.py i spec.EXTENZIJA (bilo koji format datoteke)
        Dinamicko ucitavanje komponenti
        """
        #DONE: USpesno resen problem sa modulima i napravljena je instanca pluginova.
        for d in os.listdir(path):
            dir_path = os.path.join(path, d)
            if os.path.exists(os.path.join(dir_path, "__init__.py")):
                with open(os.path.join(dir_path, "spec.json"), "r") as fp:
                    spec = json.load(fp)
                    print(os.path.join(dir_path, "plugin"))
                    modul = importlib.import_module(os.path.join(dir_path, "main").replace(os.sep, "."))
                    obj = modul.Main(spec)
                    self.install(obj)

        print("Broj ucitanih plugina:", len(self.plugins))
        





