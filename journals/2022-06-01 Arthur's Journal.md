# Arthur's Journal

## 2022-06-01

### 2:50 pm

Status:

* The Python code gives different results than the Maple code for basis type 1
* I am using a simplified version of Example-4-5 to debug
* I have created more test cases
* Goal: determine which function is producing the wrong results
* write more test cases:
  * compare results for basis type 2 (default) to type 1 (SHO) - DONE
  * write Maple code to export the results as CSV data files - DONE
  * update test cases to use newly generated data - TODO
  * look at pytest-allclose - DONE

break 6:20 pm

### 7:45 pm

* create testcases for all generated data - DONE

Status:

* Test cases pass for basis type = 2
* Test cases fail for basis type = 0, 1, 3
* In fact, the Python code always computes the expected result for basis type = 2, which is the default
* Therefore, there is something wrong with how the `glb_lam_fun` variable is being accessed from the `full_operators.py`
* Write a test case that sets and calls the `glb_lam_fun` variable
* The way I am importing `glb_lam_fun` is not working as I expect:

```text
PASSED            [  7%]before glb_lam_fun = <function lambda_acm_fun at 0x1292acb80>
Using the constant lambda basis.
after glb_lam_fun = <function lambda_acm_fun at 0x1292acb80>
FAILED            [ 10%]before glb_lam_fun = <function lambda_acm_fun at 0x1292acb80>
Using the constant lambda basis.
after glb_lam_fun = <function lambda_acm_fun at 0x1292acb80>
```

* Calling `ACM_set_basis_type()` DOES NOT change the value of `glb_lam_fun` that I import into another module!!!
* Fix: Define a wrapper function `ACM_eval_lambda_fun()` in the same module as `glb_lam_fun`. - DONE
* All tests now pass.
* Commit these fixes to current working branch. - DONE
* Resume verifying examples at Example 4.5 - TODO

break 10:40 pm

## 2022-06-02

### 11:40 am

* Resume verifying examples at Example 4.5 - TODO
* Example_4_5_d with smaller parameters now agrees with Maple but is much slower
* Parameters: `ACM_Adapt(RWC_ham, sqrt(B), 2.500, 0, 5, 0, 5, 0, 8)`
* Elapsed times for Example_4_5_d_050508:
  * Maple: 0.566s
  * Python: 8.241s
* Profile execution - TODO

break 12:15 pm

### 2:55 pm

* investigate performance problem - is this a regression?
  * No: Example_2_2_a and Example_2_2_b still run faster in Python
* Profile execution - IN-PROGRESS
  * the time is being spent in SymPy
  * convert to NumPy
  * merge current branch into master -> v1-1-5 - DONE
  * create new branch for NumPy changes -> improve_performance_section_4 - DONE
* convert to NumPy
* inspect and convert the following functions:
* RepXspace() - OK
* RepXspace_Term() - OK
* RepXspace_Prod() - convert
* RepXspace_Twin() - convert
* RepXspace_PiqPi() - convert
* RepXspace_PiPi() - convert
* RepXspace_Pi() - convert
* RepRadial_Prod_rem() - convert
* RepRadial_Prod_common() - convert
* RepRadial() - convert
* RepRadial_LC_rem() - convert
* RepRadial_LC_common() - convert
* RepRadial_bS_DS() - convert
* RepRadial_b2_sqrt() - convert
* RepRadial_param() - convert
* RepRadial_b2_sqrtInv() - convert
* RepRadialshfs_Prod() - convert
* KTSOp.representation() - convert
* KTOp.representation() - convert
* SOp.representation() - convert
* RepSO5r3_Prod_rem() - convert
* RepSO5r3_Prod_wrk() - convert
* RepSO5_Y_rem() - convert
* RepSO5_sqLdim() - convert
* RepSO5_sqLdiv() - convert

#### Conversion Strategy

* work top-down
* convert Matrix to NumPy in caller as required
* run mypy to detect type errors
* whenever the return type is changed, inspect all callers and remove redundant type conversions
* eliminate unnecessary SymPy operations such as simplify - assume all matrix elements are float
* RepXspace_Prod() - DONE
* RepXspace_Twin() - DONE
* RepXspace_PiqPi() - DONE
* RepXspace_PiPi() - DONE
* RepXspace_Pi() - DONE
* RepRadial_Prod_rem() - DONE
* RepRadial_Prod_common() - ...
* RepRadial() - convert
* RepRadial_LC_rem() - convert
* RepRadial_LC_common() - convert
* RepRadial_bS_DS() - convert
* RepRadial_b2_sqrt() - convert
* RepRadial_param() - convert
* RepRadial_b2_sqrtInv() - convert
* RepRadialshfs_Prod() - convert
* KTSOp.representation() - convert
* KTOp.representation() - convert
* SOp.representation() - convert
* RepSO5r3_Prod_rem() - convert
* RepSO5r3_Prod_wrk() - convert
* RepSO5_Y_rem() - convert
* RepSO5_sqLdim() - convert
* RepSO5_sqLdiv() - convert

