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
  * merge current branch into master
  * create new branch for NumPy changes