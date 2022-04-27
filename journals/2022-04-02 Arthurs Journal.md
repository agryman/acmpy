# Arthur's Journal

## 2022-04-02

`full_space.py` - IN-PROGRESS
* `Eigenfiddle` - IN-PROGRESS

I need to understand the correspondence between the Maple and SymPy
functions that compute eigenvectors.

* Maple:
```text
#   eigenstuff:=Eigenvectors(Matrix(n,n,(i,j)->(Hmatrix[i,j]+Hmatrix[j,i])/2,
#                                     scan=diagonal[upper],shape=symmetric));
```

According to the Maple Help docs, the scan option is only used when the matrix
is initialized from a list.
The shape option is used to allocate storage. Since the matrix is symmetric,
only half the storage is needed.

* SymPy:

## 2022-04-03

### 6:25 pm

Understand output of Maple `Eigenvectors` procedure.

break 6:43 pm

## 2022-04-04

### 9:57 am

Maple `Eigenvectors(M)` returns the list of eigenvalues as a column vector,
and the list of eigenvectors as a matrix where the columns are the
eigenvectors. Therefore, if we create a diagonal matrix D from the eigenvalues
and let V be the matrix of eigenvectors, we should have MV = VD.

break 10:30 am

### 3:00 pm

In SymPy:

To find the eigenvectors of a matrix, use eigenvects.
eigenvects returns a list of tuples of the form (eigenvalue, algebraic_multiplicity, [eigenvectors]).

```text
M = Matrix([[3, -2,  4, -2], [5,  3, -3, -2], [5, -2,  2, -2], [5, -2, -3,  3]])
>>> M
⎡3  -2  4   -2⎤
⎢             ⎥
⎢5  3   -3  -2⎥
⎢             ⎥
⎢5  -2  2   -2⎥
⎢             ⎥
⎣5  -2  -3  3 ⎦
>>> M.eigenvals()
{-2: 1, 3: 1, 5: 2}

```

There is a fairly direct correspondence between Maple and SymPy.
The main difference is that SymPy includes the multiplicity of the eigenvalues.

* Create a Python equivalent to the Maple `Eigenvectors` procedure - DONE

`full_space.py` - IN-PROGRESS
* `Eigenfiddle` - DONE
* `AmpXspeig` - IN-PROGRESS

Note: `AmpXspeig` creates a Maple Matrix whose elements are themselves of type Matrix.
SymPy handles this the construction the same way.
This may make the use of NumPy less straight-forward.

break 7:12 pm

## 2022-04-05

### 11:54 am

`full_space.py` - IN-PROGRESS
* `AmpXspeig` - DONE
* `Show_Eigs` - DONE
* `min_head` - DONE
* `fsel` - DONE
* `Show_Mels` - TODO

break 2:19 pm

## 4:44 pm

`full_space.py` - IN-PROGRESS
* `Show_Mels` - IN-PROGRESS

break 7:59 pm

## 2022-04-06

### 8:48 am

`full_space.py` - IN-PROGRESS
* `Show_Mels` - IN-PROGRESS

break 9:30 am

## 3:23 pm

`full_space.py` - IN-PROGRESS
* `Show_Mels` - DONE
* `Show_Mels_Row` - DONE
* `Show_Rats` - DONE
* `Show_Amps` - DONE
* `ACM_ScaleOrAdapt` - IN-PROGRESS

break 5:30 pm

## 2022-04-07

### 2:55 pm

`full_space.py` - DONE
* `ACM_ScaleOrAdapt` - DONE
* `ACM_Scale` - DONE
* `ACM_Adapt` - DONE

`hamiltonian_data.py` - IN-PROGRESS
* `RWC_Ham` - DONE
* `RWC_expt` - DONE
* `RWC_expt_link` - DONE
* `RWC_dav` - DONE
* `lam_dav` - DONE
* `beta_dav` - DONE
* `RWC_alam` - IN-PROGRESS

break 5:39 pm

## 2022-04-08

### 4:25 pm

`hamiltonian_data.py` - IN-PROGRESS
* `RWC_alam` - IN-PROGRESS

break 5:30 pm

## 2022-04-09

### 3:30 pm

`hamiltonian_data.py` - DONE
* `RWC_alam` - DONE
* `RWC_alam36` - DONE
* `RWC_alam_clam` - DONE
* `RWC_alam_fun` - DONE

`radial_space.py` - IN-PROGRESS
* `ME_Radial_bDb` - DONE
* `ME_Radial_b_pl` - DONE
* `ME_Radial_bm_pl` - DONE
* `ME_Radial_Db_pl` - DONE
* `ME_Radial_b_ml` - DONE
* `ME_Radial_bm_ml` - DONE
* `ME_Radial_Db_ml` - DONE
* `ME_Radial_id_pl` - IN-PROGRESS

break 6:00 pm

### 8:12 pm

`radial_space.py` - IN-PROGRESS
* `ME_Radial_id_pl` - DONE
* `ME_Radial_id_ml` - DONE
* `MF_Radial_id_poly` - DONE
* `MF_Radial_id_pl` - DONE
* `MF_Radial_id_pl2` - DONE
* `ME_Radial` - DONE
* `RepRadial` - TODO

break 10:20 pm

## 2022-04-10

### 3:30 pm

`radial_space.py` - IN-PROGRESS
* `RepRadial` - DONE
* `RepRadial_param` - DONE
* `RepRadial_sq` - DONE
* `Matrix_sqrt` - DONE
* `Matrix_sqrtInv` - DONE
* `RepRadial_bS_DS` - DONE
* `Lambda_Splits` - TODO

break 6:30 pm

## 2022-04-11

### 11:42 am

`radial_space.py` - IN-PROGRESS
* `Lambda_Splits` - DONE
* `RepRadialshfs_Prod` - TODO

break 12:05 pm

### 4:40 pm

`radial_space.py` - IN-PROGRESS
* `RepRadialshfs_Prod` - DONE
* `RepRadial_Prod` - DONE
* `RepRadial_Prod_rem` - DONE
* `Parse_RadialOp_List` - TODO

break 6:30 PM

## 2022-04-12

### 1:45 pm

`radial_space.py` - DONE
* `Parse_RadialOp_List` - DONE
* `Lambda_RadialOp_List` - DONE
* `RepRadial_LC` - DONE
* `RepRadial_LC_rem` - DONE

