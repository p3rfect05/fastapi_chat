class Solution:
    def generateMatrix(self, n: int) -> list[list[int]]:
        matrix = [[0] * n for _ in range(n)]
        i = 0
        j = 0
        k = 1
        while k < n * n:
            # left to right
            print(i, j, k, n * n)
            while True:
                #print(i, j, k)
                matrix[i][j] = k
                if j < n - 1:
                    if matrix[i][j + 1] != 0:
                        break
                    j += 1
                else:
                    break
                k += 1

            # up - down
            while True:
                matrix[i][j] = k
                if i < n - 1:
                    if matrix[i + 1][j] != 0:
                        break
                    i += 1
                else:
                    break
                k += 1
            while True:
                matrix[i][j] = k

                if j > 0:
                    if matrix[i][j - 1] != 0:
                        break
                    j -= 1
                else:
                    break
                k += 1
            # up - down

            while True:
                matrix[i][j] = k
                if i > 0:
                    if matrix[i - 1][j] != 0:
                        break
                    i -= 1
                else:
                    break
                k += 1
            #print(i, j, k)
        return matrix

print(Solution().generateMatrix(3))