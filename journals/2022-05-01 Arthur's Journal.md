# Arthur's Journal

## 2022-05-01

### 10:40 am

Status:
* I am in the process of replacing the use of SymPy 'Matrix' operations with NumPy
* There are two main issues I need to resolve:
  * Two functions take a `Matrix` and are cached: `Matrix_sqrt` and `Matrix_sqrtInv`
    * I had to replace `Matrix` with `ImmutableMatrix` for this to work because all arguments must be `Hashable`
    * NumPy does not provide immutable arrays, but does this matter?
    * create a test case that passes a NumPy array to a cached function - DONE
  * The `Matrix` objects are normally converted to floats
    * However, the matrix elements are computed analytically and returned as SymPy `Expr` objects
    * Is the use of symbolic matrix elements beneficial of numerical accuracy?
    * create a test case to determine if accuracy is reduced by always converting matrix elements to `float` - TODO
* The IDE produces type warnings when matrix element functions are passed as arguments to functions
  * Should I create an abstract base class or define a protocol for these functions? - TODO

Create test case that passes a NumPy array to a cached function. - DONE
* The test fails with the error: `TypeError: unhashable type: 'numpy.ndarray'`
* `mypy` does not report a type error
* the IDE does not report a type error or warning

I wonder if these functions really need to be cached.
What is the likelihood of a cache hit?
Would it make more sense to wrap the computations that call these functions as cached so that
only a few immutable parameters are used in the key?
* inspect the code where these functions are called and see if I can lift the caching to a higher level - IN-PROGRESS
  * yes, `Matrix_sqrt` and `Matrix_sqrtInv` are only used with `RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)`
  * create two new functions and move caching there:
    * `RepRadial_b2_sqrt` 
    * `RepRadial_b2_sqrtInv`
  * create test cases for `RepRadial_bS_DS` that call the above functions
  * create test cases for `RepRadial(ME_Radial_b2, lambda, nu_min, nu_max)`
  * Note that if `lambda` is a float then the matrix contains floats
  * Is there any significance to allowing `lambda` to be algebraic?
  * There is a significance to the difference between `lambda`'s between radial spaces being integral
    * In this case, the parity of the difference is significant

break 12:20 pm

### 2:40 pm

Test cases for `RepRadial_bS_DS`:

|K    |T    | R      |Calls        |
|---  |---  |--------|---          |
|0    |0    |odd < 0 |Matrix_sqrt  |
|0    |0    |odd >= 0 |Matrix_sqrt  |
|K    |T    |even     |Matrix_sqrt  |
|K    |T    |even     |Matrix_sqrtInv|

I created and tested the new functions `RepRadial_b2_sqrt` and `RepRadial_b2_sqrtInv`
* replace direct calls to `Matrix_sqrt` and `Matrix_sqrtInv` - DONE
* retest - DONE
* remove cache attribute from `Matrix_sqrt` and `Matrix_sqrtInv` - DONE
* back out use of `ImmutableMatrix` from `Matrix_sqrt` and `Matrix_sqrtInv` - DONE
* replace cache clear calls -DONE
* retest - DONE
* change interface of `Matrix_sqrt` and `Matrix_sqrtInv` to return NumPy arrays - DONE
* retest - DONE

I suspect that the next source of performance improvement is to change the computation of the
representation matrices from SymPy to NumPy (and the usual Python math library).
The profiles indicate that a lot of time is spent in simplification of expressions.
There is no evidence that the expressions need to be handled algebraically.
In order to get some evidence, I will implement one representation matrix in NumPy 
and compare it to SymPy.
I'll compare their accuracy and performance.
However, in any case it would make the code cleaner if object-oriented design principles were used.
* finish reading Trevor's paper - TODO
* read the corresponding chapters in David's textbook - TODO
* design an OO class hierarchy and implement it for one operator and both SymPy and NumPy - TODO
* compare accuracy and performance - TODO

Comments on Trevor's paper:
* the text refers to `RWC_exp` (94) and `RWC_exp_link` (95) but the code contains `RWC_expt` and `RWC_expt_link`
* equation (103) implies that the operator is a tensor product, but mathematically it's simple a product
  * perhaps this is a matter of notation - Trevor uses the `\otimes` symbol which usually denotes tensor product
  * on further reading, the tensor product refers to the SO(3) value of the operator, 
  * i.e. the operator W maps the Hilbert space H to the tensor product H \otimes V where V is a representation of SO(3)
  * for example, multiplication by the position vector sends a scalar wave function to H \otimes R^3

Next: 7.3.2. Products involving one non-scalar operator - TODO

break 6:50 pm

### 8:30 pm

Next: 7.3.2. Products involving one non-scalar operator - DONE

Comments:
* In section 8.1, "From (76), it is seen that each truncated Hilbert space Htrunc used in the model is a direct product of truncated spherical and radial spaces."
  * This isn't accurate. The truncated Hilbert space is a direct sum of direct products.
  * The radial space factor varies with the seniority of the SO(5) factor
* In section 8.2.2, "The component Lvals of (127) contains, in ascending order, all values of L in the range Lmin ≤ L ≤ Lmax that have non-zero dimension in trunc H."
  * However, I recall reading that Lvals was not necessarily in ascending order.
  * Never mind. Section 7.1 says: "The component Lvals of (96) contains, in ascending order, all values of L in the range Lmin ≤ L ≤ Lmax, trunc
    specified by (77) or (78), that have non-zero dimension in H . Note that these values are not necessarily consecutive."

Next: Appendix A. Rigid-β models - TODO

break 11:00 pm

## 2022-05-02

### 8:30 am

Next: Appendix A. Rigid-β models - DONE

