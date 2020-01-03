# Copyright 2017 PyFLOWGO development team (Magdalena Oryaelle Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFLOWGO library.
#
# The PyFLOWGO library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The PyFLOWGO library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License
# along with the PyFLOWGO library.  If not, see https://www.gnu.org/licenses/.

import run_flowgo



if __name__ == "__main__":

    # -------------------------------------------------- RUN FLOWGO  ---------------------------------------------------

    #TODO: enter the json file you want to run

    path_to_folder = "./"
    json_file = path_to_folder + 'resource/template.json'

    # instanciate flowgo runner and run it
    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)



