import subprocess
import sys
from pathlib import Path

from jinja2 import Template

ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT / "property_template.py.jinja"
OUTPUT_DIR = ROOT / "generated"

REPETITIONS = 10_000
SEED = 152
MIN_VALUE = 0.0
MAX_VALUE = 1.0

PROPERTIES = {
    "associativity_add": (
        "(x + y) + z",
        "x + (y + z)",
    ),
    "distributivity": (
        "x * (y + z)",
        "x * y + x * z",
    ),
}

TYPES = {
    "float32": "np.float32",
    "float64": "np.float64",
}


def main():
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(exist_ok=True)

    for property_name, (lhs, rhs) in PROPERTIES.items():
        for type_name, type_expression in TYPES.items():

            variant_name = f"{property_name}_{type_name}"
            output_path = OUTPUT_DIR / f"{variant_name}.py"

            generated_code = template.render(
                property_name=property_name,
                lhs=lhs,
                rhs=rhs,
                type_name=type_expression,
                repetitions=REPETITIONS,
                seed=SEED,
                min_value=MIN_VALUE,
                max_value=MAX_VALUE,
            )

            output_path.write_text(generated_code, encoding="utf-8")

            print(f"\n--- {variant_name} ---")

            result = subprocess.run(
                [sys.executable, str(output_path)],
                capture_output=True,
                text=True,
                check=True,
                cwd=ROOT,
            )

            print(result.stdout.strip())


if __name__ == "__main__":
    main()
