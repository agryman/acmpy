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