Note that the following paper describes the coordinates for the 4-sphere
that use SO(3) coordinates plus the angle gamma:
```text
JOURNAL OF MATHEMATICAL PHYSICS VOLUME 45, NUMBER 7 JULY 2004
Spherical harmonics and basic coupling coefficients for the group SO„5... in an SO„3... basis
D. J. Rowe and P. S. Turner
J. Repka
```

Next:
* read the corresponding chapters in David's textbook - TODO

break 10:00 am

## 2022-05-03

### 10:55 am

* read the corresponding chapters in David's textbook - IN-PROGRESS
  * note that the description of 4-sphere coordinate system is given the Rowe, Turner, Repka article.
  * stopped at p99, 2.1.2 Spherical Polar Coordinates

break 12:25 pm

### 3:55 pm

* continue from p99, 2.1.2 Spherical Polar Coordinates - DONE
  * stopped at p 106, 2.2.1 The metric tensor

David's textbook contains all the relevant math.
I'll use it as a reference.
I hope Trevor's article uses the same notations and conventions.

Continue with performance improvements.
* design an OO class hierarchy and implement it for one operator and both SymPy and NumPy - TODO
* compare accuracy and performance - TODO

I believe that I can make progress make first using NumPy in the functions that
compute the prods and sums of operators.
The dividing line occurs where SymPy matrices are converted into numerical matrices using the evalf() method.
* replaced Matrix with np.ndarray at the point where evalf() is called
* use the `float()` function to convert SymPy `Expr` objects and store the result in np.ndarray objects, aka NDFloat64
* after conversions, scan code for uses of `ndarray_to_Matrix()` - TODO
  * understand why are we converting back to SymPy?
* inspect the code and determine where this dividing line occurs - IN-PROGRESS
  * RepXspace - DONE
    * change return type to NDFloat64 - DONE
    * update callers to expect NDFloat64 instead of Matrix - DONE
      * AmpXspeig - DONE
      * DigXspace - DONE
      * debug_repxspace.py - DONE
      * test_full_operators.py - DONE
    * test - DONE
      * 16.93s, 15.38s, 16.51s, 15.58s
  * RepXspace_Prod - TODO
    * change return type to NDFloat64 - DONE
    * update callers - TODO
      * RepXspace - TODO

break 5:55 pm

## 2022-05-04

### 3:05 pm

Continue conversion from Matrix to ndarray
* RepXspace_Prod - TODO
  * change return type to NDFloat64 - DONE
  * update callers - DONE
    * RepXspace - DONE
  * test - OK 20.75s with both SymPy and NumPy
  * remove redundant SymPy - DONE
  * test - OK 14.76s, 14.80s, 14.76s, 14.92s
  * average time before change = (16.93 + 15.38 + 16.51 + 15.58)/4 = 16.1
  * average time after change = (14.76 + 14.80 + 14.76 + 14.92)/4 = 14.81
  * time improvement = (16.1 - 14.81) = 1.29
  * percent improvement = 1.29/16.1 * 100 = 8%
  * profile execution for (5, 18, 6)
    * unprofiled time = 16.4s
    * profiler now throws error:
```text
In ACM_Adapt, the scaling factor for "transition rates" is chosen such that
  B(E2: 2(1) -> 0(1)) = 100.000000
nu_max: 5, v_max: 18, L_max: 6
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
elapsed process time for ACM_Scale: 16.415146
Traceback (most recent call last):
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/IPython/core/interactiveshell.py", line 3251, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-aaa4f1cb7dfe>", line 1, in <module>
    runfile('/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/performance/profile_acm_scale.py', wdir='/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/performance')
  File "/Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5080.210/IntelliJ IDEA.app.plugins/python/helpers/pydev/_pydev_bundle/pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "/Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5080.210/IntelliJ IDEA.app.plugins/python/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/performance/profile_acm_scale.py", line 62, in <module>
    cProfile.run(command, filename, SortKey.CUMULATIVE)
  File "/usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/cProfile.py", line 16, in run
    return _pyprofile._Utils(Profile).run(statement, filename, sort)
  File "/usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/profile.py", line 53, in run
    prof.run(statement)
  File "/usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/cProfile.py", line 95, in run
    return self.runctx(cmd, dict, dict)
  File "/usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/cProfile.py", line 100, in runctx
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
NameError: name 'main' is not defined
```

* Why the changed behaviour in cProfile.run?
  * Debug the execution -  - DONE no exception
  * Rerun - exception occurs - DONE
  * commit latest changes to numpy branch - DONE
  * check out master and run profiler - DONE no exception
  * Summary: I can't profile execution on the numpy branch
  * What has changed? Do a diff between master and numpy branches - DONE no smoking gun
  * other people have hit this problem
  * they work around it using `cProfile.runctx(‘functionname(args)’, globals(), locals())`
  * update the code to avoid passing command string - DONE

The execution time is now 15.24s:
```text
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
nu_max: 5, v_max: 18, L_max: 6
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
elapsed process time for ACM_Scale: 15.248869000000001
```

This latest change has not been a significant improvement.
Looks like the main bottleneck was in diagonalisation.

Eliminate redundancy in `RepXspace` - TODO

break 6:30 pm

## 2022-05-05

### 3:40 pm

* Eliminate redundancy in `RepXspace` - DONE
  * `elapsed process time for ACM_Scale: 16.424601`
  * possibly slightly slower because I am now initializing `sum` with an array of zeros
* special empty list of terms
  * `elapsed process time for ACM_Scale: 16.390562`
* avoid `sum()`:
  * `elapsed process time for ACM_Scale: 16.377676`
* Leave special casing in for now since it does make a slight improvement

* scan code for conversions of np.ndarray to Matrix - DONE
  * leave as is for now