break 4:30 pm

### 5:10 pm

`so5_so3_cg.py` - IN-PROGRESS
* `load_CG_table` - IN-PROGRESS

break 5:25 pm

### 8:00 pm

`so5_so3_cg.py` - DONE
* `load_CG_table` - DONE
* `CG_SO5r3` - DONE

This concludes the initial translation effort.
All Maple code has been translated into Python.
Next step is to continue working through the Maple worksheet.

break 8:35 pm


## 2022-04-13

### 1:50 pm

Resume working through the `acm1.4a-examples.mw` Maple worksheet.
I copied the worksheet into `acm1.4a-examples-arthur.mw` and set the
directory of the SO5-S03 CG coefficients to my local copy.

Run all cells in the worksheet.

break 2:30 pm

### 6:15 pm

Worksheet completed:

* Time: 10261.31s = 171 minutes
* Memory: 561.93M

Saved PDF of results.

Continue converting worksheet to Jupyter notebooks.

`2. Basic use of ACM_Scale and ACM_Adapt (Fig 5 of [RWC2009])` - IN-PROGRESS
* `2.2 Diagonalization of Hamiltonian using ACM_Scale` - IN-PROGRESS

I need to fix a circular import error:
```text
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Input In [3], in <module>
----> 1 from acmpy.internal_operators import ACM_Hamiltonian
      3 RWC_ham_fig5a = ACM_Hamiltonian(x1, 0, x3, x4, 0, x6, 0, 0, 0, x10)
      5 RWC_ham_fig5a

File ~/Documents/repositories/agryman/acmpy/src/acmpy/internal_operators.py:10, in <module>
      6 from sympy import Symbol, pi, sqrt, Integer, Rational, Expr, \
      7     S, factorial, Matrix, diag, eye
      9 from acmpy.compat import nonnegint, require_nonnegint, is_odd, IntFloatExpr
---> 10 from acmpy.so5_so3_cg import CG_SO5r3
     11 from acmpy.spherical_space import lbsSO5r3_rngVvarL, dimSO3, dimSO5r3_rngVvarL, SO5SO3Label
     13 OperatorProduct = tuple[Expr, tuple[Symbol, ...]]

File ~/Documents/repositories/agryman/acmpy/src/acmpy/so5_so3_cg.py:9, in <module>
      5 from os.path import expanduser
      7 from sympy import S, Expr, Rational, simplify, sqrt, factorial
----> 9 import acmpy.globals as g
     10 from acmpy.compat import nonnegint, posint, require_nonnegint, require_posint, \
     11     is_odd, readdata_float
     12 from acmpy.spherical_space import dimSO5r3, dimSO5, dimSO3

File ~/Documents/repositories/agryman/acmpy/src/acmpy/globals.py:8, in <module>
      4 from typing import Callable, Optional
      6 from sympy import sqrt, Expr
----> 8 from acmpy.internal_operators import OperatorSum, Op_AM, quad_op
      9 from acmpy.spherical_space import dimSO3
     10 from acmpy.so5_so3_cg import CG_SO3, SO5Quintet, SO5Quartet

ImportError: cannot import name 'OperatorSum' from partially initialized module 'acmpy.internal_operators' 
(most likely due to a circular import) 
(/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/internal_operators.py)
```

Solution: move the CG_coeffs table from `globals.py` to `so5_so3_cg.py`. - DONE

Run `mypy`.
* Fix errors - TODO

break 6:40 pm

## 2022-04-14

### 2:45 pm

Run `mypy`.
* Fix errors - IN-PROGRESS

break 5:45 pm

## 2022-04-15

### 8:20 am

Run `mypy`.
* Fix errors - DONE

Do topological sort of modules by imports. - IN-PROGRESS
* `acm1_4.py` imports `globals.py`
* `compat.py`
* `full_operators.py`
* `full_space.py`
* `globals.py`
* `hamiltonian_data.py`
* `internal_operators.py`
* `radial_space.py`
* `so5_so3_cg.py`
* `spherical_space.py`

break 8:45 am

### 4:20 pm

Do topological sort of modules by imports. - DONE
* `full_space.py`: globals, compat, internal_operators, spherical_space, full_operators, radial_space
* `full_operators.py`: compat, spherical_space, radial_space, internal_operators, so5_so3_cg, globals
* `acm1_4.py`: globals
* `hamiltonian_data.py`: compat, internal_operators, globals
* `globals.py`: internal_operators, spherical_space, so5_so3_cg, compat
* `radial_space.py`: compat, internal_operators, eignenvalues
* `internal_operators.py`: compat, so5_s03_cg, spherical_space
* `so5_so3_cg.py`: compat, spherical_space
* `spherical_space.py`: compat
* `compat.py`: 
* `eigenvalues.py`

Break the cycles:
* radial_space -> full_space -> radial_space - DONE
* full_space -> full_operators -> radial_space -> full_space - DONE

Why does radial_space import full_space? - DONE
* full_space contained Eigenfiddle which is general purpose.
* I created `eigenvalues.py` and moved Eigenfiddle there.

break 5:30 pm

## 2022-04-18

Refactor `internal_operators.py` - DONE
* Move symbols into the modules for their Hilbert spaces - DONE
* Run `mypy` - TODO
* Run `pytest` - TODO

break 6:25 pm

### 8:30 pm

* Run `mypy` - DONE
* Run `pytest` - DONE

Circular imports:
* globals: internal_operators, spherical_space, so5_so3_cg, compat, full_space
* internal_operators: compat, so5_so3_cg, spherical_space, radial_space, full_operators
* full_operators: compat, spherical_space, radial_space, internal_operators, s05_so3_cg

We have a cycle: internal_operators -> full_operators -> internal_operators - DONE

* Rerun notebooks - DONE

Continue conversion of Section 2.2 - IN-PROGRESS
* getting exceptions - create test case file and debug in IDE
```text
ACM_Scale(RWC_ham_fig5a, sqrt(B), Rational(1, 2), 0, 5, 0, 18, 0, 6)
```

break 10:30 pm

## 2022-04-19

Continue conversion of Section 2.2 - IN-PROGRESS
* getting exceptions - create test case file and debug in IDE
```text
ACM_Scale(RWC_ham_fig5a, sqrt(B), Rational(1, 2), 0, 5, 0, 18, 0, 6)
```

