class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FlowGoLogger(metaclass=Singleton):
    def __init__(self):
        self._variables = []

    def add_variable(self, variable_name, position, value):
        entry_generated = False

        for current_entry in self._variables:
            if position == current_entry.get('position', None):
                current_entry[variable_name] = value
                entry_generated = True

            if entry_generated is True:
                break

        # add a new entry
        if entry_generated is False:
            self._variables.append({'position':position, variable_name:value})

    def write_values_to_file(self, filename):
        import csv

        if len(self._variables) > 0:
            with open(filename, 'w') as csvfile:
                fieldnames = self._variables[0].keys()

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for row in self._variables:
                    writer.writerow(row)

    def get_values(self, variable_name):
        generated_list = []

        for current_row in self._variables:
            generated_list.append(current_row.get(variable_name, None))

        return generated_list