* Continue running the examples from the Maple worksheet and fix bugs and performances issues as they arise - IN-PROGRESS
  * my goal is to have the entire worksheet running correctly and with adequate performance
  * create test cases for examples
* rerun existing Jupyter notebooks - IN-PROGRESS
  * The Jupyter notebook is displaying a different number of digits than the terminal!
    * Terminal: `Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):`
    * Notebook: `Lowest eigenvalue is -6.3438. Relative eigenvalues follow (each divided by 1.0000):`
    * Defer investigation
  * Completed 2.2
    * The display difference is in fact bigger than just precision
    * The number of eigenvalues is just 4, should be 6
* Terminal:
```text
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
```
* Notebook:
```text
Lowest eigenvalue is -6.3438. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00,   1.56,   1.99,   2.86]
  At L= 2: [   0.10,   0.97,   1.74,   2.19]
  At L= 3: [   1.11,   2.70,   3.32,   4.58]
  At L= 4: [   0.30,   1.23,   1.92,   2.08]
  At L= 5: [   1.41,   2.20,   3.22,   3.64]
  At L= 6: [   0.61,   1.58,   2.35,   2.49]
```
* Perhaps there is  problem accessing the global variables in the notebook?
  * Problem solved: Rerun notebook from start because I had added ACM_set_defaults(0) after customizing the output settings

Next: 2.3 - TODO

break 7:00 pm

### 6:45 pm

Next: 2.3 - IN-PROGRESS
* 2.3 is taking a very long time > 30m
```text
ACM_set_rat_lst([[2,0,1,1],[4,2,1,1],[6,4,1,1],[8,6,1,1]])
ACM_set_amp_lst([[2,2,1,1]])
ACM_Scale(RWC_ham_fig5a, sqrt(B), 2.5, 0, 10, 0, 18, 0, 6)
```
* results are correct:
```text
Lowest eigenvalue is -6.33961. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.57,    2.12,    2.89,    3.61,    4.23]
  At L= 2: [    0.10,    0.97,    1.78,    2.25,    2.39,    3.16]
  At L= 3: [    1.11,    2.75,    3.37,    4.57,    5.07,    5.67]
  At L= 4: [    0.31,    1.24,    1.92,    2.11,    2.52,    2.82]
  At L= 5: [    1.43,    2.20,    3.24,    3.76,    3.94,    4.57]
  At L= 6: [    0.61,    1.58,    2.38,    2.54,    2.88,    2.91]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.13
  B(E2: 4(1) -> 2(1)) =     0.19
  B(E2: 6(1) -> 4(1)) =     0.22
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.22
```
* time if for smaller values of nu_max, v_max, L_max
* is execution slower in a Jupyter notebook?

Running in the IDE:
```text
nu_max: 10, v_max: 3, L_max: 6
Lowest eigenvalue is -6.23994. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.86,    2.16,    3.69,    4.25,    5.44]
  At L= 2: [    0.38,    1.48,    2.39,    3.45,    4.34,    5.37]
  At L= 3: [    1.37,    3.48,    5.57,    7.68,    9.85,   12.29]
  At L= 4: [    0.50,    1.92,    2.59,    3.95,    4.65,    5.97]
  At L= 6: [    1.37,    3.48,    5.57,    7.68,    9.85,   12.29]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.10
  B(E2: 4(1) -> 2(1)) =     0.16
  B(E2: 6(1) -> 4(1)) =     0.14
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 31.689609000000004
```

Running in Jupyter:
```text
Lowest eigenvalue is -6.23994. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.86,    2.16,    3.69,    4.25,    5.44]
  At L= 2: [    0.38,    1.48,    2.39,    3.45,    4.34,    5.37]
  At L= 3: [    1.37,    3.48,    5.57,    7.68,    9.85,   12.29]
  At L= 4: [    0.50,    1.92,    2.59,    3.95,    4.65,    5.97]
  At L= 6: [    1.37,    3.48,    5.57,    7.68,    9.85,   12.29]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.10
  B(E2: 4(1) -> 2(1)) =     0.16
  B(E2: 6(1) -> 4(1)) =     0.14
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
CPU times: user 29.4 s, sys: 172 ms, total: 29.5 s
Wall time: 28.5 s
```

IDE : Jupyter = 31.7 : 29.5

Increase v_max to 6.

IDE:
```text
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 85.188801
```
Jupyter:
```text
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
CPU times: user 1min 19s, sys: 244 ms, total: 1min 19s
Wall time: 1min 17s
```

IDE : Jupyter = 85.2 : 79.0

So in fact, Jupyter is faster, possibly because the IDE adds some overhead to the IPython console.

Profile the execution for v_max = 6. - DONE
* the profile shows that a lot of time is spent on SymPy numerical computation
* how long does Maple take on the above? - TODO
* I think I need to replace all numeric computations with NumPy

break 10:15 pm

## 2022-05-06

### 11:00 am

I ran `profile_acm_scale.py` with (nu_max=10, v_max=18, L_max=6) last night but is failed to complete
as of 11:00 am.
Terminate the process.

Plan:
* perform benchmarks on Maple vs Python for (10,6,6) - TODO
* Reimplement all Python code using NumPy for floating point computations - TODO
  * use NumPy vectorized operations where possible
  * create new code in a parallel set of modules
  * use OO design for new code
  * use current SymPy implementations as oracles for test cases

Benchmarks for nu_max: 10, v_max: 6, L_max: 6
* Python:
```text
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 85.85265
```
* Maple
```text
st := time();
ACM_Scale(RWC_ham_fig5a, sqrt(B), 2.500, 0, 10, 0, 6, 0, 6);
elapsed := time() - st;
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
                        elapsed := 3.572
```

There is a huge difference in performance.
Python : Maple = 86 : 4 = 21x slower