Example 2.2 in the Maple notebook took 28 minutes to run and then gave a format string error.
Trace execution.
`RepXspace` is noticeably slow. It produces a 42 x 42 matrix of floats so maybe Numpy would be better.
`Eigenfiddle` is then called to find the eigenvalues and bases. It is also noticeably slow.
These functions are called in a loop over the range of angular momenta.

Second pass through the loop the matrix is 72 x 72 and `Eigenfiddle` is even slower - 3 minutes.

The dimensions of the matrix change as L changes (36, 102), increasing and decreasing.
Computation of the eigenvalues and bases is definitely the bottleneck.

1. Debug the formatting string error using a smaller testcase. - TODO

2. Perform a controlled benchmarking of Sympy versus Numpy for several
tasks involving floating point matrices. - TODO
* matrix creation
* matrix scalar multiplication
* matrix multiplication
* matrix inversion
* matrix diagonalisation

Debugging with debug_acm_scale.
* RepXspace_Prod returns a 1 x 1 matrix with `zoo` as its entry. - TODO
* The `zoo` is returned from RepXspace_Twin when the operator is Radial_bm2
* The matrix elements in `RepXspace_Twin` are assumed to be float but are actually Expr: `sph_ME: float = sph_Mat[i2 - 1, j2 - 1]`
* The call to `RepRadial_Prod_rem` returns `zoo`
* The call to `RepRadialshfs_Prod` returns `zoo`
* The call to `r_op.representation(anorm, lambda_run, R, nu_min, nu_max)` returns `zoo` where the args
are r_op is a KTOp with K = -2, T = 0, and anorm = S.One, lambda_run = S.One, R = 0, nu_min = 0, nu_max = 0
* It calls `RepRadial_bS_DS`
* `Mat = RepRadial(ME_Radial_bm2, lambda_run, nu_min, nu_max)`
* `ME_Radial_pt(S(1), 0, 0)` divides by `(lambdaa - 1)`!!!!
  * Looks like lambdaa cannot be == 1. Is it always > 1???

Work around this restrictions by using `lambdaa` = 2.5. - TODO
* This quickly recreates format string error:
```text
Lowest eigenvalue is -1.6496. Relative eigenvalues follow (each divided by 1.0000):
Traceback (most recent call last):
  File "/Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5080.210/IntelliJ IDEA.app.plugins/python/helpers/pydev/pydevd.py", line 1491, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "/Users/arthurryman/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/221.5080.210/IntelliJ IDEA.app.plugins/python/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/debug/debug_acm_scale.py", line 13, in <module>
    main()
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/debug/debug_acm_scale.py", line 9, in main
    ACM_Scale(ham, S.One, Rational(5, 2), 0, 0, 0, 0, 0, 0)
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/full_space.py", line 1280, in ACM_Scale
    return ACM_ScaleOrAdapt(0, 0, ham_op, anorm, lambda_base,
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/full_space.py", line 1217, in ACM_ScaleOrAdapt
    Show_Eigs(eigen_vals, Lvals, g.glb_eig_num)
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/full_space.py", line 403, in Show_Eigs
    ','.join([f'{((val - eigen_low) / sft):{wid}.{pre}f}'
  File "/Users/arthurryman/Documents/repositories/agryman/acmpy/src/acmpy/full_space.py", line 403, in <listcomp>
    ','.join([f'{((val - eigen_low) / sft):{wid}.{pre}f}'
TypeError: unsupported format string passed to Zero.__format__
```

break 7:30 pm

## 2022-04-20

### 6:00 pm

Simplify use of the `index()` function for lists. - TODO

break 6:15 pm

## 2022-04-21

### 11:40 am

Simplify use of the `index()` function for lists. - DONE

Debug the formatting string error using a smaller testcase. - IN-PROGRESS
* Recreate the error by using `lambdaa` = 2.5 IN `debug/acm_scale.py. - IN-PROGRESS

break 12:30 pm

### 3:15 pm

Debug the formatting string error using a smaller testcase. - DONE
* Recreate the error by using `lambdaa` = 2.5 in `debug/acm_scale.py. - DONE
  * Fix: convert sympy Float to built-in float

#### Status
The code runs slowly. The bottleneck is in the eigenvalue computation.
I assume that Sympy is slow because it is treating the matrices as having Float entries, or Expr in general.
I assume that Numpy or Scipy would be much faster.
At this point I can do one the following:
1. Continue running the Maple examples, but this could be slow if I hit more errors. I'd have to wait 38 minutes for the error to appear.
2. Skip to the Component Testing examples.
3. Compare performance of Sympy versus Numpy.

#### Decision
* The Numpy performance on matrix operations is too slow to be used in practice.
* The use of Python is therefore not attractive unless it performs comparably to Maple.
* The entire Maple notebook took 10261 seconds to execute.
* The first ACM_Scale example took around 38 minutes = 38 * 60 seconds = 2280 seconds to execute.
* Accurately time the first ACM_Scale example in Maple and in Python. - TODO

I measured the time in Maple in the command line interface.
```text
> st:=time():ACM_Scale(RWC_ham_fig5a, sqrt(B), 2.5, 0, 5, 0, 18, 0, 6):elapsed:=time()-st;                                                                    
memory used=1411.4MB, alloc=44.3MB, time=24.70
memory used=1433.8MB, alloc=44.3MB, time=25.12
memory used=1468.7MB, alloc=44.3MB, time=26.20
memory used=1495.9MB, alloc=44.3MB, time=26.73
memory used=1521.1MB, alloc=44.3MB, time=26.95
memory used=1546.1MB, alloc=44.3MB, time=27.06
memory used=1579.6MB, alloc=44.3MB, time=28.01
memory used=1610.0MB, alloc=44.3MB, time=28.74
memory used=1643.1MB, alloc=44.3MB, time=29.61
memory used=1668.8MB, alloc=44.3MB, time=30.09
memory used=1694.7MB, alloc=44.3MB, time=30.30
memory used=1720.6MB, alloc=44.3MB, time=30.42
memory used=1746.5MB, alloc=44.3MB, time=30.54
memory used=1772.4MB, alloc=44.3MB, time=30.65
memory used=1806.7MB, alloc=44.3MB, time=31.52
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
                                                                       elapsed := 7.946
```

