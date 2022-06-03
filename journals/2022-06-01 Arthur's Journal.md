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
