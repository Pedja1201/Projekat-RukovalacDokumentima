import os
import inspect
import importlib
import json
from plugin_framework.plugin_specification import PluginSpecification


class PluginRegistry:
    def __init__(self,iface, plugins=[]):
        self.iface = iface
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
        # FIXME: ili dodati samo ako vec nije u komponentama
        exsists = self._check_existing_plugin(plugin.plugin_specification.id)
        if not exsists:
            # FIXME: nisu proverene zavisnosti
            self.plugins.append(plugin)

    def uninstall(self, plugin):
        # FIXME: sta ako nema te komponente u listi?
        self.deactivate(plugin.plugin_specification.id)
        self.plugins.remove(plugin)

    def activate(self, _id):
        for plugin in self.plugins: # plugin # naslednica od extension
            if _id == plugin.plugin_specification.id:
                plugin.activate()


    def deactivate(self, _id):
        for plugin in self.plugins: # plugin # naslednica od extension
            if _id == plugin.plugin_specification.id:
                plugin.deactivate()
    
    # @property
    # def plugins(self):
    #     return self._plugins

    def install_plugins(self, path="plugins"):
        """
        Sve komponente nalaze u plugins folderu, svaka ima svoj zaseban folder, a unjemu
        obavezno main.py i spec.EXTENZIJA (bilo koji format datoteke)
        Dinamicko ucitavanje komponenti
        """
        for content in os.listdir(path):
            if content != "__init__.py":
                dir_path = os.path.join(path, content)
                if os.path.exists(os.path.join(dir_path, "__init__.py")):
                    # Ako postoji za njega znamo da je python paket
                    main_module_path = os.path.join(dir_path, "main.py")
                    spec_path = os.path.join(dir_path, "spec.json") # specifikacija svakog plugina ce se nalaziti
            # u ovoj dateoteci

                    data = {}
                    with open(spec_path) as fp:
                        data = json.load(fp)
                    specification = PluginSpecification.from_dict(data)
                    print(data, specification)
             
                    plugin = importlib.import_module(main_module_path.replace(os.path.sep, ".").rstrip(".py"))
                    class_members = inspect.getmembers(plugin, inspect.isclass)
                    print(class_members)
                    if len(class_members) == 1:
                        plugin = plugin.Extension(specification, self.iface) # unutar modula ce postojati tacno jedna klasa koju cemo
                        # zvati Plugin
                            # instalacija plugin-a
                        self.install(plugin)
                    else:
                        raise IndexError("The plugin.py module must contain just one class!")
        print("Broj ucitanih plugina:", len(self.plugins))


    def _check_existing_plugin(self, _id):
        """
        Provera da li plugin sa id postoji u listi.
        """
        for plugin in self.plugins:
            if plugin.plugin_specification.id == _id:
                return True
        return False









            # for root, dirs, files in os.walk(path):
            # for d in dirs:
            #     d_path = os.path.join(path, d)
            #     spec_path = os.path.join(d_path, "spec.json")
            #     plugin_path = os.path.join(d_path, "main").replace(os.path.sep,".")
            #     if os.path.exists(spec_path):
            #         with open(spec_path, "r") as fp:
            #             specification = json.load(fp)
            #             plugin_module = importlib.import_module(plugin_path)
            #             found = False
            #             for member in inspect.getmembers(plugin_module):
            #                 if member[0] == "Main":
            #                     inst = plugin_module.Main(specification)
            #                     print(inst)
            #                     found = True
            #                     self._plugins.append(inst)
            #             if not found:
            #                 raise ValueError("Main class not found!")
            # break # ne ulazimo u podfoldere