The elapsed CPU time in Maple was less than 8 seconds.

The equivalent Python test is in `examples/ex_2_2_diagonalization_of_hamiltonian.py`.
```text
Lowest eigenvalue is -3045.21343. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [ 5.63491,41.83980,106.92048,915.30012,952.04333,1037.52618,1171.14025,4515.83137,4521.08029,4533.34196,4552.65238,5409.82870,5416.63907,5428.89411,17917.01853,17936.94719,17983.57880,18057.22904,22290.18949,22310.22373,22346.33648,47227.71161,47244.89910,47285.08103,47348.44491,54926.89712,54943.36906,54973.04913,164070.98192,164085.37568,164118.98196,164171.85082,202161.49072,202176.16637,202202.59014,468424.39097,468438.88854,468472.72422,468525.91726,524008.51415,524022.31690,524047.16458]
  At L= 2: [ 0.00000,14.48825,26.55757,60.33102,82.02645,135.00674,922.10926,934.36020,975.14482,1003.64660,1076.75667,1121.30662,4516.80322,4518.55255,4524.38718,4528.47395,4538.99290,4545.42920,5408.76862,5411.49339,5413.76365,5420.11937,5424.20447,5434.18746,17920.70648,17927.34769,17949.51221,17965.05219,18005.10599,18029.64996,22287.07481,22295.08485,22301.76234,22320.47129,22332.50779,22361.96102,47230.89298,47236.62115,47255.73112,47269.12278,47303.61414,47324.73179,54924.33587,54930.92246,54936.41276,54951.79274,54961.68545,54985.88600,164073.64703,164078.44469,164094.44117,164105.64265,164134.46132,164152.08330,202159.20810,202165.07782,202169.96961,202183.66842,202192.47619,202214.01084,468427.07555,468431.90797,468448.01770,468459.29602,468488.30314,468506.03379,524006.36715,524011.88805,524016.48894,524029.37206,524037.65456,524057.90232]
  At L= 3: [ 5.63505,41.83981,106.92049,952.04330,1037.52618,1171.14025,4521.08047,4533.34201,4552.65240,5409.82793,5416.63898,5428.89407,17936.94721,17983.57880,18057.22904,22290.18940,22310.22372,22346.33647,47244.89911,47285.08103,47348.44491,54926.89706,54943.36906,54973.04913,164085.37569,164118.98196,164171.85082,202161.49071,202176.16637,202202.59014,468438.88854,468472.72422,468525.91726,524008.51414,524022.31690,524047.16458]
  At L= 4: [ 5.63497,14.48828,26.55759,41.83982,60.33103,82.02646,106.92049,135.00674,922.10926,934.36013,952.04329,975.14481,1003.64659,1037.52617,1076.75666,1121.30662,1171.14025,4516.80322,4518.55298,4521.08052,4524.38727,4528.47404,4533.34204,4538.99294,4545.42922,4552.65241,5409.82835,5411.49322,5413.76349,5416.63894,5420.11931,5424.20442,5428.89405,5434.18745,17920.70648,17927.34774,17936.94722,17949.51222,17965.05220,17983.57881,18005.10599,18029.64997,18057.22904,22290.18945,22295.08483,22301.76232,22310.22372,22320.47128,22332.50778,22346.33647,22361.96102,47230.89298,47236.62118,47244.89912,47255.73112,47269.12278,47285.08103,47303.61415,47324.73180,47348.44491,54926.89710,54930.92245,54936.41274,54943.36905,54951.79273,54961.68544,54973.04913,54985.88599,164073.64703,164078.44469,164085.37569,164094.44117,164105.64265,164118.98196,164134.46132,164152.08330,164171.85082,202161.49071,202165.07782,202169.96961,202176.16637,202183.66842,202192.47619,202202.59014,202214.01084,468427.07555,468431.90797,468438.88854,468448.01770,468459.29602,468472.72422,468488.30314,468506.03379,468525.91726,524008.51415,524011.88805,524016.48894,524022.31690,524029.37206,524037.65456,524047.16458,524057.90232]
  At L= 5: [14.48834,26.55760,60.33104,82.02646,135.00675,934.36012,975.14479,1003.64658,1076.75666,1121.30662,4518.55308,4524.38740,4528.47407,4538.99298,4545.42923,5411.49287,5413.76343,5420.11924,5424.20439,5434.18743,17927.34775,17949.51224,17965.05220,18005.10600,18029.64997,22295.08479,22301.76232,22320.47127,22332.50778,22361.96101,47236.62118,47255.73113,47269.12279,47303.61415,47324.73180,54930.92242,54936.41274,54951.79273,54961.68544,54985.88599,164078.44469,164094.44118,164105.64265,164134.46132,164152.08330,202165.07781,202169.96961,202183.66842,202192.47618,202214.01084,468431.90797,468448.01770,468459.29602,468488.30314,468506.03379,524011.88805,524016.48894,524029.37205,524037.65456,524057.90231]
  At L= 6: [ 5.63500,14.48830,26.55760,41.83983,41.83985,60.33105,82.02647,106.92050,106.92050,135.00675,934.36020,952.04322,952.04327,975.14479,1003.64658,1037.52616,1037.52616,1076.75665,1121.30662,1171.14024,1171.14024,4518.55253,4521.08064,4521.08095,4524.38740,4528.47411,4533.34210,4533.34215,4538.99300,4545.42924,4552.65243,4552.65243,5409.82817,5411.49313,5413.76343,5416.63875,5416.63885,5420.11922,5424.20436,5428.89398,5428.89401,5434.18743,17927.34769,17936.94723,17936.94726,17949.51224,17965.05220,17983.57882,17983.57882,18005.10600,18029.64997,18057.22904,18057.22905,22290.18943,22295.08482,22301.76232,22310.22369,22310.22370,22320.47127,22332.50777,22346.33646,22346.33646,22361.96101,47236.62114,47244.89912,47244.89915,47255.73113,47269.12279,47285.08104,47285.08104,47303.61415,47324.73180,47348.44491,47348.44491,54926.89708,54930.92244,54936.41274,54943.36904,54943.36904,54951.79273,54961.68544,54973.04912,54973.04913,54985.88599,164078.44468,164085.37569,164085.37569,164094.44118,164105.64265,164118.98196,164118.98196,164134.46132,164152.08330,164171.85082,164171.85082,202161.49071,202165.07781,202169.96961,202176.16636,202176.16637,202183.66842,202192.47618,202202.59014,202202.59014,202214.01084,468431.90797,468438.88854,468438.88854,468448.01770,468459.29602,468472.72422,468472.72422,468488.30315,468506.03379,468525.91726,468525.91726,524008.51415,524011.88805,524016.48894,524022.31690,524022.31690,524029.37205,524037.65456,524047.16458,524047.16458,524057.90231]
elapsed process time for ACM_Scale: 659.327389
```