break 6:10 pm

### 8:30 pm

* RepRadial_Prod_common() - DONE
* RepRadial_Prod() - DONE
* RepRadial() - DONE
* RepRadial_LC_rem() - DONE
* RepRadial_LC_common() - DONE
* RepRadial_bS_DS() - ...
  * tests break!!!
* RepRadial_b2_sqrt() - convert
* RepRadial_param() - convert
* RepRadial_b2_sqrtInv() - convert
* RepRadialshfs_Prod() - convert
* KTSOp.representation() - convert
* KTOp.representation() - convert
* SOp.representation() - convert
* RepSO5r3_Prod_rem() - convert
* RepSO5r3_Prod_wrk() - convert
* RepSO5_Y_rem() - convert
* RepSO5_sqLdim() - convert
* RepSO5_sqLdiv() - convert

Status: I converted RepRadial_bS_DS() but broke the tests.

```text
====================================================================== short test summary info ======================================================================
FAILED acmpy/tests/test_full_operators.py::TestRepXspace::test_example_4_5_basis_type[0] - assert False
FAILED acmpy/tests/test_full_operators.py::TestRepXspace::test_example_4_5_basis_type[1] - assert False
FAILED acmpy/tests/test_full_operators.py::TestRepXspace::test_example_4_5_basis_type[2] - assert False
FAILED acmpy/tests/test_full_operators.py::TestRepXspace::test_example_4_5_basis_type[3] - assert False
FAILED acmpy/tests/test_full_space.py::TestDigXspace::test_RWC_ham_fig5a - assert False
=================================================================== 5 failed, 644 passed in 8.95s ===================================================================
```

break 10:10 pm

## 2022-06-03

Resolve pytest failures -

* Inspect the test cases and determine the code involved
  * test_example_4_5_basis_type calls RepXspace() with the Hamiltonian from Example.4.1

```text
B: ClassVar[int] = 50
    c2: ClassVar[float] = 2.0
    c1: ClassVar[float] = 1 - 2 * c2
    chi: ClassVar[float] = 1.5
    kappa: ClassVar[float] = 1.0
```

* test_RWC_ham_fig5a calls DigXspace() with the Hamiltonian:

```text
B: int = 20
    c2: Expr = Rational(3, 2)
    c1: Expr = 1 - 2 * c2
    chi: Expr = S(2)
```

* debug the testcases, put breakpoint in `RepRadial_bS_DS()`
  * do they follow the same paths?
  * /test_full_operators.py::TestRepXspace::test_example_4_5_basis_type - calls `RepRadial_bS_DS()`
    * anorm = sqrt(50), lambdaa = 2.5, nu_min = 0, nu_max = 5
      * (K, R, T) = (0, 0, 2)
      * (K, R, T) = (-2, 0, 0)
      * (K, R, T) = (2, 0, 0)
      * (K, R, T) = (4, 0, 0)
      * (K, R, T) = (1, 3, 0)
      * (K, R, T) = (1, -3, 0)
  * /test_full_space.py::TestDigXspace::test_RWC_ham_fig5a
    * anorm = 4.47213595499958, lambdaa = 2.5, nu_min = 0, nu_max=5
      * KTR = 0, 0, 2
      * -2, 0, 0
      * 4, 0, 0
      * 1, 1, 0
      * 1, -1, 0
      * 0, 0, 2 lambdaa = 3.5
      * 0, 0, 2, 2.5
      * -2, 0, 0, 3.5
      * -2, 0, 0, 2.5
      * 2, 0, 0, 3.5
      * 2, 0, 0, 2.5
      * 4, 0, 0 3.5
      * 1, -1, 3.5
      * 1, 1, 0, 2.5
      * 0, 0, 2, 3.5
      * 0, 0, 2, 2.5
      * -2, 0, 0, 3.5
      * -2, 0, 0, 2.5
      * 4, 0, 0, 2.5
* Restore previous version of `RepRadial_bS_DS()` - does this resolve failures?
  * restored SymPy implementation as `RepRadial_bS_DS_sp()`
  * all tests pass
* Rename NumPy implementation to `RepRadial_bS_DS_np()`
* I visually inspected the two implementations
  * no obvious bugs
  * I suspect the *= and += operators may be doing something odd
    * replace with full expressions
* compare intermediate results for NumPy vs SymPy
  * where do they differ from the SymPy implementation?

This is a subtle bug. I was using the mutating assignment operators, e.g.

```text
Mat = RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)
                Mat *= (1 / anorm ** 2)
```

