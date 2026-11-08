import random
import csv
from decimal import Decimal, getcontext
import argparse
class cli:
    @staticmethod
    def ex1(repetitions=1000, seed=152, min_value=0.0, max_value=1.0):
        rng = random.Random(seed)
        equal_count = 0

        for _ in range(repetitions):
            x = rng.uniform(min_value, max_value)
            y = rng.uniform(min_value, max_value)
            z = rng.uniform(min_value, max_value)

            if (x+y)+z==x+(y+z):
                equal_count += 1

        different_count = repetitions - equal_count
        percentage = equal_count / repetitions * 100
        
        with open("part3.2/answer_associativity_cli.txt", "w") as file:
            file.write(f"Number of tests: {repetitions}\n")
            file.write(f"Min value: {min_value}\n")
            file.write(f"Max value: {max_value}\n")
            file.write(f"Equal results: {equal_count}\n")
            file.write(f"Different results: {repetitions - equal_count}\n")
            file.write(f"Percentage of equality: {percentage:.6f}%\n")

        return {
            "repetitions": repetitions,
            "seed": seed,
            "min_value": min_value,
            "max_value": max_value,
            "equal_count": equal_count,
            "different_count": different_count,
            "percentage": percentage,
        }
              
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
    description="Floating-point associativity experiment"
)
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=152)
    parser.add_argument("--min-value", type=float, default=0.0)
    parser.add_argument("--max-value", type=float, default=1.0)

    args = parser.parse_args()
    cli = cli()
    result = cli.ex1(
        repetitions=args.repetitions,
        seed=args.seed,
        min_value=args.min_value,
        max_value=args.max_value,
    )
    #tp1.ex2()

    