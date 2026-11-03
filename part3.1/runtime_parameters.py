import random
import csv
from decimal import Decimal, getcontext
class runtime_parameters:
    def ex1(self): 
        REPETITIONS = [100, 1_000, 10_000, 100_000, 1_000_000]
        MIN_VALUE = 0
        MAX_VALUE = 1

        with open("answer_associativity_runtime_parameters.txt", "w") as file:

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
        

if __name__ == "__main__":
    runtime_parameters = runtime_parameters()
    runtime_parameters.ex1()

    