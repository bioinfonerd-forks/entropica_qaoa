"""
Test that all the components of qaoa play nicely together
"""
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
import numpy as np
from scipy.optimize import minimize

from pyquil.paulis import PauliSum, PauliTerm
from pyquil.api import WavefunctionSimulator, local_qvm, get_qc

#from vqe.optimizer import scipy_optimizer
from entropica_qaoa.qaoa.cost_function import (QAOACostFunctionOnWFSim,
                                            QAOACostFunctionOnQVM)
from entropica_qaoa.qaoa.parameters import FourierParams


def test_qaoa_on_wfsim():
    # ham = PauliSum.from_compact_str("(-1.0)*Z0*Z1 + 0.8*Z0 + (-0.5)*Z1")
    term1 = PauliTerm("Z", 0, -1) * PauliTerm("Z", 1)
    term2 = PauliTerm("Z", 0, 0.8)
    term3 = PauliTerm("Z", 1, -0.5)
    ham = PauliSum([term1, term2, term3])

    params = FourierParams.linear_ramp_from_hamiltonian(ham, n_steps=10, q=2)
    p0 = params.raw()
    sim = WavefunctionSimulator()
    cost_fun = QAOACostFunctionOnWFSim(ham, params, sim,
                                       scalar_cost_function=True, nshots=100,
                                       noisy=True)
    with local_qvm():
        out = minimize(cost_fun, p0, tol=1e-3, method="Cobyla",
                       options={"maxiter": 500})
        wf = sim.wavefunction(cost_fun.prepare_ansatz,
                              memory_map=cost_fun.make_memory_map(params))
    assert np.allclose(out["fun"], -1.3, rtol=1.1)
    assert out["success"]
    assert np.allclose(wf.probabilities(), [0, 0, 0, 1], rtol=1.5, atol=0.05)
    print(out)


@pytest.mark.slow
def test_qaoa_on_qvm():
    # ham = PauliSum.from_compact_str("(-1.0)*Z0*Z1 + 0.8*Z0 + (-0.5)*Z1")
    term1 = PauliTerm("Z", 0, -1) * PauliTerm("Z", 1)
    term2 = PauliTerm("Z", 0, 0.8)
    term3 = PauliTerm("Z", 1, -0.5)
    ham = PauliSum([term1, term2, term3])
    params = FourierParams.linear_ramp_from_hamiltonian(ham,
                                                        n_steps=10,
                                                        q=2)
    p0 = params.raw()
    qvm = get_qc("2q-qvm")
    with local_qvm():
        cost_fun = QAOACostFunctionOnQVM(ham, params, qvm,
                                         scalar_cost_function=True, nshots=4,
                                         base_numshots=50)
        out = minimize(cost_fun, p0, tol=2e-1, method="Cobyla",
                       options={"maxiter": 100})
    assert np.allclose(out["fun"], -1.3, rtol=1.1)
    assert out["success"]
    print(out)