The above measurements include the computation of transition rates and amplitudes.
Both of these involve matrix computations.

Compare performance for (10, 6, 6) without the computation of transition rates and amplitudes.
* Maple: 3.4s -> 3.6s
* Python: 44.44s -> 85.9s

Clearly the SymPy matrix computations are too slow.
Proceed with conversion to NumPy.

General strategy:
* work bottom-up
* implement NumPy, OO replacement
* write test case using the SymPy implementation
* modify callers to use new implementation

Before doing the bottom-up replacement, change signature of DigXspace to use NumPy and avoid
conversion back to Matrix. - IN-PROGRESS
* ACM_Scale
* ACM_ScaleOrAdapt
* ShowEigs
* AmpXspeig - DONE
* Show_Rats
* Show_Amps

break 1:10 pm

### 5:00 pm

Before doing the bottom-up replacement, change signature of DigXspace to use NumPy and avoid
conversion back to Matrix. - IN-PROGRESS
* ACM_Scale - DONE
* ACM_ScaleOrAdapt - DONE
* Show_Eigs - DONE
* AmpXspeig - DONE
* Show_Rats - DONE
* Show_Amps
* Show_Mels
* Show_Mels_Row
* Show_Mels_Rows

Ripple return type NDFloatArrayLBlocks through callers - TODO

break 6:50 pm

## 2022-05-07

### 11:05 am

Ripple return type LBlockNDFloatArray class through callers - IN-PROGRESS
* def get/set methods for blocks specified by L_f, L_i - TODO

break 12:50 pm

### 2:25 pm

Ripple return type LBlockNDFloatArray class through callers - IN-PROGRESS
* def get/set methods for blocks specified by L_row, L_col - DONE
* AmpXspeig - DONE
* ACM_ScaleOrAdapt - DONE
* Show_Rats - DONE
* Show_Amps - DONE
* ACM_Adapt - DONE
* ACM_Scale - DONE
* Show_Mels - DONE
* Show_Mels_Row - DONE
* Show_Mels_Rows - DONE
* mypy - DONE
* pytest - DONE
* measure performance - 

```text
nu_max: 5, v_max: 3, L_max: 6
Lowest eigenvalue is -6.24231. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.79,    2.09,    3.64,    4.13,    5.49]
  At L= 2: [    0.38,    1.48,    2.30,    3.35,    4.15,    5.28]
  At L= 3: [    1.38,    3.39,    5.31,    8.27,   12.73,   23.48]
  At L= 4: [    0.50,    1.93,    2.44,    3.87,    4.66,    5.73]
  At L= 6: [    1.38,    3.39,    5.31,    8.27,   12.73,   23.48]
elapsed process time for ACM_Scale: 7.930843
```

With transition amplitudes:
```text
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 44.304010999999996
```

The previous Python time was 85s.
The change to using views of NumPy arrays reduced the time to 44s.
Speedup = 85/44 = 1.93x. 
This is progress but Maple is still an order of magnitude faster at 3.6 sec.
The Maple code is 44/3.6 = 12.2x faster.

Profile the Python code.
```text
Sat May  7 18:17:54 2022    acm_scale_10_6_6_stats
         138554906 function calls (133106390 primitive calls) in 83.903 seconds
   Ordered by: internal time
   List reduced from 918 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  4161177    4.799    0.000    6.478    0.000 {built-in method builtins.__import__}
304668/30717    4.435    0.000   34.703    0.001 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/simplify/powsimp.py:15(powsimp)
5662811/4954732    4.061    0.000   25.256    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/cache.py:69(wrapper)
3714487/3714433    3.785    0.000    7.194    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/sympify.py:92(sympify)
15659614/15310765    3.023    0.000    3.588    0.000 {built-in method builtins.isinstance}
  4161177    2.686    0.000    9.164    0.000 /Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5080.210/IntelliJ IDEA.app.plugins/python/helpers/pydev/_pydev_bundle/pydev_import_hook.py:16(do_import)
93790/88179    2.480    0.000    9.923    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/mul.py:178(flatten)
1053306/1049786    1.980    0.000    4.291    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/expr.py:144(__eq__)
  5815363    1.541    0.000    2.054    0.000 {built-in method builtins.getattr}
  2224968    1.475    0.000    3.192    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:1978(__hash__)
  5291882    1.433    0.000    1.983    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:2294(__hash__)
  2227919    1.251    0.000    1.721    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:807(__hash__)
  2076239    1.212    0.000    6.276    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/sympify.py:479(_sympify)
145403/134776    1.101    0.000   13.584    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/operations.py:46(__new__)
339243/153840    1.064    0.000    8.398    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/compatibility.py:501(ordered)
4735914/4532682    1.062    0.000    1.313    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/expr.py:126(__hash__)
    43755    0.954    0.000    2.155    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/facts.py:499(deduce_all_facts)
246534/62340    0.833    0.000    3.959    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/compatibility.py:315(default_sort_key)
1657189/1323095    0.821    0.000    6.685    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/assumptions.py:460(getit)
1771376/668094    0.816    0.000    1.056    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/basic.py:2065(_preorder_traversal)
  1364587    0.788    0.000    1.069    0.000 /usr/local/Cellar/python@3.10/3.10.0_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10/random.py:239(_randbelow_with_getrandbits)
  1579973    0.682    0.000    0.928    0.000 <frozen importlib._bootstrap>:404(parent)
  3562985    0.662    0.000    0.662    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/basic.py:713(args)
5503484/5439001    0.662    0.000    0.827    0.000 {built-in method builtins.hash}
273951/121824    0.645    0.000   26.223    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/simplify/powsimp.py:102(recurse)
638938/537074    0.640    0.000    4.228    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/decorators.py:88(__sympifyit_wrapper)
   411711    0.635    0.000    2.491    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:1876(__eq__)
   132639    0.631    0.000    6.971    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/basic.py:1241(replace)
  3714440    0.625    0.000    0.625    0.000 {built-in method builtins.hasattr}
303068/296249    0.571    0.000    2.074    0.000 /Users/arthurryman/Documents/repositories/agryman/acmpy/venv/lib/python3.10/site-packages/sympy/core/numbers.py:2210(__mul__)
```

