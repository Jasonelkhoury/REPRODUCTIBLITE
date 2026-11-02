import random
import csv
from decimal import Decimal, getcontext
class tp1:
    def ex1(self): 
        REPETITIONS = [100, 1_000, 10_000, 100_000, 1_000_000]
        MIN_VALUE = 0
        MAX_VALUE = 1

        with open("answer_associativity.txt", "w") as file:

            for number_of_tests in REPETITIONS:
                random.seed(152)
                equal_count = 0

                for _ in range(number_of_tests):
                    x = random.uniform(MIN_VALUE, MAX_VALUE)
                    y = random.uniform(MIN_VALUE, MAX_VALUE)
                    z = random.uniform(MIN_VALUE, MAX_VALUE)

                    if (x+y)+z==x+(y+z):
                        equal_count += 1

                different_count = number_of_tests - equal_count
                percentage = equal_count / number_of_tests * 100

                file.write(f"Number of tests: {number_of_tests}\n")
                file.write(f"Equal results: {equal_count}\n")
                file.write(f"Different results: {different_count}\n")
                file.write(f"Percentage of equality: {percentage:.6f}%\n\n")
        
    
    

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
    #tp1.ex2()

    