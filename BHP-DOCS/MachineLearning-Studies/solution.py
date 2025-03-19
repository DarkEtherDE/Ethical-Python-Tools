#This is a demo task.
#
#Write a function:

#def solution(A)

#that, given an array A of N integers, returns the smallest positive integer (greater than 0) that does not occur in A.

#For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.

#Given A = [1, 2, 3], the function should return 4.

#Given A = [−1, −3], the function should return 1.

#Write an efficient algorithm for the following assumptions:

#N is an integer within the range [1..100,000];

def solution(N):
    values = [2, 3, 5]
    chars = ['C', 'O', 'D', 'I', 'L', 'I', 'T', 'Y']
    string = ''
    
    for i in values: 
        while N % i == 0:
            N //= i
            string += chars[0]  # Append the first character to uncovered_chars
            chars = chars[1:]  # Remove the first character from chars
            return chars
            


print(solution(49))