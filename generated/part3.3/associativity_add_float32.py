import json
import random
import numpy as np

PROPERTY = "associativity_add"
REPETITIONS = 10000
SEED = 152
MIN_VALUE = 0.0
MAX_VALUE = 1.0

# Numeric type selection

NUMBER_TYPE = np.float32
TYPE_LABEL = "float32"


# Random generator selection

rng = random.Random(SEED)



def check_property():
    equal_count = 0

    for _ in range(REPETITIONS):
        x = NUMBER_TYPE(rng.uniform(MIN_VALUE, MAX_VALUE))
        y = NUMBER_TYPE(rng.uniform(MIN_VALUE, MAX_VALUE))
        z = NUMBER_TYPE(rng.uniform(MIN_VALUE, MAX_VALUE))

        if (x + y) + z == x + (y + z):
            equal_count += 1

    different_count = REPETITIONS - equal_count

    return {
        "property": PROPERTY,
        "type": TYPE_LABEL,
        "random_generator": "PythonRandom",
        "repetitions": REPETITIONS,
        "seed": SEED,
        "min_value": MIN_VALUE,
        "max_value": MAX_VALUE,
        "equal_count": equal_count,
        "different_count": different_count,
        "percentage": 100.0 * equal_count / REPETITIONS,
    }


if __name__ == "__main__":
    print(json.dumps(check_property()))