However, the function `RepRadial()` is cached.
Therefore, the cached value was modified so the next time the function
was called, an incorrect value would be returned.
Therefore, the code needs to take care that cached values are NEVER mutated!
Either, always copy the returned value, OR don't modify the returned value.

Committed bug fix.

Pause further conversion and focus on setting up laptop for demos.

break 1:30 pm

### 2:55 pm

Setup laptop. - IN-PROGRESS

* installing latest Xcode 13.4 - ...
* installing latest Xcode 13.4 Command Line Tools for brew -

Continue conversion to NumPy

* RepRadial_bS_DS() - DONE
* RepRadial_b2_sqrt() - DONE
* RepRadial_param() - DONE
* RepRadial_b2_sqrtInv() - DONE
* RepRadialshfs_Prod() - DONE
* KTSOp.representation() - DONE
* KTOp.representation() - DONE
* SOp.representation() - DONE
* RepSO5r3_Prod_rem() - DONE
* RepSO5r3_Prod_wrk() - DONE
* RepSO5r3_Prod() - DONE
* RepSO5_Y_rem() - DONE
* RepSO5_sqLdim() - DONE
* RepSO5_sqLdiv() - DONE

Measure performance of numpy implementation on Example 4.5 -

```text
============================== Begin: Example_4_5_d_050508 ==============================
Lowest eigenvalue is -23.29391. Relative eigenvalues follow (each divided by 0.03662):
  At L= 0: [   40.77,  117.51,  219.48,  302.71]
  At L= 2: [    6.00,   20.51,   62.00,   91.80]
  At L= 3: [   33.47,  210.26,  372.07,  519.59]
  At L= 4: [    4.12,   16.68,   37.53,   69.32]
  At L= 5: [    1.03,   19.16,  169.07,  190.48]
  At L= 6: [    1.17,   20.54,   48.83,  170.12]
  At L= 7: [    1.91,  169.02,  332.89,  491.09]
  At L= 8: [    0.00,   30.74,  170.33,  199.79]
Selected transition rates follow (each divided by 0.00002):
  B(E2: 2(1) -> 0(1)) =   100.00
  B(E2: 4(1) -> 2(1)) =    37.70
  B(E2: 6(1) -> 4(1)) =    42.59
  B(E2: 8(1) -> 6(1)) =   814.02
  B(E2: 2(2) -> 2(1)) =  7899.99
  B(E2: 4(2) -> 4(1)) =  1113.23
  B(E2: 4(3) -> 4(2)) =  3845.49
  B(E2: 4(4) -> 4(3)) =  2594.25
  B(E2: 6(2) -> 6(1)) =  2476.52
  B(E2: 6(3) -> 6(2)) =  1486.19
  B(E2: 6(4) -> 6(3)) =    16.05
Selected transition amplitudes follow (each divided by 0.00410):
  Amp( 2(1) -> 2(1) ) =    -4.77
elapsed process time = 7.965
============================== End:   Example_4_5_d_050508 ==============================
```

Previous time was 8.241s.

Profile code to determine where time is being spent. -

