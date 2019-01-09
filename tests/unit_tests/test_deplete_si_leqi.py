"""Regression tests for openmc.deplete.integrator.si_leqi algorithm.

These tests integrate a simple test problem described in dummy_geometry.py.
"""

from pytest import approx
import openmc.deplete

from tests import dummy_operator


def test_si_leqi(run_in_tmpdir):
    """Integral regression test of integrator algorithm using si_leqi"""

    op = dummy_operator.DummyOperator()
    op.output_dir = "test_integrator_regression"

    # Perform simulation using the si_leqi algorithm
    dt = [0.75, 0.75]
    power = 1.0
    openmc.deplete.si_leqi(op, dt, power, print_out=False)

    # Load the files
    res = openmc.deplete.ResultsList(op.output_dir / "depletion_results.h5")

    _, y1 = res.get_atoms("1", "1")
    _, y2 = res.get_atoms("1", "2")

    # Reference solution
    s1 = [2.03325094, 1.16826254]
    s2 = [2.92711288, 0.53753236]

    assert y1[1] == approx(s1[0])
    assert y2[1] == approx(s1[1])

    assert y1[2] == approx(s2[0])
    assert y2[2] == approx(s2[1])
