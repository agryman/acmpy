"""This module contains examples from Section 1 of the Maple worksheet acm1.4a-examples.mw."""

from acmpy.examples.example import Example
from acmpy.globals import ACM_set_defaults, ACM_set_output, ACM_set_datum, ACM_set_listln, \
    ACM_set_eig_fit, ACM_set_rat_fit


class Example_1_2(Example):
    @classmethod
    def set(cls):
        ACM_set_defaults(0)
        ACM_set_output(2, 8, 5)
        ACM_set_datum(1)
        ACM_set_listln(6, 4)
        ACM_set_eig_fit(6.0, 2, 1)
        ACM_set_rat_fit(100.0, 2, 0, 1, 1)