```text
/Users/arthurryman/Documents/repositories/agryman/acmpy/venv/bin/python "/Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5787.30/IntelliJ IDEA.app.plugins/python/helpers/pydev/pydevconsole.py" --mode=client --port=64773
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/Users/arthurryman/Documents/repositories/agryman/acmpy', '/Users/arthurryman/Documents/repositories/agryman/acmpy/src'])
Python 3.10.0 (default, Oct 13 2021, 06:44:31) [Clang 12.0.0 (clang-1200.0.32.29)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.3.0 -- An enhanced Interactive Python. Type '?' for help.
PyDev console: using IPython 8.3.0
Python 3.10.0 (default, Oct 13 2021, 06:44:31) [Clang 12.0.0 (clang-1200.0.32.29)] on darwin
runfile('/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/performance/profile_example.py', wdir='/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/performance')
Profiling: off
2 decimal places for each displayed value,
8 total digits for each displayed value,
except 5 decimal places for lowest (absolute) eigenvalue.
Eigenvalues displayed relative to minimal value.
Display lowest 6 eigenvalue(s) at each L.
Display lowest 4 rate/amplitude(s) in each list.
In ACM_Adapt, the scaling factor for relative eigenvalues is chosen such that
that for the 2(1) state is 6.000000
In ACM_Adapt, the scaling factor for "transition rates" is chosen such that
  B(E2: 2(1) -> 0(1)) = 100.000000
Display lowest 4 eigenvalue(s) at each L.
Display lowest 3 rate/amplitude(s) in each list.
7
1
Using the harmonic oscillator basis with lambda_v = lambda_0 + v.
<function lambda_sho_fun at 0x12b089240>
8
============================== Begin: Example_4_5_d_050508 ==============================
Lowest eigenvalue is -23.29391. Relative eigenvalues follow (each divided by 0.03662):
  At L= 0: [   40.77,  117.51,  219.48,  302.71]
  At L= 2: [    6.00,   20.51,   62.00,   91.80]
  At L= 3: [   33.47,  210.26,  372.07,  519.59]
  At L= 4: [    4.12,   16.68,   37.53,   69.32]
  At L= 5: [    1.03,   19.16,  169.07,  190.48]
  At L= 6: [    1.17,   20.54,   48.83,  170.12]
  At L= 7: [    1.91,  169.02,  332.89,  491.09]
  At L= 8: [    0.00,   30.74,  170.33,  199.79]
Selected transition rates follow (each divided by 0.00002):
  B(E2: 2(1) -> 0(1)) =   100.00
  B(E2: 4(1) -> 2(1)) =    37.70
  B(E2: 6(1) -> 4(1)) =    42.59
  B(E2: 8(1) -> 6(1)) =   814.02
  B(E2: 2(2) -> 2(1)) =  7899.99
  B(E2: 4(2) -> 4(1)) =  1113.23
  B(E2: 4(3) -> 4(2)) =  3845.49
  B(E2: 4(4) -> 4(3)) =  2594.25
  B(E2: 6(2) -> 6(1)) =  2476.52
  B(E2: 6(3) -> 6(2)) =  1486.19
  B(E2: 6(4) -> 6(3)) =    16.05
Selected transition amplitudes follow (each divided by 0.00410):
  Amp( 2(1) -> 2(1) ) =    -4.77
elapsed process time = 7.904
============================== End:   Example_4_5_d_050508 ==============================
Profiling: on
2 decimal places for each displayed value,
8 total digits for each displayed value,
except 5 decimal places for lowest (absolute) eigenvalue.
Eigenvalues displayed relative to minimal value.
Display lowest 6 eigenvalue(s) at each L.
Display lowest 4 rate/amplitude(s) in each list.
In ACM_Adapt, the scaling factor for relative eigenvalues is chosen such that
that for the 2(1) state is 6.000000
In ACM_Adapt, the scaling factor for "transition rates" is chosen such that
  B(E2: 2(1) -> 0(1)) = 100.000000
Display lowest 4 eigenvalue(s) at each L.
Display lowest 3 rate/amplitude(s) in each list.
7
1
Using the harmonic oscillator basis with lambda_v = lambda_0 + v.
<function lambda_sho_fun at 0x12b089240>
8
============================== Begin: Example_4_5_d_050508 ==============================
Lowest eigenvalue is -23.29391. Relative eigenvalues follow (each divided by 0.03662):
  At L= 0: [   40.77,  117.51,  219.48,  302.71]
  At L= 2: [    6.00,   20.51,   62.00,   91.80]
  At L= 3: [   33.47,  210.26,  372.07,  519.59]
  At L= 4: [    4.12,   16.68,   37.53,   69.32]
  At L= 5: [    1.03,   19.16,  169.07,  190.48]
  At L= 6: [    1.17,   20.54,   48.83,  170.12]
  At L= 7: [    1.91,  169.02,  332.89,  491.09]
  At L= 8: [    0.00,   30.74,  170.33,  199.79]
Selected transition rates follow (each divided by 0.00002):
  B(E2: 2(1) -> 0(1)) =   100.00
  B(E2: 4(1) -> 2(1)) =    37.70
  B(E2: 6(1) -> 4(1)) =    42.59
  B(E2: 8(1) -> 6(1)) =   814.02
  B(E2: 2(2) -> 2(1)) =  7899.99
  B(E2: 4(2) -> 4(1)) =  1113.23
  B(E2: 4(3) -> 4(2)) =  3845.49
  B(E2: 4(4) -> 4(3)) =  2594.25
  B(E2: 6(2) -> 6(1)) =  2476.52
  B(E2: 6(3) -> 6(2)) =  1486.19
  B(E2: 6(4) -> 6(3)) =    16.05
Selected transition amplitudes follow (each divided by 0.00410):
  Amp( 2(1) -> 2(1) ) =    -4.77
elapsed process time = 14.685
============================== End:   Example_4_5_d_050508 ==============================
Fri Jun  3 16:21:23 2022    Example_4_5_d_050508_stats
         24605294 function calls (23885934 primitive calls) in 13.169 seconds
   Ordered by: internal time
   List reduced from 1063 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   300896    0.732    0.000    1.696    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:293(__init__)
4449143/4439108    0.729    0.000    0.747    0.000 {built-in method builtins.isinstance}
640658/623600    0.681    0.000    1.583    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/sympify.py:92(sympify)
995445/964438    0.540    0.000    2.121    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/cache.py:69(wrapper)
301545/286463    0.462    0.000    1.248    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/expr.py:144(__eq__)
   352413    0.404    0.000    0.521    0.000 {built-in method builtins.__import__}
  1410010    0.275    0.000    0.331    0.000 {built-in method builtins.getattr}
   352413    0.238    0.000    0.759    0.000 /Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5787.30/IntelliJ IDEA.app.plugins/python/helpers/pydev/_pydev_bundle/pydev_import_hook.py:16(do_import)
   407475    0.213    0.000    0.977    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/sympify.py:479(_sympify)
     7678    0.204    0.000    0.490    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/facts.py:499(deduce_all_facts)
    15996    0.188    0.000    4.075    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:922(_gcd_terms)
   120584    0.187    0.000    0.830    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:817(__init__)
   331429    0.182    0.000    0.247    0.000 /usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/random.py:239(_randbelow_with_getrandbits)
41913/20510    0.168    0.000    0.996    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/expr.py:2186(extract_multiplicatively)
    35050    0.156    0.000    0.364    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/add.py:1051(primitive)
138371/137225    0.155    0.000    0.601    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:2210(__mul__)
   496412    0.143    0.000    0.197    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:2294(__hash__)
653149/623468    0.142    0.000    0.166    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/expr.py:126(__hash__)
    81566    0.140    0.000    0.940    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:460(mul)
173920/135726    0.137    0.000    0.928    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/decorators.py:88(__sympifyit_wrapper)
   565832    0.135    0.000    0.170    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/facts.py:533(<genexpr>)
17010/3015    0.132    0.000    0.791    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/simplify/powsimp.py:15(powsimp)
29237/5033    0.128    0.000    2.801    0.001 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:1224(do)
    20478    0.121    0.000    0.370    0.000 /usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/random.py:380(shuffle)
4322/3809    0.095    0.000    0.743    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/mul.py:178(flatten)
   821471    0.093    0.000    0.098    0.000 {method 'get' of 'dict' objects}
    15996    0.092    0.000    4.727    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/exprtools.py:987(gcd_terms)
102497/102338    0.092    0.000    1.240    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/decorators.py:254(_func)
144161/143985    0.091    0.000    0.322    0.000 {built-in method builtins.any}
24851/3876    0.091    0.000    0.956    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/assumptions.py:472(_ask)
```

