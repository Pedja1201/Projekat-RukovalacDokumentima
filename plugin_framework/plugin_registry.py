import os
import inspect
import importlib
import json
from plugin_framework.plugin_specification import PluginSpecification

# from plugin_framework.plugin_specification import PluginSpecification

class PluginRegistry:
    def __init__(self, plugins=[]):
        self.plugins = plugins
        self._plugins = plugins

    def install(self, plugins):
        # FIXME: ili dodati samo ako vec nije u komponentama
        self.plugins.append(plugins)

    def uninstall(self, plugins):
        # FIXME: sta ako nema te komponente u listi?
        self.plugins.remove(plugins)

    def activate(self, _id):
        for plugin in self._plugins: # plugin # naslednica od extension
            if _id == plugin.plugin_specification.id:
                plugin.activate()


    def deactivate(self, _id):
        for plugin in self._plugins: # plugin # naslednica od extension
            if _id == plugin.plugin_specification.id:
                plugin.deactivate()

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

