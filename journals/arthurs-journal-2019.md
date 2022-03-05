# Arthur's Journal 2019

## 2019-12-08

### 8:28 AM

#### Recap

I started this project on 2019-06-24 after a conversation
with David Rowe.
David said that he had published a Maple program that
performed Algebraic Collective Model (ACM) computations in 2016,
but few other researchers were using it.
David thought that that main obstacle to adoption
was that Maple required the purchase of a licence.
David expressed a desired to see the program reimplemented in 
freely available computer language.
Since I was looking for a way to get re-engaged in math and physics,
I offerred to take on the task.

David published the ACM program in the journal Computer Physics
Communications (CPC).
I searched the CPC program library and found that Python was the most
popular language.
The Maple ACM program did both symbolic and numerical
computation so next I confirmed that Python had this capability.
The numerical computations were done to find the eigenvalues 
of the Hamiltonian matrix and used an industry standard Fortran library.
This same library was available in the Python numpy package.
Symbolic computation can be done in Python using the SymPy package. 
Furthermore, Maple notebooks could be replaced by Python Jupyter notebooks.
I therefore recommended that we select Python as the target language.

I gathered all the Maple code and stored it in the GitHub repository
named acm14.
This repo contains both version 16 and 1.4 which is the published version.
I collected relevant publications there too.

David generously purchased a Maple licence for me.
I was able to run the Maple code.

I then created the acmpy repo to store the Python code.

### 8:47 AM - break

---

## 2019-12-09

### 5:08 PM

The ACM makes use of pre-computed SO(5) > SO(3) Clebsch-Gordan coefficients
that are stored in disk files.
My first Python programming goal is to read these files.
I created so5cg.py for that purpose.

### 5:13 PM break

---

## 2019-12-14

### 10:57 AM
- implement so5cg.py
- use regex
- see <https://docs.python.org/3/howto/regex.html#regex-howto>
- read this article
- coded parsing function parse_v2
- next <https://docs.python.org/3/howto/regex.html#grouping>

### 12:18 PM - break

---

### 1:03 PM
- continue reading


### 2:39 PM
- finished regex article
- work on parsing a single line of the data file
- does Python have C-line scanf?
- no, but I can split the line by whitespace using the re.split() function
- trim the leading leading and trailing whitespace using string strip() function
- convert to float and int using float() and int()

### 3:00 PM - break

###8:38 PM
- continue parsing line of file
- done
- read file and parse lines
- done

### 9:51 PM - break

---

## 2019-12-15

### 4:12 PM

- continue coding so5cg.py
- I implemented loading of all the files into a dictionary
- it takes around 1 minute to load all CG files
- change this to lazy loading since some calculations won't need all the files
- just scan the directories initially and save the Path in the dictionary
- on a request to retrieve the CG coefficient, check the existence of the Path entry on load it, 
replacing the Path with the CG values loaded from the file
- done loading just the file paths, this is very fast
- next implement the retrieval operation
- the theory behind the calculation is described in 
Construction of SO(5) ⊃ SO(3) spherical harmonics and 
Clebsch–Gordan coefficients by M.A. Caprio , D.J. Rowe , T.A. Welsh
- that paper gives Mathematica code and some calculated values
- Welsh calculated the values provided here with unpublished C++ code
- skim the paper
- read the Maple code to understand the API