The time must is probably being spent in the computation of the
matrix elements. These functions return floats but do the
calculation using SymPy.

## 2022-06-08

### 4:15 pm

I presented the code at the David Rowe Memorial Symposium on 2022-06-04.

Resume verifying the Maple Notebook examples and resolving performance problems.

* Compare `Example_4_5_d_050508`
  * Python: elapsed process time = 7.950
  * Maple: elapsed := 0.616

Note that Python outperforms Maple prior to Section 4.5.

Here is the Python profile:

```text
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(30)
Fri Jun  3 16:31:31 2022    Example_4_5_d_050508_stats
         24605294 function calls (23885934 primitive calls) in 13.169 seconds
   Ordered by: cumulative time
   List reduced from 1063 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   13.175   13.175 example.py:28(run)
        1    0.000    0.000   13.175   13.175 section_4.py:185(exec)
        1    0.000    0.000   13.175   13.175 full_space.py:1398(ACM_Adapt)
        1    0.000    0.000   13.175   13.175 full_space.py:1264(ACM_ScaleOrAdapt)
        9    0.001    0.000   13.159    1.462 full_operators.py:229(RepXspace)
       49    0.001    0.000   13.155    0.268 full_operators.py:268(RepXspace_Term)
       49    0.001    0.000   12.985    0.265 full_operators.py:401(RepXspace_Prod)
       49    0.005    0.000   12.973    0.265 full_operators.py:611(RepXspace_Twin)
        1    0.000    0.000   12.956   12.956 full_space.py:141(DigXspace)
      139    0.000    0.000   12.708    0.091 radial_space.py:1793(RepRadial_Prod_rem)
      139    0.001    0.000   12.708    0.091 radial_space.py:1707(RepRadial_Prod_common)
      139    0.001    0.000   12.686    0.091 radial_space.py:1549(RepRadialshfs_Prod)
 6742/542    0.062    0.000   12.031    0.022 simplify.py:411(simplify)
      297    0.004    0.000   11.966    0.040 matrices.py:924(_handle_creation_inputs)
      864    0.011    0.000   11.952    0.014 matrices.py:1126(<listcomp>)
      136    0.000    0.000   11.882    0.087 repmatrix.py:316(__new__)
      136    0.001    0.000   11.882    0.087 repmatrix.py:319(_new)
      122    0.000    0.000   11.796    0.097 radial_space.py:1443(representation)
      122    0.002    0.000   11.795    0.097 radial_space.py:1149(RepRadial_bS_DS)
       14    0.000    0.000   11.637    0.831 radial_space.py:794(RepRadial_param)
      504    0.001    0.000   11.531    0.023 radial_space.py:799(<lambda>)
      372    0.000    0.000   11.486    0.031 radial_space.py:574(MF_Radial_id_poly)
      372    0.002    0.000   11.485    0.031 radial_space.py:597(MF_Radial_id_pl)
      252    0.005    0.000    5.792    0.023 radial_space.py:508(ME_Radial_id_pl)
      252    0.005    0.000    5.738    0.023 radial_space.py:540(ME_Radial_id_ml)
    15996    0.092    0.000    4.727    0.000 exprtools.py:987(gcd_terms)
    15996    0.188    0.000    4.075    0.000 exprtools.py:922(_gcd_terms)
8257/3413    0.034    0.000    3.723    0.001 basic.py:1241(replace)
91881/3413    0.079    0.000    3.634    0.001 basic.py:1466(walk)
40788/2657    0.032    0.000    3.572    0.001 basic.py:1472(<listcomp>)
Out[8]: <pstats.Stats at 0x11387be20>
```

