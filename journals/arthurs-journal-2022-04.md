# Arthur's Journal 2022-04

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