The most time is still being spent on SymPy numerical computations.

Idea: it would be interesting to subtract the transition amplitude profile from the pure eigenvalue
profile to understand why the transition amplitude profile is so much slower.
This could be done using Pandas.
The difference is probably that the transition amplitude matrix is a full matrix whereas
the eigenvalue matrix is block diagonal.
Defer this for now since it's clear that SymPy should not be used for numerical computations.

Change scaling factor to be float - TODO

Check code for all uses of evalf() - TODO

break 6:25 pm

### 7:45 pm

Change scaling factor to be float - DONE
* mypy - DONE
* pytest - DONE

Checkpoint current version of code - DONE
* commit changes to numpy branch
* create and approve PR
* merge in master branch
* tag as v1-1-1

Check code for all uses of evalf() - IN-PROGRESS
* 52 results in code
* Make anorm and lambda_base floats - DONE
* measure performance - DONE
```text
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 5.1183629999999996
```

There is no change in the displayed accuracy.

Previous time:
```text
elapsed process time for ACM_Scale: 44.304010999999996
```

Speedup = 44.3/5.1 = 8.7x

Maple time = 3.6 sec.

Python/Maple = 5.1/3.6 = 1.4x.
Therefore, Python is now only 40% slower than Maple.

Check code for all uses of evalf() - IN-PROGRESS
* 41 results in code
* the remaining use of SymPy numerical computation is in the representation matrices of type Matrix
* convert the representations to NumPy - TODO
* try to also use NumPy vectorized computation - TODO
* NumPy also has an api for creating an array via a lambda
* However, the lambda is passed two arrays of indices which means it should be possible to vectorize


## 2022-05-08

### 10:50 am

Check code for all uses of evalf() and replace with NumPy where appropriate - IN-PROGRESS
* convert the representations to NumPy - TODO
* try to also use NumPy vectorized computation - TODO
* NumPy also has an api for creating an array via a lambda: np.fromfunction()
  * see https://numpy.org/doc/stable/reference/generated/numpy.fromfunction.html
* However, the lambda is passed two arrays of indices which means it should be possible to vectorize
  * define ufunc classes to compute matrix elements from indicies
  * see https://numpy.org/doc/stable/reference/generated/numpy.ufunc.html

evalf() is applied to the results of the following functions:
* NumSO5r3_Prod
* CG_SO5r3
* RepRadial_Prod_rem
* RepRadial_LC_rem
* Qred_p1
* Qred_m1
* QxQred_0
* QxQred_p2
* QxQxQred_p3
* QxQxQred_m3
* QmxQxQred_p1
* QixQxQred
* QxQxQred_m1
* mel_fun: MatrixElementFunction - DONE

break 12:20 pm

### 1:50 pm

evalf() is applied to the results of the following functions:
* RepSO5_sqLdim
* RepSO5_sqLdiv
* NumSO5r3_Prod
* CG_SO5r3
* ME_SO5r3
* RepRadial - IN-PROGRESS
* RepRadial_Prod_rem
* RepRadial_LC_rem
* ME_Radial_b2
* ME_Radial_bDb
* ME_Radial_D2b
* Qred_p1
* Qred_m1
* QxQred_0
* QxQred_p2
* QxQxQred_p3
* QxQxQred_m3
* QmxQxQred_p1
* QixQxQred
* QxQxQred_m1
* mel_fun: MatrixElementFunction - DONE

Analyse RepRadial
```text
def RepRadial(ME: Callable, lambdaa: float,
              nu_min: nonnegint, nu_max: nonnegint
              ) -> Matrix:
```
ME is used as:
```text
M: Matrix = Matrix(n, n, lambda i, j: ME(lambdaa, nu_min + int(i), nu_min + int(j)))
```
Example ME function is:
```text
def ME_Radial_b2(lambdaa: float, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
```
* it doesn't make sense for the return value to be Expr
* change return value to float - IN-PROGRESS
* define new type - DONE
```text
RadialMatrixElementFunction = Callable[[float, nonnegint, nonnegint], float]
```
* create test cases for each matrix element function - IN-PROGRESS
  * testing has so far revealed a difference in behaviour - DONE
    * Maple: binomial(-1, -1) = 1
    * SymPy: binomial(-1, -1) = 0
* ME_Radial_id_ml(2.5, 1, 0, 2) gave an imaginary value -1.632993162*I - TODO


break 7:15 pm

### 9:15 pm

* change ME function return value to float - DONE
* create a test case for each ME function - IN-PROGRESS
  * ME_Radial_S0 - DONE
  * ME_Radial_Sp - DONE
  * ME_Radial_Sm - DONE
  * ME_Radial_b2 - DONE
  * ME_Radial_bm2 - DONE
  * ME_Radial_pt - DONE
  * ME_Radial_D2b - DONE
  * ME_Radial_bDb - DONE
  * ME_Radial_b_pl - DONE
  * ME_Radial_bm_pl - DONE
  * ME_Radial_Db_pl - DONE
  * ME_Radial_b_ml - DONE
  * ME_Radial_bm_ml - DONE
  * ME_Radial_Db_ml - DONE
  * ME_Radial_id_pl - DONE
  * ME_Radial_id_ml - IN-PROGRESS
  * MF_Radial_id_poly
  * MF_Radial_id_pl