Why are there still calls to sympy Matrix?

```text
297    0.004    0.000   11.966    0.040 matrices.py:924(_handle_creation_inputs)
      864    0.011    0.000   11.952    0.014 matrices.py:1126(<listcomp>)
```

Note the matrix element functions:

```text
372    0.000    0.000   11.486    0.031 radial_space.py:574(MF_Radial_id_poly)
      372    0.002    0.000   11.485    0.031 radial_space.py:597(MF_Radial_id_pl)
      252    0.005    0.000    5.792    0.023 radial_space.py:508(ME_Radial_id_pl)
      252    0.005    0.000    5.738    0.023 radial_space.py:540(ME_Radial_id_ml)
```

Inspect code that still uses SymPy `Matrix`

* `internal_operators.py`
  * `RepSO5_Y_alg()` - not used
    `eigenvalues.py`
    * `Eigenvectors()` - not used
* `test_radial_space.py` - DONE
  * `test_KT000()` - DONE
  * `test_KT001()` - DONE
* `radial-space.py` - TODO
  * `RepRadial_LC()`
  * `RepRadial_param()`
  * `RepRadial_sq()`
  * `RepRadialshfs_Prod()`

break 6:05 pm

### 9:00 pm

* `radial-space.py` - IN-PROGRESS
  * `RepRadial_LC()` - not used
  * `RepRadial_sq()` - not used - DELETED
  * `RepRadial_param()` - used - DONE
    * This function was returning a Matrix instead of NDArrayFloat!!!
    * with this fix: elapsed process time = 7.868 (formerly 7.950)
  * `RepRadialshfs_Prod()` - used - DONE
    * with this fix: elapsed process time = 7.105 (formerly 7.868)

With the changes to `RepRadial_param()` and `RepRadialshfs_Prod()` there shouldn't be any calls to `Matrix` functions.

* profile the execution again

```text
Wed Jun  8 21:39:38 2022    Example_4_5_d_050508_stats
         22125825 function calls (21415660 primitive calls) in 12.089 seconds
   Ordered by: cumulative time
   List reduced from 961 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   12.096   12.096 example.py:28(run)
        1    0.000    0.000   12.095   12.095 section_4.py:185(exec)
        1    0.000    0.000   12.095   12.095 full_space.py:1398(ACM_Adapt)
        1    0.000    0.000   12.095   12.095 full_space.py:1264(ACM_ScaleOrAdapt)
        9    0.000    0.000   12.082    1.342 full_operators.py:229(RepXspace)
       49    0.001    0.000   12.080    0.247 full_operators.py:268(RepXspace_Term)
        1    0.000    0.000   11.981   11.981 full_space.py:141(DigXspace)
       49    0.001    0.000   11.903    0.243 full_operators.py:401(RepXspace_Prod)
       49    0.004    0.000   11.891    0.243 full_operators.py:611(RepXspace_Twin)
      139    0.000    0.000   11.749    0.085 radial_space.py:1767(RepRadial_Prod_rem)
      139    0.001    0.000   11.749    0.085 radial_space.py:1681(RepRadial_Prod_common)
      139    0.000    0.000   11.726    0.084 radial_space.py:1525(RepRadialshfs_Prod)
      122    0.000    0.000   11.726    0.096 radial_space.py:1419(representation)
      122    0.001    0.000   11.726    0.096 radial_space.py:1125(RepRadial_bS_DS)
       14    0.000    0.000   11.711    0.837 radial_space.py:793(RepRadial_param)
       14    0.000    0.000   11.711    0.836 radial_space.py:798(<listcomp>)
      372    0.000    0.000   11.664    0.031 radial_space.py:573(MF_Radial_id_poly)
      372    0.002    0.000   11.663    0.031 radial_space.py:596(MF_Radial_id_pl)
 1081/389    0.042    0.000   11.566    0.030 simplify.py:411(simplify)
      252    0.005    0.000    5.878    0.023 radial_space.py:507(ME_Radial_id_pl)
      252    0.005    0.000    5.832    0.023 radial_space.py:539(ME_Radial_id_ml)
    15996    0.093    0.000    4.784    0.000 exprtools.py:987(gcd_terms)
    15996    0.190    0.000    4.128    0.000 exprtools.py:922(_gcd_terms)
8257/3413    0.036    0.000    3.767    0.001 basic.py:1241(replace)
91881/3413    0.078    0.000    3.677    0.001 basic.py:1466(walk)
40788/2657    0.032    0.000    3.614    0.001 basic.py:1472(<listcomp>)
91881/77349    0.039    0.000    3.379    0.000 basic.py:1488(rec_replace)
     1468    0.001    0.000    3.250    0.002 basic.py:1456(<lambda>)
     3015    0.036    0.000    3.248    0.001 polytools.py:6644(cancel)
      692    0.002    0.000    3.240    0.005 simplify.py:614(<lambda>)
```