There elapsed time is 659 seconds which is almost 100x slower than Maple.
Also, the results are different, and the output does not respect the settings.
All eigenvalues are displayed and each is displayed with too much precision.

First, determine why the results are different and fix the problem.
Work with a test case that takes a few seconds to execute in Python.

The minimal test case is in `debug_acm_scale.py`

Maple result:
```text
Lowest eigenvalue is -2.50000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                [[[-2.50000000000000]], [], [0]]
```

Python result:
```text
Lowest eigenvalue is -1.6496. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [ 0.0000]
elapsed time: 0.198793
```

Learn how to use Maple debugger to step through execution. - IN-PROGRESS

break 6:10 pm

## 2022-04-22

### 11:00 am

Learn how to use Maple debugger to step through execution. - DONE

Fix display errors in `Show_Eigs` - IN-PROGRESS

```text
Lowest eigenvalue is -3045.21343. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    5.63,   41.84,  106.92,  915.30,  952.04, 1037.53]
elapsed process time for ACM_Scale: 693.903888
```

Now the correct precision and number of eigenvalues to show are used
but only the L=0 eigenvalues are displayed.

break 12:30 pm

### 2:30 pm

I fixed 3 transcription errors in `Show_Eigs`.
The output format now is correct but the eigenvalues are still wrong.
```text
Lowest eigenvalue is -3045.21343. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    5.63,   41.84,  106.92,  915.30,  952.04, 1037.53]
  At L= 2: [    0.00,   14.49,   26.56,   60.33,   82.03,  135.01]
  At L= 3: [    5.64,   41.84,  106.92,  952.04, 1037.53, 1171.14]
  At L= 4: [    5.63,   14.49,   26.56,   41.84,   60.33,   82.03]
  At L= 5: [   14.49,   26.56,   60.33,   82.03,  135.01,  934.36]
  At L= 6: [    5.64,   14.49,   26.56,   41.84,   41.84,   60.33]
elapsed process time for ACM_Scale: 666.187861
```

The Maple result is:
```text
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
                                                                       elapsed := 7.946
```

Continue debugging with a simpler testcase.

```text
    ACM_set_defaults(0)
    ham = ACM_Hamiltonian(1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ACM_Scale(ham, S.One, Rational(5, 2), 0, 0, 0, 0, 0, 0)
```

Maple:
```text
Lowest eigenvalue is -2.50000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                [[[-2.50000000000000]], [], [0]]
```

Python:
```text
Lowest eigenvalue is -1.6496. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
```

Clearly, the eigenvalue is wrong.

Trace execution and compare results:
* `ACM_Scale`
* `ACM_ScaleOrAdapt`
* `DigXspace`
* ...
* `Parse_RadialOp_List` - found off-by-one index error

Python result now matches Maple result:
```text
Lowest eigenvalue is -2.5000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.16159599999999985
```

### 4:45 pm

Does this fix the error in Example 2.2?
Rerun Python code:
```text
Lowest eigenvalue is -3044.64466. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    5.63,   41.84,  106.92,  915.48,  952.22, 1037.70]
  At L= 2: [    0.00,   14.49,   26.56,   60.33,   82.02,  135.00]
  At L= 3: [    5.63,   41.84,  106.92,  952.22, 1037.70, 1171.30]
  At L= 4: [    5.63,   14.49,   26.56,   41.84,   60.33,   82.02]
  At L= 5: [   14.49,   26.56,   60.33,   82.02,  135.00,  934.54]
  At L= 6: [    5.63,   14.49,   26.56,   41.84,   41.84,   60.33]
elapsed process time for ACM_Scale: 654.9964600000001
```

The Python result is slightly different but still very wrong (and slow).

Try to recreate the error using Hamiltonians that contain just
one term, on the smallest Hilbert space.
The nonzero terms in `RWC_ham_fig5a` are:
* c11 = x1 - DONE
* c21 = x3
* c22 = x4
* c30 = x6
* c40 = x10 = kappa = 0 - Does nothing

Maple results:
```text
ACM_Scale(ham11, 1, 5/2, 0, 0, 0, 0, 0, 0);
Lowest eigenvalue is -2.50000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                [[[-2.50000000000000]], [], [0]]
ACM_Scale(ham21, 1, 5/2, 0, 0, 0, 0, 0, 0);
Lowest eigenvalue is 2.50000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                [[[2.50000000000000]], [], [0]]
ACM_Scale(ham22, 1, 5/2, 0, 0, 0, 0, 0, 0);
Lowest eigenvalue is 6.25000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                [[[6.25000000000000]], [], [0]]
ACM_Scale(ham30, 1, 5/2, 0, 0, 0, 0, 0, 0);
Lowest eigenvalue is 0.00000. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00]
                       [[[0.]], [], [0]]
```

Python results:
```text
Hamiltonian: ((1, (Radial_D2b,)), (-SENIORITY*(SENIORITY + 3) - 2, (Radial_bm2,)))
Lowest eigenvalue is -2.5000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.16646099999999997
Hamiltonian: ((1, (Radial_b2,)),)
Lowest eigenvalue is -1.1667. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0016480000000000938
Hamiltonian: ((1, (Radial_b2, Radial_b2)),)
Lowest eigenvalue is 3.4028. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0022099999999998232
Hamiltonian: ((4*pi/3, (Radial_b, SpHarm_310)),)
Lowest eigenvalue is 0.0000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.001651000000000069
```

Debug the `ham21 = ((1, (Radial_b2,)),)` case first. - IN-PROGRESS

Summary:
* c11 = x1 - OK
* c21 = x3 - error
* c22 = x4 - error
* c30 = x6 - OK

Continue at `RepXspace_Prod`

break 6:05 pm

## 2022-04-23

### 11:25 am

