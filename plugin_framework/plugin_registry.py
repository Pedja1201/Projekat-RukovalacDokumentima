import os
import inspect
import importlib
import json
from plugin_framework.plugin_specification import PluginSpecification


class PluginRegistry:
    def __init__(self, plugins=[]):
        self.plugins = plugins
        self._plugins = plugins
        # self._plugins = list()


    def get_by_name(self, name):
        """
        Vraca plugin koji ima naziv symbolic_name. Ukoliko se podesi da vise pluginova ima isti symbolic_name, vraca
        se samo prvi.

        :param symbolic_name: naziv spram kog pretrazujemo sve dostupne pluginove.
        :type symbolic_name: str
        :returns: Plugin -- pronadjeni plugin.
        :raises: IndexError -- ukoliko ne postoji ni jedan plugin koji je zadovoljio filter.
        """
        return list(filter(lambda x: x.name == name, self._plugins))[0]

    def install(self, plugins):
        # FIXME: ili dodati samo ako vec nije u komponentama
        exsists = self._check_existing_plugin(plugins.plugin_specification.id)
        if not exsists:
            # FIXME: nisu proverene zavisnosti
            self._plugins.append(plugins)

    def uninstall(self, plugins):
        # FIXME: sta ako nema te komponente u listi?
        self.deactivate(plugins.plugin_specification.id)
        self._plugins.remove(plugins)

    def activate(self, _id):
        for plugins in self._plugins: # plugin # naslednica od extension
            if _id == plugins.plugin_specification.id:
                plugins.activate()


    def deactivate(self, _id):
        for plugins in self._plugins: # plugin # naslednica od extension
            if _id == plugins.plugin_specification.id:
                plugins.deactivate()
    
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
                    if os.path.exists(main_module_path):
                        # Mozemo proveriti da li ima jednu klasu Main
                        module_path = main_module_path.rstrip(".py")
                        module_python_path = module_path.replace(os.path.sep, ".")
                        module = importlib.import_module(module_python_path)
                        class_members = inspect.getmembers(module, inspect.isclass)
                        has_main = False
                        for member in class_members:
                            if member[0] == "Main":
                                has_main = True
                                break
                        if has_main:
                            # TODO: dodati kao ucitani modul
                            self.plugins.append(module)
        print("Broj ucitanih plugina:", len(self.plugins))


    def _check_existing_plugin(self, _id):
        """
        Provera da li plugin sa id postoji u listi.
        """
        for plugin in self._plugins:
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

