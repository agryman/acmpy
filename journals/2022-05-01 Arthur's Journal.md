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

Eliminate redundancy in `RepXspace` - TODO

break 6:30 pm
