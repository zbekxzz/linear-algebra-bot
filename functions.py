import json                       # to read JSON files
import random                     # to get random quote from list
from pytube import YouTube        # to download videos from YouTube
import os                         # to rename and delete files
import numpy as np

def get_random_quote():
    # Open and read quotes from JSON file
    with open('json/quotes.json') as rfile:
        quotes = json.load(rfile)
    
    # Get random quote to send user
    r = random.randint(1, 50)
    return f"`Your quote:`\n*{quotes[str(r)]}*"

def get_tutorials_list():
    list = """I have tutorials for these themes:
    
*Chapter 1. Linear Equations in Linear Algebra*

*1.1.1* Systems of Linear Equations
*1.1.2* Solve Systems of Linear Equations in Augmented Matrices Using Row Operations
*1.2.1* Row Reduction and Echelon Forms
*1.2.2* Solution Sets and Free Variables
*1.3.1* Vector Equations
*1.3.2* Linear Combinations
*1.4.1* The Matrix Equation Ax=b
*1.4.2* Computation of Ax
*1.5.1* Homogeneous System Solutions
*1.5.2* Non-Homogeneous System Solutions
*1.6.1* Applications of Linear Systems - Economic Sectors
*1.6.2* Applications of Linear Systems - Network Flow
*1.7.1* Linear Independence
*1.7.2* Special Ways to Determine Linear Independence
*1.8.1* Matrix Transformations
*1.8.2* Introduction to Linear Transformations
    
*Chapter 2. Matrix Algebra*

*2.1.1* Matrix Operations - Sums and Scalar Multiples
*2.1.2* Matrix Operations - Multiplication and Transpose
*2.2.1* The Inverse of a Matrix
*2.2.2* Solving 2x2 Systems with the Inverse and Inverse Properties
*2.2.3* Elementary Matrices And An Algorithm for Finding A Inverse
*2.3.1* Characterizations of Invertible Matrices

*Chapter 3. Determinants*

*3.1.1* Introduction to Determinants
*3.1.2* Co-factor Expansion
*3.2.1* Properties of Determinants

*Chapter 4. Vector Spaces*

*4.1.1* Vector Spaces
*4.1.2* Subspace of a Vector Space
*4.2.1* Null Spaces
*4.2.2* Column Spaces
*4.3.1* Linearly Independent Sets and Bases
*4.3.2* The Spanning Set Theorem
*4.5.1* The Dimension of a Vector Space
*4.5.2* Subspaces of a Finite Dimensional Space
*4.6.1* The Row Space
*4.6.2* Rank

*Chapter 5. Eigenvectors and Eigenvalues*

*5.1.1* Eigenvectors and Eigenvalues
*5.1.2* More About Eigenvectors and Eigenvalues
*5.2.1* Determinants and the IMT
*5.2.2* The Characteristic Equation

*Chapter 6. Orthogonality and Least Squares*

*6.1.1* Inner Product, Vector Length and Distance
*6.1.2* Orthogonal Vectors
*6.2.1* Orthogonal Sets
*6.2.2* Orthogonal Projections
*6.3.1* Orthogonal Decomposition Theorem
*6.3.2* The Best Approximation Theorem
*6.5.1* Least Squares Problems
"""
    return list

def get_calc_commands():
    commands = """*At this moment I have such functions:*

/determinant  -  _finding a determinants of a matrix_
/rank  -  _finding a rank of a matrix_
/eigenvalue  -  _finding an eigenvalue of a matrix_
/eigenvector  -  _finding an eigenvectors of a matrix_

Other features under developing...
"""
    return commands
    
def get_video_link(message):
    # Deleting downloaded video if exists to maintain empty space on disk
    files = os.listdir("""C:/Users/bq/Desktop/algebraBot2""")
    video = [_ for _ in files if _[-4:] == ".mp4"]
    if len(video) == 1:
        os.remove(video[0])
    
    # Open and read links of tutorial videos from JSON file 
    with open("json/links.json") as rfile:
        links = json.load(rfile)

    # Download tutorial video from YouTube 
    yt = YouTube(links[message[6:]])
    ys = yt.streams.get_highest_resolution()
    ys.download()

    # Rename downloaded video to get short name and easy to send
    files = os.listdir("""C:/Users/bq/Desktop/algebraBot2""")
    video = [_ for _ in files if _[-4:] == ".mp4"]
    os.rename(video[0], f"{message[6:]}.mp4")
    return f"C:/Users/bq/Desktop/algebraBot2/{message[6:]}.mp4"

def get_random_task(rand_task):
    with open('json/assignments.json') as rfile:
        tasks = json.load(rfile)
    number = random.randint(1, len(tasks[rand_task]))
    return tasks[rand_task][f"{number}"]

def find_determinant(dim, arr):
    dim = dim.split(" ")
    R = int(dim[0])
    num = list(map(int, arr.split()))
    matrix = np.array(num).reshape(R, R)
    return f"The inserted matrix is square and Determinant is "'{0:.0f}'.format(np.linalg.det(matrix))

def find_rank(dim, arr):
    dim = dim.split(" ")
    R = int(dim[0])
    C = int(dim[1])
    num = list(map(int, arr.split()))
    matrix = np.array(num).reshape(R, C)
    return f"The inserted matrix's rank is {np.linalg.matrix_rank(matrix)}"

def find_eigenvalue(dim, arr):
    dim = dim.split(" ")
    R = int(dim[0])
    C = int(dim[1])
    num = list(map(int, arr.split()))
    matrix = np.array(num).reshape(R, C)
    eigs = np.linalg.eigvals(matrix)
    str = ""
    for i in range(len(eigs)):
        str += f"{eigs[i]:.3f}"
    return f"The inserted matrix's eigenvalue is {str}"

def find_eigenvector(dim, arr):
    dim = dim.split(" ")
    R = int(dim[0])
    C = int(dim[1])
    num = list(map(int, arr.split()))
    matrix = np.array(num).reshape(R, C)
    value, vector = np.linalg.eig(matrix)
    str = ""
    for i in range(2):
        row = ""
        for j in range(2):
            row += f"| {vector[i][j]:.3f} "
        row += "|\n"
        str += row
    return str