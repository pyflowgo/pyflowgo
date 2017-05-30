import unittest
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_state

class MyTestCase(unittest.TestCase):

    def test_computes_relative_viscosity(self):
        relative_viscosity_model_er = pyflowgo.flowgo_relative_viscosity_model_er.FlowGoRelativeViscosityModelER()
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_er.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.45675270805, 10)

if __name__ == '__main__':
    unittest.main()