Debug the `ham21 = ((1, (Radial_b2,)),)` case first. - IN-PROGRESS
* Continue at `RepXspace_Prod`
* `RepXspace_Twin` should return `xsp_Mat =[2.500]`
* `RepRadial_Prod_rem` returned `Matrix([[-7/6]])`, should return `Matrix([[5/2]])`
* `RepRadial_Prod_common`
* `RepRadialshfs_Prod`returned `Matrix([[-7/6]])`, should return `Matrix([[5/2]])`
* `Mat = r_op.representation(anorm, lambda_run, R, nu_min, nu_max)` `Matrix([[-7/6]])`, should return `Matrix([[5/2]])`

break 12:20 pm

## 2022-04-24

### 10:00 am

Debug the `ham21 = ((1, (Radial_b2,)),)` case first. - IN-PROGRESS
* `Mat = r_op.representation(anorm, lambda_run, R, nu_min, nu_max)` 
  * r_op = {K: 2, T:0}
  * returns:`Matrix([[-7/6]])`, 
  * should return: `Matrix([[5/2]])`
  * calls `RepRadial_bS_DS(self.K, self.T, anorm, lambdaa, R, nu_min, nu_max)`
    * inspect code - why is `ME_Radial_D2b` called for the operator `Radial_b2`?

Found error.
Python now returns correct result:
```text
Hamiltonian: ((1, (Radial_b2,)),)
Lowest eigenvalue is 2.5000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0035570000000000324
```

Rerun all four cases.
```text
Hamiltonian: ((1, (Radial_D2b,)), (-SENIORITY*(SENIORITY + 3) - 2, (Radial_bm2,)))
Lowest eigenvalue is -2.5000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.1604319999999999
Hamiltonian: ((1, (Radial_b2,)),)
Lowest eigenvalue is 2.5000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0016780000000000683
Hamiltonian: ((1, (Radial_b2, Radial_b2)),)
Lowest eigenvalue is 15.6250. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0022290000000000365
Hamiltonian: ((4*pi/3, (Radial_b, SpHarm_310)),)
Lowest eigenvalue is 0.0000. Relative eigenvalues follow (each divided by 1.0000):
  At L= 0: [   0.00]
elapsed time: 0.0019540000000000113
```

Still wrong result for `ham22`:
```text
Hamiltonian: ((1, (Radial_b2, Radial_b2)),)
Lowest eigenvalue is 15.6250. Relative eigenvalues follow (each divided by 1.0000):
```
Lowest eigenvalue should be 6.25000. Debug `ham22`- TODO

Create tests for recent fixes: - IN-PROGRESS
* `RepRadial_bS_DS` - DONE

Tests have not discovered any errors in `RepRadial_bS_DS`.
* Continue tracing execution for `ham22` to locate error. - TODO

break 12:50 pm

### 3:55 pm

Create test cases for the simple hamiltonians. - DONE
Use `DigXspace`.

Tracing execution for `ham22`.
* Parse_RadialOp_List([Radial_b2, Radial_b2]) should return [[4,0]]
  * is returning [[4,0],[2,0]]
  * inspect code for `Parse_RadialOp_List` - DONE
  * create test cases for `Parse_RadialOp_List` - DONE
  * Found the error: final code block was indented too much and therefore in the loop!
  * All `Parse_RadialOp_List` tests pass now.
  * All tests pass now.

* Correct the type declarations for rbs_op in `RepRadial_Prod_rem` and its callers. - DONE
  * Should be tuple[Symbol,...], not list[Symbol] because its cached
  * Check args of all cached functions - arg should be immutable
  