* ME_Radial_id_ml: 17 of 27 failed
```text
acmpy/tests/test_radial_me.py:357 (TestME_Radial_id_ml.test_ok[0-1-1--0.3760507166])
self = <acmpy.tests.test_radial_me.TestME_Radial_id_ml object at 0x129437ca0>
mu_f = 0, mu_i = 1, r = 1, expected = -0.3760507166

    @pytest.mark.parametrize(
        "mu_f,mu_i,r,expected", [
            (0, 0, 0, 1.0000000000),
            (0, 0, 1, 0.8819171036), -> 0.5773502691896257
            (0, 0, 2, 0.4879500364), -> 1.0
            (0, 1, 0, 0.0000000000),
            (0, 1, 1, -0.3760507166), -> -0.3651483716701107
            (0, 1, 2, -0.4161251894), -> -1.2649110640673518
            (0, 2, 0, 0.0000000000),
            (0, 2, 1, 0.2085954062), -> 0.2760262237369417
            (0, 2, 2, 0.3462370863), -> 1.434274331201272
            (1, 0, 0, 0.0000000000),
            (1, 0, 1, 0.4714045209), -> 0.816496580927726
            (1, 0, 2, 0.7968190730), -> > return res * math.sqrt(poch_f / poch_i) ValueError: math domain error
            (1, 1, 0, 1.0000000000),
            (1, 1, 1, 0.7035264708), -> 0.2581988897471611
            (1, 1, 2, -0.0849411986), -> > return res * math.sqrt(poch_f / poch_i) ValueError: math domain error
            (1, 2, 0, 0.0000000000),
            (1, 2, 1, -0.3902462714), -> -0.19518001458970663
            (1, 2, 2, -0.0942337990), -> > return res * math.sqrt(poch_f / poch_i) ValueError: math domain error
            (2, 0, 0, 0.0000000000),
            (2, 0, 1, 0.0000000000),
            (2, 0, 2, 0.3563483226), -> 1.632993161855452
            (2, 1, 0, 0.0000000000),
            (2, 1, 1, 0.6030226892), -> 0.8944271909999159
            (2, 1, 2, 0.7597371764), -> -1.0327955589886444
            (2, 2, 0, 1.0000000000),
            (2, 2, 1, 0.5853694070), -> 0.1690308509457033
            (2, 2, 2, -0.2633914755) -> 1.0734900802433864
        ]
    )
    def test_ok(self, mu_f, mu_i, r, expected):
        ME: float = ME_Radial_id_ml(2.5, mu_f, mu_i, r)
>       assert math.isclose(ME, expected)
E       assert False
E        +  where False = <built-in function isclose>(-0.3651483716701107, -0.3760507166)
E        +    where <built-in function isclose> = math.isclose
```

* the 0 or 1 case is correct
* there are two types of errors for the other cases
  * numeric value wrong
  * math domain error - probably taking the square root of a negative number

break 10:45 pm

## 2022-05-09

### 11:30 am

Debug test case failure:
```text
acmpy/tests/test_radial_me.py:357 (TestME_Radial_id_ml.test_ok[0-1-1--0.3760507166])
```
* Test case used lambda = 2.5 but expected data used 5.5 - DONE
  * all tests now pass

* create a test case for each ME function - IN-PROGRESS
  * ME_Radial_id_ml - DONE
  * MF_Radial_id_poly - TODO
  * MF_Radial_id_pl - TODO

The function:
```text
MF_Radial_id_poly(mu: Nu, nu: Nu, r: nonnegint)
```
is always called with nu <= mu + 2.

break 12:35 pm

### 3:00 pm

* create a test case for each ME function - DONE
  * MF_Radial_id_poly - DONE
  * MF_Radial_id_pl - DONE

It does appear the symbolic computation improves the accuracy of ME_Radial_id_pl and ME_Radial_id_ml.
This is because the matrix elements are ratios of Gamma functions and therefore cancellation occurs
making the results polynomials in lambda.
Both Maple and SymPy can simplify expressions.
Accuracy improves if the expressions are simplified before evaluation.

However, the Gamma functions appear in ratios that are expression as Pochhammer symbols.
SciPy provides an implementation, sc.poch. 
It is therefore plausible that SciPy uses a more accurate algorithm for evaluating Pochhammer symbols
that avoids first computing the Gamma functions and then dividing.

Compare the accuracy of the SymPy MF_Radial_id_poly implementation versus a ScipPy implementation using sc.poch. - TODO

Measure performance using the current version v1-1-2.

In the radial space, replace Matrix with ndarray. - TODO

Current Python performance on Ex 2.3 a:
```text
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
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
elapsed process time for ACM_Scale: 3.6990489999999996
```

Previous Python time:
```text
elapsed process time for ACM_Scale: 5.1183629999999996
```

Speedup = 5.12/3.70 = 1.38x. This is a worthwhile speedup.

Maple time = 3.6 sec.

Python/Maple = 3.7/3.6 = 1.03. The Python code is now only 3% slower.

Measure performance of Ex 2.3b.
```text
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
nu_max: 10, v_max: 6, L_max: 6
Lowest eigenvalue is -6.33329. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.63,    2.13,    3.19,    3.66,    4.23]
  At L= 2: [    0.13,    1.06,    2.05,    2.36,    2.71,    3.23]
  At L= 3: [    1.14,    3.02,    3.43,    5.15,    5.74,    7.29]
  At L= 4: [    0.32,    1.38,    2.09,    2.34,    2.63,    3.18]
  At L= 5: [    1.67,    2.48,    3.89,    4.72,    6.10,    6.98]
  At L= 6: [    0.70,    1.71,    2.62,    2.83,    3.10,    3.14]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.12
  B(E2: 4(1) -> 2(1)) =     0.18
  B(E2: 6(1) -> 4(1)) =     0.21
  B(E2: 2(1) -> 2(1)) =     0.18
  B(E2: 4(1) -> 4(1)) =     0.14
  B(E2: 6(1) -> 6(1)) =     0.12
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.23
  Amp( 2(2) -> 2(2) ) =     0.22
elapsed process time for ACM_Scale: 3.675498
```

