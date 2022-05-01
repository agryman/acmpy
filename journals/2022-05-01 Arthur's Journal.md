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
* design an OO class hierarchy and implement it one one operator and both SymPy and NumPy - TODO
* compare accuracy and performance - TODO


