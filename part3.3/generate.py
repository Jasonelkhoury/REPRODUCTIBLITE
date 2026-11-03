from pathlib import Path

from jinja2 import Template

ROOT = Path(__file__).resolve().parent.parent

PYTHON_TEMPLATE_PATH = ROOT / "property_template.py.jinja"
JAVA_TEMPLATE_PATH = ROOT / "property_template.java.jinja"

OUTPUT_DIR = ROOT / "part3.3" / "generated"

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

# Python numeric types
PYTHON_TYPES = {
    "float32": {
        "numeric_type": "PythonFloat32",
    },
    "float64": {
        "numeric_type": "PythonFloat64",
    },
}

# Java numeric types
JAVA_TYPES = {
    "float32": {
        "type_name": "float",
        "type_label": "float32",
    },
    "float64": {
        "type_name": "double",
        "type_label": "float64",
    },
}


def main():
    python_template = Template(
        PYTHON_TEMPLATE_PATH.read_text(encoding="utf-8")
    )

    java_template = Template(
        JAVA_TEMPLATE_PATH.read_text(encoding="utf-8")
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate Python variants
    for property_name, (lhs, rhs) in PROPERTIES.items():
        for type_name, type_config in PYTHON_TYPES.items():

            variant_name = f"{property_name}_{type_name}"
            output_path = OUTPUT_DIR / f"{variant_name}.py"

            generated_code = python_template.render(
                property_name=property_name,
                lhs=lhs,
                rhs=rhs,
                numeric_type=type_config["numeric_type"],
                random_generator="PythonRandom",
                repetitions=REPETITIONS,
                seed=SEED,
                min_value=MIN_VALUE,
                max_value=MAX_VALUE,
            )

            output_path.write_text(
                generated_code,
                encoding="utf-8",
            )

            print(f"Generated: {output_path.relative_to(ROOT)}")

    # Generate Java variants
    for property_name, (lhs, rhs) in PROPERTIES.items():
        for type_name, type_config in JAVA_TYPES.items():

            variant_name = f"{property_name}_{type_name}"

            # Java public class name must match the filename
            class_name = "".join(
                part.capitalize()
                for part in variant_name.split("_")
            )

            output_path = OUTPUT_DIR / f"{class_name}.java"

            generated_code = java_template.render(
                property_name=property_name,
                class_name=class_name,
                lhs=lhs,
                rhs=rhs,
                type_name=type_config["type_name"],
                type_label=type_config["type_label"],
                random_generator="JavaRandom",
                repetitions=REPETITIONS,
                seed=SEED,
                min_value=MIN_VALUE,
                max_value=MAX_VALUE,
            )

            output_path.write_text(
                generated_code,
                encoding="utf-8",
            )

            print(f"Generated: {output_path.relative_to(ROOT)}")

    print(f"\nSuccessfully generated 8 variants in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()