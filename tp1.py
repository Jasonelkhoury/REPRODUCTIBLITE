import random
import csv
from decimal import Decimal, getcontext
class tp1:
    def ex1(self):
        NUMBER_OF_TESTS = 1_000
        MIN_VALUE = 0
        MAX_VALUE = 1
        random.seed(152)

        equal_count = 0
       
        for _ in range(1, NUMBER_OF_TESTS+1):
            x = random.uniform(MIN_VALUE,MAX_VALUE)
            y = random.uniform(MIN_VALUE,MAX_VALUE)
            z = random.uniform(MIN_VALUE,MAX_VALUE)
            if (x+y)+z==x+(y+z):
                equal_count+=1
                
        percentage = equal_count / NUMBER_OF_TESTS * 100
        with open("answer_associativity.txt", "w") as file:
            file.write(f"Number of tests: {NUMBER_OF_TESTS}\n")
            file.write(f"Equal results: {equal_count}\n")
            file.write(f"Different results: {NUMBER_OF_TESTS - 1 - equal_count}\n")
            file.write(f"Percentage of equality: {percentage:.6f}%\n")
        
    
    

    @staticmethod
    def ex2(n=50, precision=100):
        getcontext().prec = precision
        u = Decimal(1).exp()

        for k in range(1, n + 1):
            u = (u - 1) * Decimal(k)

        final_balance = u - 1
        with open("answer_banking.txt", "w") as file:
            file.write(f"Initial balance: {Decimal(1).exp()}\n")
            file.write(f"Number of years: {n}\n")
            file.write(f"Decimal precision: {precision} digits\n")
            file.write(f"Final balance: {final_balance}\n")

          
        

if __name__ == "__main__":
    tp1 = tp1()
    tp1.ex1()
    tp1.ex2()

    