* no more calls to `Matrix` functions
* the most time-consuming SymPy call is `simplify()`

```text
1081/389    0.042    0.000   11.566    0.030 simplify.py:411(simplify)
```

This is probably caused by the calls to the `ME` and `MF` functions:

```text
372    0.000    0.000   11.664    0.031 radial_space.py:573(MF_Radial_id_poly)
      372    0.002    0.000   11.663    0.031 radial_space.py:596(MF_Radial_id_pl)
 1081/389    0.042    0.000   11.566    0.030 simplify.py:411(simplify)
      252    0.005    0.000    5.878    0.023 radial_space.py:507(ME_Radial_id_pl)
      252    0.005    0.000    5.832    0.023 radial_space.py:539(ME_Radial_id_ml)
```

* MF_Radial_id_poly
* MF_Radial_id_pl
* ME_Radial_id_pl
* ME_Radial_id_ml

Idea - Use OO design.

* Create an abstract base class that can compute the entire representation matrix.
* Define the default behaviour in the base class to:
  * iterate over the matrix entries and call the scalar function to return a float
  * the default scalar function calls the SymPy expression function and converts it to float
  * incrementally override the scalar functions with a native float version
  * incrementally override the matrix functions using vectorization (aka ufunc)

Pragmatic approach:

* use SciPy functions for gamma and binomial
* create separate SciPy version and compare results with SymPy version
* trace execution to see what values of arguments should be used
  * `MF_Radial_id_pl()` was called 260 times with lambdaa = lamvar
  * `MF_Radial_id_pl()` was called  60 times with lambdaa = 5.5
* understand why `lamvar` is used
  * perhaps we should use Pochhammer function instead of ratios of gamma functions
  * `ME_Radial_id_pl()` calls `MF_Radial_id_poly()` and then substitutes `lambdaa` for `lamvar`
  * `MF_Radial_id_poly()` calls `MF_Radial_id_pl()` with `lamvar`
* Compare the direct numeric evaluation with the symbolic simplification
  * created testcase `test_lamvar()` - no loss of accuracy using direct numeric evaluation
  * create version that uses SciPy `poch()` - TODO
    * create testcases - TODO

break 11:40 pm

## 2022-06-09

### 9:10 am

Rather than immediately going to SciPy `poch()` I may get a speedup by
using SymPy `RisingFactorial()` to replace the quotients of gamma functions.

- The testcases have sped up by 3 seconds

break 9:20 am

### 11:25 am

Measure performance.

* elapsed process time = 1.747 (formerly 7.105)!
  * Maple: elapsed := 0.616
  * Maple is now just 3x faster than Python
* very significant speedup using SymPy `RisingFactorial()` instead of `gamma()`

Profile execution.

