import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import numpy as np

from pyquil.paulis import PauliSum, PauliTerm
from pyquil.gates import RX, RY, H, CNOT
from pyquil.quil import Program, QubitPlaceholder, MEASURE

from entropica_qaoa.vqe.measurelib import (append_measure_register,
                                        sampling_expectation_z_base,
                                        sampling_expectation)


# TODO make a more complicated test case and sure, that the test case is
# actually correct
def test_sampling_expecattion_z_base():
    bitstrings = np.array([[1,0], [0,1], [1,1], [1,1]])
    # ham = PauliSum.from_compact_str("1.0*Z0*Z1 + 0.5*Z0 + (-1)*Z1")
    term1 = PauliTerm("Z", 0) * PauliTerm("Z", 1)
    term2 = PauliTerm("Z", 0, 0.5)
    term3 = PauliTerm("Z", 1, -1)
    ham = PauliSum([term1, term2, term3])
    out = sampling_expectation_z_base(ham, bitstrings)
    assert np.allclose(out, (0.25, 0.946487243000456))


# TODO A more elaborate test?
def test_append_measure_register():
    q0 = QubitPlaceholder()
    p = Program(H(q0), RX(np.pi/2, 0))
    p = append_measure_register(p)
    assert str(p[-1]) == "MEASURE 0 ro[1]"


def test_sampling_expectation():
    bitstring1 = np.array([[1, 0], [0, 1], [1, 1], [1, 1]])
    bitstring2 = np.array([[1, 0], [0, 1], [1, 1], [1, 1]])
    bitstrings = [bitstring1, bitstring2]
    # ham1 = PauliSum.from_compact_str("1.0*Z0*Z1 + 0.5*Z0 + (-1)*Z1")
    # ham2 = PauliSum.from_compact_str("1.0*X0*Z1 + 0.5*X0 + (-1)*Z1")
    term1 = PauliTerm("Z", 0) * PauliTerm("Z", 1)
    term2 = PauliTerm("Z", 0, 0.5)
    term3 = PauliTerm("Z", 1, -1)
    term4 = PauliTerm("X", 0) * PauliTerm("Z", 1)
    term5 = PauliTerm("X", 0, 0.5)
    ham1 = PauliSum([term1, term2, term3])
    ham2 = PauliSum([term4, term5, term3])
    hams = [ham1, ham2]
    out = sampling_expectation(hams, bitstrings)
    assert np.allclose(out, (0.5, 1.3385315336840842))
