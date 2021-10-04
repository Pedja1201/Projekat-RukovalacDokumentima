import importlib
import inspect
import os


class ComponentFramework:
    def __init__(self, components=[]):
        self.components = components

    def add_component(self, component):
        # FIXME: ili dodati samo ako vec nije u komponentama
        self.components.append(component)

    def remove_component(self, component):
        # FIXME: sta ako nema te komponente u listi?
        self.components.remove(component)

    def install_components(self, path="plugins"):
        """
        Sve komponente nalaze u components folderu, svaka ima svoj zaseban folder, a unjemu
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
                            self.components.append(module)
        print("Broj ucitanih komponeniti:", len(self.components))