Increase v_max to 18.
```text
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
nu_max: 10, v_max: 18, L_max: 6
Lowest eigenvalue is -6.33961. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.57,    2.12,    2.89,    3.61,    4.23]
  At L= 2: [    0.10,    0.97,    1.78,    2.25,    2.39,    3.16]
  At L= 3: [    1.11,    2.75,    3.37,    4.57,    5.07,    5.67]
  At L= 4: [    0.31,    1.24,    1.92,    2.11,    2.52,    2.82]
  At L= 5: [    1.43,    2.20,    3.24,    3.76,    3.94,    4.57]
  At L= 6: [    0.61,    1.58,    2.38,    2.54,    2.88,    2.91]
Selected transition rates follow (each divided by 1.00000):
  B(E2: 2(1) -> 0(1)) =     0.13
  B(E2: 4(1) -> 2(1)) =     0.19
  B(E2: 6(1) -> 4(1)) =     0.22
  B(E2: 2(1) -> 2(1)) =     0.17
  B(E2: 4(1) -> 4(1)) =     0.15
  B(E2: 6(1) -> 6(1)) =     0.13
Selected transition amplitudes follow (each divided by 1.00000):
  Amp( 2(1) -> 2(1) ) =    -0.22
  Amp( 2(2) -> 2(2) ) =     0.22
elapsed process time for ACM_Scale: 11.021412
```

* Example 2.2
  * 5, 18, 6: Maple = 8.509, Python = 3.425
  * 10, 18, 6: Maple = 20.165, Python = 6.649
  * 15, 18, 6: Maple = 44.735, Python = 11.102
  * 10, 6, 6: Maple = 3.620, Python = 2.883
* Example 2.3a
  * 10, 6, 6: Maple = 3.616, Python = 3.68
  * 10, 18, 6: Maple = 20.810, Python = 10.368
* Example 2.3b
  * 10, 18, 6: Maple = 20.751, Python = 10.406
* Example 2.3c
  * 10, 18, 6: Maple = 20.604, Python = 10.445
* Example 2.4a
  * ACM_Scale: 10, 18, 6: Maple = 20.272, Python = 10.434
  * ACM_Adapt: 10, 18, 6: Maple = 20.140, Python = 10.343
* Example 2.4b
  * ACM_Adapt: 10, 18, 6: Maple = 20.409, Python = 10.385
* Example 2.4c
  * ACM_Adapt: 10, 12, 12: Maple = 25.934, Python = 18.947

break 6:05 pm

### 7:40 pm

* Example 2.5a
  * ACM_Adapt: 10, 18, 6: Maple = 20.709, Python = 10.358
* Example 2.5b
  * ACM_Adapt: 10, 18, 6: Maple = 21.162, Python = 10.600
* Example 2.5c
  * ACM_Adapt: 10, 18, 6: Maple = 21.001, Python = 10.372

* Example 3 - TODO
* Create example running framework - DONE
* Port examples into framework - IN_PROGRESS
  * port set_example_2_4_a() next

break 10:05 pm

## 2022-05-10

### 3:35 pm

* Port examples into framework - IN_PROGRESS
  * port set_example_2_4_a() next - DONE
* Improve design of Example class - DONE
  * Each example should optionally follow some other example the leaves the ACM global variables in the required state
  * A typical example does these steps:
    * set
    * exec
    * unset
  * Change this to:
    * prepare(predecessor example) - if one exists
    * set(this example)
    * exec(this example)
    * unset(this example)
  * Define prepare(this example) as follows - DONE
    * prepare(predecessor example)
    * set(this example)
    * unset(this example)
* Example 3 - TODO

break 6:55 pm

* Port examples into framework - IN_PROGRESS
  * Section 3 - IN-PROGRESS


## 2022-05-11

### 2:40 pm

* Port examples into framework - IN_PROGRESS
  * Section 3 - IN-PROGRESS
    * Show_Eigs() and Show_Rats() are used in the examples so keep their APIs as-is
    * Show_Amps() also is part of the API
    * I can preserve the API on the understanding that instead of returning a Matrix of Matrix, I return LBlockNDFloatArray
    * I need to define an empty LBlockNDFloatArray, or maybe just a union type for this edge case, or Optional?

break 6:10 pm

### 8:40 pm

* Port examples into framework - DONE
* Section 3 - DONE
  * Show_Eigs() and Show_Rats() are used in the examples so keep their APIs as-is
  * Show_Amps() also is part of the API
  * I can preserve the API on the understanding that instead of returning a Matrix of Matrix, I return LBlockNDFloatArray
  * I need to define an empty LBlockNDFloatArray, or maybe just a union type for this edge case, or Optional?
    * use Optional[LBlockNDFloatArray] - DONE
* Section 4 - IN-PROGRESS
  * completed 4.3
  * next 4.4

break 10:20 pm

## 2022-05-12

### 10:30 am

Create Maple workbook with each example section as a worksheet so they can be re-executed individually. - DONE

* Section 4 - IN-PROGRESS
  * 4.4 - TODO

break 12:20 pm

### 3:30 pm

* Section 4 - IN-PROGRESS
  * 4.4 - IN-PROGRESS
  * RWC_alam(B, -3, 2) fails for B >= 15
    * the translation to Python is correct since the code work for certain inputs
    * the problem is in `solveset()` which fails to find any solution as B increases past 14
    * try using an older SymPy solver - not obvious what to use
    * do the math

