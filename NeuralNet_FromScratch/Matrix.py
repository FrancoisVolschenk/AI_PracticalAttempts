from random import randint, random

class Matrix:
    """This class represents the concept of a matrix with linear algebra based matrix operations"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data = []

        # initialize to 0
        for r in range(self.rows):
            self.data.append([])
            for c in range(self.cols):
                self.data[r].append(0.0)

    @staticmethod
    def multiply(m1, m2):
        """This method returns the result of matrix multiplication"""
        if m2.rows != m1.cols:
            raise Exception("The dimensions of the operands do not match. M2's rows must equal M1's columns")
        result = Matrix(m1.rows, m2.cols)
        for r in range(result.rows):
            for c in range(result.cols):
                sum = 0
                for innerC in range(m1.cols):
                    sum += m1.data[r][innerC] * m2.data[innerC][c]
                result.data[r][c] = sum
        return result
    
    @staticmethod
    def fromArray(arr: list):
        """This method takes in a list and returns the matrix representation of the list"""
        rows = len(arr)
        cols = 1
        if rows != 0 and type(arr[0]) == list:
            cols = len(arr[0])
        result = Matrix(rows, cols)
        if cols != 1:
            for r in range(rows):
                for c in range(cols):
                    result.data[r][c] = arr[r][c]
        else:
            for r in range(rows):
                result.data[r][0] = arr[r]
        return result
    
    @staticmethod
    def toArray(m1):
        """This method returns a list equivalent of a matrix"""
        result = []
        if m1.cols != 1:
            for r in range(m1.rows):
                result.append([])
                for c in range(m1.cols):
                    result[r].append(m1.data[r][c])
        else:
            for r in range(m1.rows):
                result.append(m1.data[r][0])

        return result
    
    @staticmethod
    def Subtract(m1, m2):
        """Element wise subtraction without modifying the operands"""
        if m1.rows != m2.rows or m1.cols != m2.cols:
            raise Exception("The dimensions of the matrices do not match")
        result = Matrix(m1.rows, m1.cols)
        for r in range(m1.rows):
            for c in range(m1.cols):
                result.data[r][c] = m1.data[r][c] - m2.data[r][c]

        return result
    
    def scale(self, scalar: float):
        """Scalar multiplication"""
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] *= scalar  

    def elemMultiply(self, other):
        """Element wise multiplication"""
        if other.rows != self.rows or other.cols != self.cols:
            raise Exception("The dimensions of the matrices do not match")
        
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] *= other.data[r][c]

    def add(self, operand):
        """Element wise addition, or a scalar based addition if a single value is given"""
        if type(operand) == Matrix:
            if operand.rows != self.rows or operand.cols != self.cols:
                raise Exception("Operand dimensions do not match. Matrices must have same dimensions")
            for r in range(self.rows):
                for c in range(self.cols):
                    self.data[r][c] += operand.data[r][c]
        else:
            for r in range(self.rows):
                for c in range(self.cols):
                    self.data[r][c] += operand      

    def transpose(self, matrix = None):
        """Simple matrix transposition
        if no matrix was passed through, the matrix that it was called from is modified
        otherwise the matrix remains uncanged and a new matrix is returned"""
        result = Matrix(self.cols, self.rows)
        for r in range(self.rows):
            for c in range(self.cols):
                result.data[c][r] = self.data[r][c]
        if matrix is not None:
            return result
        else:
            self.data = result.data
            self.rows, self.cols = self.cols, self.rows

    def randomize(self):
        """Fill the matrix with random values"""
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] = randint(-1, 1) + random()

    def map(self, fn, matrix = None):
        """Apply a given function to all values in the matrix
        If no matrix is passed as a parameter, the matrix from which the method was called will be modified"""
        if matrix is None:
            for r in range(self.rows):
                for c in range(self.cols):
                    self.data[r][c] = fn(self.data[r][c])
        else:
            result = Matrix(self.rows, self.cols)
            for r in range(self.rows):
                for c in range(self.cols):
                    result.data[r][c] = fn(self.data[r][c])
            return result

    def __repr__(self):
        """Print the matrix to the console"""
        output = ""
        for r in range(self.rows):
            for c in range(self.cols):
                output += f"| {self.data[r][c]} "
            output += "|\n"
        return output