Function signatures:
* def RepXspace_Twin(rad_ops: tuple[Symbol, ...] -> RepRadial_Prod_rem(tuple(rad_ops),
* def RepRadial_Prod_rem(rbs_op: list[Symbol] -> RepRadial_Prod_common(rbs_op
* def RepRadial_Prod_common(rbs_op: list[Symbol] -> Parse_RadialOp_List(rbs_op)
* def Parse_RadialOp_List(rs_op: list[Symbol]
* def RepRadial_Prod(rbs_op: list[Symbol] -> RepRadial_Prod_common(rbs_op
* def ME_Radial(radial_op: Expr -> RepRadial_Prod(op_prod,

Corrections:
* def RepXspace_Twin(rad_ops: tuple[Symbol, ...] -> RepRadial_Prod_rem(rad_ops,
* def RepRadial_Prod_rem(rbs_op: tuple[Symbol, ...] -> RepRadial_Prod_common(rbs_op
* def RepRadial_Prod_common(rbs_op: tuple[Symbol, ...] -> Parse_RadialOp_List(rbs_op)
* def Parse_RadialOp_List(rs_op: tuple[Symbol, ...]
* def ME_Radial(radial_op: Symbol -> RepRadial_Prod(op_prod,

mypy and pytest pass with no errors.

Rerun example 2.2.

Recall that the Maple result is:
```text
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
                                                                       elapsed := 7.946
```

The Python result is now:
```text
Lowest eigenvalue is -6.13099. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.55,    1.97,    2.86,    3.60,    4.03]
  At L= 2: [    0.11,    0.97,    1.77,    2.17,    2.38,    3.02]
  At L= 3: [    1.14,    2.70,    3.30,    4.56,    5.10,    5.35]
  At L= 4: [    0.30,    1.21,    1.90,    2.07,    2.39,    2.79]
  At L= 5: [    1.39,    2.21,    3.20,    3.60,    3.86,    4.44]
  At L= 6: [    0.61,    1.58,    2.34,    2.47,    2.79,    2.86]
elapsed process time for ACM_Scale: 687.323225
```

* Do the corrections give the expected Maple result?
  * The Python results are now very close to the Maple results, but too different to be explained by round-off error.
  * There is probably still a minor bug in the code.
* Has performance improved?
  * No. The Python code is still much slower: 687/8 = 86 times slower.
  * I strongly suspect that the bottleneck is using the SymPy Matrix functions for eigenvalues, inverses, and multiplication.
  * I expect NumPy to perform much better, but I really should profile the execution.
* Define a simpler test case that will allow debugging of the numeric differences. - TODO

break 7:10 pm

## 2022-04-25

### 11:20 am

Define a simpler test case that will allow debugging of the numeric differences. - DONE
* Increase the size of the truncated Hilbert space: try (0,1,0,1,0,1), and check each atomic Hamiltonian

The only error occurs for c11=1.

Maple eigenvalues:
```text
[-5.37082869331582, -1.62917130668418]
```

Python eigenvalues:
```text
[-4.774754878398197, -2.225245121601804]
```

Trace execution for c11=1 - TODO

break 12:40 pm

### 3:15 pm

Trace execution for c11=1 - IN-PROGRESS

The following call produces the wrong result.
```text
RepRadial_bS_DS(0, 2, 1, 5/2, 0, 0, 1)
```
* create test case - TODO

break 6:20 pm

### 7:45 pm

* create test case - IN-PROGRESS
```text
RepRadial_bS_DS(0, 2, 1, 5/2, 0, 0, 1)
```

Found error in call:
```text
ME_Radial_D2b(Rational(5,2),0,1)
```
Python returns:
```text
-4*sqrt(10)/15
```

Maple returns
```text
(7*sqrt(10))/30
```

Create test cases for `ME_Radial_D2b` - DONE

Fixed error in `ME_Radial_D2b`

All tests pass: 99 passed in 0.92s

All modules type check ok: Success: no issues found in 39 source files.

Does this fix the problem in Example 2.2?

Recall that the Maple result is:
```text
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
                                                                       elapsed := 7.946
```

The Python result is now:
```text
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
elapsed process time for ACM_Scale: 702.547779
```

The performance ratio = 703/8 = 88 times slower!

Profile the execution of the Python code to confirm that the bottleneck is in the SymPy matrix functions. - TODO

break 9:00 pm

## 2022-04-26

### 3:05 pm

Profile the execution of the Python code to confirm that the bottleneck is in the SymPy matrix functions. - DONE

Analyze stats. - IN-PROGRESS

break 5:30 pm

### 8:05 pm

With the profiler, execution time doubled:
```text
nu_max: 5, v_max: 18, L_max: 6
Lowest eigenvalue is -6.34376. Relative eigenvalues follow (each divided by 1.00000):
  At L= 0: [    0.00,    1.56,    1.99,    2.86,    3.61,    4.09]
  At L= 2: [    0.10,    0.97,    1.74,    2.19,    2.38,    3.05]
  At L= 3: [    1.11,    2.70,    3.32,    4.58,    5.12,    5.43]
  At L= 4: [    0.30,    1.23,    1.92,    2.08,    2.41,    2.80]
  At L= 5: [    1.41,    2.20,    3.22,    3.64,    3.89,    4.47]
  At L= 6: [    0.61,    1.58,    2.35,    2.49,    2.83,    2.88]
elapsed process time for ACM_Scale: 1600.625652
```

As expected, the most time was spent in the `mpmath` library.
```text
Tue Apr 26 17:14:05 2022    acm_scale_5_18_6_stats

         2858748085 function calls (2857025419 primitive calls) in 1626.970 seconds

   Ordered by: internal time
   List reduced from 1527 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
233803625  244.384    0.000  244.384    0.000 .../mpmath/libmp/libmpf.py:208(_normalize1)
163700301  177.221    0.000  338.970    0.000 .../mpmath/libmp/libmpf.py:884(python_mpf_mul)
142185223  174.084    0.000  237.372    0.000 .../mpmath/matrices/matrices.py:432(__getitem__)
 75628882  140.697    0.000  216.609    0.000 .../mpmath/matrices/matrices.py:497(__setitem__)
152046925  132.782    0.000  508.440    0.000 <string>:2(__mul__)
 90669756  120.841    0.000  268.107    0.000 .../mpmath/libmp/libmpf.py:702(mpf_add)
     3173  119.692    0.038 1086.391    0.342 .../mpmath/matrices/eigen.py:248(qr_step)
879476903/879373823  102.741    0.000  102.983    0.000 {built-in method builtins.isinstance}
 46542826   42.822    0.000  192.615    0.000 <string>:2(__add__)
 43961396   39.566    0.000  200.577    0.000 <string>:2(__sub__)
245624090   38.565    0.000   38.565    0.000 {built-in method __new__ of type object at 0x10ce04c70}
270392476   35.531    0.000   35.833    0.000 {built-in method builtins.hasattr}
       18   33.397    1.855  284.169   15.787 .../mpmath/matrices/eigen.py:45(hessenberg_reduce_0)
 87930448   30.990    0.000   59.619    0.000 .../mpmath/libmp/libintmath.py:91(python_bitcount)
 87930824   28.434    0.000   28.434    0.000 {built-in method _bisect.bisect_right}
 91710109   25.006    0.000   28.266    0.000 .../mpmath/ctx_mp_python.py:621(convert)
 43961419   18.787    0.000  148.516    0.000 .../mpmath/libmp/libmpf.py:797(mpf_sub)
 75667006   15.705    0.000   15.705    0.000 .../mpmath/ctx_mp_python.py:145(__nonzero__)
   114372   12.865    0.000   71.609    0.001 .../mpmath/ctx_mp_python.py:890(fdot)
       18   11.804    0.656  106.844    5.936 .../mpmath/matrices/eigen.py:150(hessenberg_reduce_1)
 13337660    8.821    0.000   13.579    0.000 .../mpmath/functions/functions.py:288(conj)
  7192353    6.935    0.000    6.940    0.000 .../mpmath/libmp/libmpf.py:153(_normalize)
 11429100    6.877    0.000   44.070    0.000 .../mpmath/matrices/matrices.py:583(<genexpr>)
       18    2.697    0.150   25.439    1.413 .../mpmath/matrices/eigen.py:552(eig_tr_r)
   114372    2.663    0.000    3.336    0.000 .../mpmath/libmp/libmpf.py:802(mpf_sum)
    98874    2.543    0.000    2.582    0.000 .../mpmath/rational.py:31(__new__)
1892121/1739578    2.027    0.000    4.576    0.000 .../sympy/core/sympify.py:92(sympify)
 13337660    1.756    0.000    1.756    0.000 .../mpmath/ctx_mp_python.py:129(<lambda>)
       18    1.706    0.095 1098.951   61.053 .../mpmath/matrices/eigen.py:383(hessenberg_qr)
94014/9522    1.519    0.000    9.402    0.001 .../sympy/simplify/powsimp.py:15(powsimp)
```

It is clear that most of the time is being spent in the mpmath library.
SymPy uses mpmath for Matrix operations.
SymPy matrices can hold arbitrary expressions so each matrix element is a Python object.
This means that access is slower than for a matrix that has elements of a fixed size.
NumPy supports matrices whose elements have a fixed size and can therefore
exploit optimized access.
* convert floating point Matrix operations to use NumPy - TODO
* perform profiling on a simpler test case: (5, 3, 3)

```text
Tue Apr 26 16:05:57 2022    acm_scale_5_3_3_stats
         18242704 function calls (17662043 primitive calls) in 10.356 seconds
   Ordered by: internal time
   List reduced from 1507 to 30 due to restriction <30>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
38067/3849    0.542    0.000    3.363    0.001 .../sympy/simplify/powsimp.py:15(powsimp)
441548/440226    0.444    0.000    0.922    0.000 .../sympy/core/sympify.py:92(sympify)
668689/624634    0.442    0.000    1.971    0.000 .../sympy/core/cache.py:69(wrapper)
2909461/2867280    0.438    0.000    0.505    0.000 {built-in method builtins.isinstance}
   308236    0.270    0.000    0.270    0.000 .../mpmath/libmp/libmpf.py:208(_normalize1)
123442/123327    0.214    0.000    0.487    0.000 .../sympy/core/expr.py:144(__eq__)
31225/8137    0.194    0.000    0.343    0.000 .../sympy/core/compatibility.py:315(default_sort_key)
   203971    0.187    0.000    0.364    0.000 .../mpmath/libmp/libmpf.py:884(python_mpf_mul)
   169310    0.179    0.000    0.248    0.000 .../mpmath/matrices/matrices.py:432(__getitem__)
   697437    0.172    0.000    0.224    0.000 {built-in method builtins.getattr}
    97458    0.166    0.000    0.257    0.000 .../mpmath/matrices/matrices.py:497(__setitem__)
   627912    0.163    0.000    0.224    0.000 .../sympy/core/numbers.py:2294(__hash__)
   187985    0.150    0.000    0.551    0.000 <string>:2(__mul__)
5809/5611    0.150    0.000    0.529    0.000 .../sympy/core/mul.py:178(flatten)
239685/238713    0.146    0.000    0.750    0.000 .../sympy/core/sympify.py:479(_sympify)
      241    0.145    0.001    1.333    0.006 .../mpmath/matrices/eigen.py:248(qr_step)
   114987    0.142    0.000    0.301    0.000 .../mpmath/libmp/libmpf.py:702(mpf_add)
   234345    0.137    0.000    0.185    0.000 .../sympy/core/numbers.py:807(__hash__)
   233112    0.135    0.000    0.319    0.000 .../sympy/core/numbers.py:1978(__hash__)
43646/19733    0.130    0.000    0.813    0.000 .../sympy/core/compatibility.py:501(ordered)
547729/526291    0.118    0.000    0.146    0.000 .../sympy/core/expr.py:126(__hash__)
   816724    0.114    0.000    0.117    0.000 {built-in method builtins.hasattr}
    58271    0.114    0.000    0.247    0.000 .../sympy/core/numbers.py:1876(__eq__)
     5781    0.106    0.000    0.245    0.000 .../sympy/core/facts.py:499(deduce_all_facts)
31144/8050    0.104    0.000    0.210    0.000 .../sympy/core/compatibility.py:479(_nodes)
219237/83601    0.099    0.000    0.127    0.000 .../sympy/core/basic.py:2065(_preorder_traversal)
23025/6418    0.087    0.000    0.555    0.000 .../sympy/core/exprtools.py:1224(do)
   198315    0.080    0.000    0.110    0.000 <frozen importlib._bootstrap>:404(parent)
     7602    0.078    0.000    0.388    0.000 .../sympy/core/function.py:2882(expand_log)
    16784    0.078    0.000    0.814    0.000 .../sympy/core/basic.py:1241(replace)
```

The profile for the simpler test case is very different. Here the mpmath library is not the most time-consuming.
* increase the dimensions of the simple test case so that it runs in a few minutes and shows the mpmath bottleneck
  * mpmath becomes the bottleneck for (nu_max, v_max, L_max) = (5, 6, 6) which runs in 26/56 seconds
* continue measurements - DONE
* run all tests and mypy, then tag the current branch as stable v1.0 - TODO
* create a new branch for numpy - TODO
* review numpy docs - TODO

break 10:10 pm

## 2022-04-27

### 10:30 am

* scan code for TODO comments and fix if important or easy - IN-PROGRESS
* run all tests and mypy, then tag the current branch as stable v1.0 - TODO
* create a new branch for numpy - TODO
* review numpy docs - DONE

break 12:35 am

### 3:10 pm

* scan code for TODO comments and fix if important or easy - DONE

What type should `Mel` be in:
```text
def quad_amp_fun(Li: nonnegint, Lf: nonnegint, Mel) -> Expr:
```

* Look at call chain:
  * glb_rat_fun is set to quad_amp_fun
  * Show_Mels sets mel_fun to g.glb_rat_fun as default
  * Show_Mels uses mel_fun(L1, L2, TR_matrix[n2 - 1, n1 - 1])
  * Show_Mels calls Show_Mels_Row(Melements, Lvals, L1, L2, rate_ent[2], toshow, mel_fun, scale)
  * Show_Mels calls Show_Mels_Rows(Melements, Lvals, L2, toshow, mel_fun, scale)
  * Show_Mels_Row calls mel_fun(L1, L2, TR_matrix[n2 - 1, n1 - 1])
  * Show_Mels_Rows calls Show_Mels_Row(Melements, Lvals, L1, L2, n2, toshow, mel_fun, scale)
* What type are the elements of TR_matrix?
  * The elements should be floats.
  * At present, they are usually the result of applying the evalf() method
  * The result of .evalf() could be a sympy Float or general Expr object (if the object cannot be evaluated)
  * Going forward, I am going to assume that the result MUST be numeric
  * Therefore, use the float() function instead of evalf() since an exception will be thrown if the object is not numeric
  * Furthermore, since Mel is a float, the result should also be a float
```text
def quad_amp_fun(Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
```

* run all tests and mypy - DONE
* commit latest changes - DONE
* tag the current branch as v1-0-0 - DONE
* create a new branch for numpy - TODO