break 6:40 pm

## 2022-05-13

### 8:25 am

* plot the function of `anorm` that `RWC_alam` is minimising - IN-PROGRESS

break 8:50 am

### 10:35 am

* plot the function of `anorm` that `RWC_alam` is minimising - IN-PROGRESS

break 12:55 pm

### 3:20 pm

* plot the function of `anorm` that `RWC_alam` is minimising - DONE
  * plotting failed to reveal any clue

## 2022-05-14

### 11:00 am

* clean up visualization notebook - IN-PROGRESS
* report SymPy bugs - TODO
  * `binomial(-1, -1) = 0`
  * `solveset` returns the empty set

break 11:40 am

### 2:25 pm
* clean up visualization notebook - DONE
* report SymPy bugs - IN-PROGRESS
  * `binomial(-1, -1) = 0` - DONE
    * see https://github.com/sympy/sympy/issues/23497
  * `solveset` returns the empty set - IN-PROGRESS

break 6:40 pm

## 2022-05-15

### 10:45 am

* report SymPy bugs - IN-PROGRESS
  * `solveset` returns the empty set - IN-PROGRESS
  * create standalone, simplified test case - IN-PROGRESS
  
break 12:35 pm

## 2022-05-16

### 11:00 am

* report SymPy `solveset` bug - IN-PROGRESS
  * `solveset` returns the empty set - IN-PROGRESS
  * create standalone, simplified test case - IN-PROGRESS
  * I'm getting unexpected results from `solveset()` for `RWC_alam()`
  * Derive the math in `RWC_alam_clam()` which is simpler - DONE
  * Derive the math in `RWC_alam()` - DONE

break 12:05 pm

### 3:10 pm

* report SymPy `solveset` bug - IN-PROGRESS
  * `solveset` returns the empty set
  * create standalone, simplified test case - IN-PROGRESS
  * I'm getting unexpected results from `solveset()` for `RWC_alam()` - IN-PROGRESS

break 6:25 pm

### 8:30 pm

* report SymPy `solveset` bug - DONE
  * create standalone, simplified test case - DONE
  * see https://github.com/sympy/sympy/issues/23510

* use nsolve instead of solveset - TODO
  * add a parameter to the initial guess

* I upgraded to the latest SymPy and now mypy reports errors
  * fix mypy - TODO

## 2022-05-17

### 11:25 am

* try workaround for solveset from Issue #23510
```text
Note that 3/2 results in a float 1.5, which may lead to further inaccuracy and solver failure.
If you use Rational(3, 2) or S(3)/2 your example will work fine.

==========Solving equation for B = 14 ==========
Success: nsolve solution = 19.676355436230185
Success: first solveset solution = 19.676355436230185
Success: first solveset solution after simplification = 19.676355436230185
==========Solving equation for B = 15 ==========
Success: nsolve solution = 20.911495067823516
Success: first solveset solution = 20.911495067823516
Success: first solveset solution after simplification = 20.911495067823516
```
* using `S(3)/2` lets `solveset()` succeed, but in actual use the parameters $c_1$ and $c_2$ may be floats
* to fix the issue use `nsolve()`
  * need an initial guess so analyze the expectation value and derive an expression for the initial guess - TODO
  * Note: the Maple code selects that maximum root.
    * Shouldn't it pick the root that minimizes the expectation value? - understand why this behavior - IN-PROGRESS

break 12:25 pm

### 2:00 pm

* Note: the Maple code for `RWC_alam()` selects that maximum root!!!
  * Shouldn't it pick the root that minimizes the expectation value? - understand why this behavior - DONE
  * create Issue in Maple code repo - DONE
    * see https://github.com/agryman/acm16/issues/6

* I upgraded to the latest SymPy and now mypy reports errors
  * fix mypy - DONE (reverted to sympy 1.9)
  * mypy                          0.950
With sympy==1.10.1
```text
mypy acmpy

acmpy/compat.py:171: error: Variable "sympy.matrices.Matrix" is not valid as a type
acmpy/compat.py:171: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
acmpy/compat.py:173: error: Argument 1 to "array" has incompatible type "List[float]"; expected "Union[_SupportsArray[dtype[<nothing>]], Sequence[_SupportsArray[dtype[<nothing>]]], Sequence[Sequence[_SupportsArray[dtype[<nothing>]]]], Sequence[Sequence[Sequence[_SupportsArray[dtype[<nothing>]]]]], Sequence[Sequence[Sequence[Sequence[_SupportsArray[dtype[<nothing>]]]]]]]"
acmpy/compat.py:173: error: Matrix? has no attribute "__iter__" (not iterable)
acmpy/compat.py:176: error: Variable "sympy.matrices.Matrix" is not valid as a type
acmpy/compat.py:176: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
...
acmpy/tests/test_full_space.py:99: error: Variable "sympy.matrices.Matrix" is not valid as a type
acmpy/tests/test_full_space.py:99: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#variables-vs-type-aliases
Found 121 errors in 8 files (checked 50 source files)
```

Back off to sympy==1.9

```text
pip uninstall sympy
pip install sympy==1.9
```

Now no mypy errors.

```text
(venv) riemann:src arthurryman$ mypy acmpy
Success: no issues found in 50 source files
```

I've joined the sympy mailing list and asked the question.
* stay with sympy 1.9 until I understand the *correct* way to use mypy with sympy 1.10.1 - DONE

* to fix the issue use `nsolve()` - IN-PROGRESS
  * need an initial guess for nsolve 
    * hard code 20 to start - TODO
    * rerun pytest
  * need an initial guess so analyze the expectation value and derive an expression for the initial guess - IN-PROGRESS
  * check notebooks that describe behaviour of expectation value for small and large values