```text
Thu Jun  9 11:30:47 2022    Example_4_5_d_050508_stats
         2561175 function calls (2474371 primitive calls) in 1.453 seconds
   Ordered by: cumulative time
   List reduced from 744 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.456    1.456 example.py:28(run)
        1    0.000    0.000    1.455    1.455 section_4.py:185(exec)
        1    0.000    0.000    1.455    1.455 full_space.py:1398(ACM_Adapt)
        1    0.000    0.000    1.455    1.455 full_space.py:1264(ACM_ScaleOrAdapt)
        9    0.000    0.000    1.442    0.160 full_operators.py:229(RepXspace)
       49    0.000    0.000    1.441    0.029 full_operators.py:268(RepXspace_Term)
        1    0.000    0.000    1.341    1.341 full_space.py:141(DigXspace)
       49    0.001    0.000    1.268    0.026 full_operators.py:401(RepXspace_Prod)
       49    0.003    0.000    1.256    0.026 full_operators.py:611(RepXspace_Twin)
      139    0.000    0.000    1.116    0.008 radial_space.py:1768(RepRadial_Prod_rem)
      139    0.001    0.000    1.115    0.008 radial_space.py:1682(RepRadial_Prod_common)
      139    0.000    0.000    1.093    0.008 radial_space.py:1526(RepRadialshfs_Prod)
      122    0.000    0.000    1.093    0.009 radial_space.py:1420(representation)
      122    0.001    0.000    1.092    0.009 radial_space.py:1126(RepRadial_bS_DS)
      389    0.005    0.000    1.091    0.003 simplify.py:411(simplify)
       14    0.000    0.000    1.078    0.077 radial_space.py:794(RepRadial_param)
       14    0.000    0.000    1.078    0.077 radial_space.py:799(<listcomp>)
      372    0.000    0.000    1.038    0.003 radial_space.py:573(MF_Radial_id_poly)
      372    0.002    0.000    1.037    0.003 radial_space.py:596(MF_Radial_id_pl)
      252    0.003    0.000    0.566    0.002 radial_space.py:507(ME_Radial_id_pl)
      252    0.003    0.000    0.511    0.002 radial_space.py:539(ME_Radial_id_ml)
104037/98643    0.068    0.000    0.375    0.000 cache.py:69(wrapper)
      183    0.003    0.000    0.245    0.001 polytools.py:6644(cancel)
12490/12440    0.013    0.000    0.237    0.000 decorators.py:254(_func)
      628    0.004    0.000    0.220    0.000 exprtools.py:987(gcd_terms)
      313    0.000    0.000    0.218    0.001 exprtools.py:1163(factor_terms)
 2153/313    0.009    0.000    0.218    0.001 exprtools.py:1224(do)
12490/12440    0.009    0.000    0.205    0.000 decorators.py:129(binary_op_wrapper)
   107/91    0.001    0.000    0.200    0.002 simplify.py:346(signsimp)
2272/2198    0.017    0.000    0.199    0.000 operations.py:46(__new__)
```

* significant time is spend in SymPy `simplify()` which is probably avoidable with loss of accuracy
* The `RepRadial` functions repeated calls to the `MF_Radial` and `ME_Radial` functions
  * these can be eliminated by using NumPy vectorized functions

Proceed with incremental OO redesign.

* create framework and wrap the SymPy matrix element functions
* create a new concrete class for each `ME` function passed into `RepRadial()` or `RepRadial_param()`
* inspect all usages of:

```text
RadialMatrixElementFunction = Callable[[float, Nu, Nu], float]
RadialMatrixElementParamFunction = Callable[[float, Nu, Nu, int], float]
```

break 12:15 pm

### 2:05 pm

Create `RadialOperator` class.

break 2:25 pm

### 6:05 pm

* ME_Radial_b_ml
* ME_Radial_b_pl
* ME_Radial_b2
* ME_Radial_bDb
* ME_Radial_bm_ml
* ME_Radial_bm_pl
* ME_Radial_bm2
* ME_Radial_D2b
* ME_Radial_Db_ml
* ME_Radial_Db_pl
* ME_Radial_id_pl
* ME_Radial_S0
* ME_Radial_Sm
* ME_Radial_Sp

break 6:30 pm

## 2022-06-10

### 3:00 pm

break 6:15 pm

## 2022-06-11

### 2:15 pm

Continue refactoring radial operators using OO design.

* ME_Radial_b_ml
* ME_Radial_b_pl
* ME_Radial_b2
* ME_Radial_bDb
* ME_Radial_bm_ml
* ME_Radial_bm_pl
* ME_Radial_bm2
* ME_Radial_D2b
* ME_Radial_Db_ml
* ME_Radial_Db_pl
* ME_Radial_id_pl
* ME_Radial_S0
* ME_Radial_Sm
* ME_Radial_Sp

The above abstraction is wrong.
The `ME` objects are not simply radial operators.
Rather, they are matrix elements of radial operators between
basis vectors belonging to bases that have different values of
the parameter $\lambda$.
The change in the value of $\lambda$ is an integer.

The generality allowed by the code is that for a given
calculation, all the bases share a pair of real, positive
parameters $(a, \lambda_0)$.

Investigate GitHub pages to simplify linking to references.
* review https://pages.github.com
* how is content from projects published on the account website? - TODO
* publish the symposium presentation - TODO
* publish the PDF references - TODO

break 5:55 pm

### 7:55 pm

Investigate GitHub pages to simplify linking to references.
* review https://pages.github.com - DONE
* how is content from projects published on the account website? - DONE
* publish the symposium presentation - TODO
* publish the PDF references - TODO

Create www folder for web content.