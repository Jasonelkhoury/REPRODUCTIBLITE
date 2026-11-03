import csv
import json
import re
import shlex
import subprocess
import sys

from pathlib import Path
from jinja2 import Template


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
PART6_DIR = Path(__file__).resolve().parent

SAMPLE_PATH = ROOT / "configs" / "sample.csv"

PYTHON_TEMPLATE_PATH = ROOT / "property_template.py.jinja"
JAVA_TEMPLATE_PATH = ROOT / "property_template.java.jinja"

GENERATED_DIR = PART6_DIR / "generated"
RESULTS_PATH = PART6_DIR / "results.csv"


# ============================================================
# EXPERIMENT PARAMETERS
# ============================================================

RUNS_PER_CONFIGURATION = 5

# Chaque exécution utilise une graine différente :
# seed, seed + 1, seed + 2, etc.
VARY_SEED_PER_RUN = True


# ============================================================
# DOCKER IMAGES
# ============================================================

DOCKER_IMAGES = {
    "CPython": "repro-cpython:3.12",
    "PyPy": "repro-pypy:3.12",
    "OpenJDK": "repro-openjdk:21",
    "GraalVM": "repro-graalvm:21",
}


# ============================================================
# VARIABILITY FACTORS
# ============================================================

REPETITIONS = {
    "Tests100": 100,
    "Tests1000": 1_000,
    "Tests10_000": 10_000,
    "Tests100_000": 100_000,
    "Tests1_000_000": 1_000_000,
}

INTERVALS = {
    "Interval01": (0.0, 1.0),
    "Interval1_000_000": (-1_000_000.0, 1_000_000.0),
}

SEEDS = {
    "Seed42": 42,
    "Seed152": 152,
}

PROPERTIES = {
    "Associativity": {
        "name": "associativity_add",
        "lhs": "(x + y) + z",
        "rhs": "x + (y + z)",
    },
    "Distributivity": {
        "name": "distributivity",
        "lhs": "x * (y + z)",
        "rhs": "x * y + x * z",
    },
}

PYTHON_TYPES = {
    "PythonFloat32": {
        "numeric_type": "PythonFloat32",
        "label": "float32",
    },
    "PythonFloat64": {
        "numeric_type": "PythonFloat64",
        "label": "float64",
    },
}

JAVA_TYPES = {
    "JavaFloat": {
        "type_name": "float",
        "label": "float32",
    },
    "JavaDouble": {
        "type_name": "double",
        "label": "float64",
    },
}

PYTHON_GENERATORS = {
    "PythonRandom",
    "PythonNumPyRandom",
}

JAVA_GENERATORS = {
    "JavaRandom",
    "JavaSplittableRandom",
}


# ============================================================
# CONFIGURATION EXTRACTION
# ============================================================

def selected_feature(row, candidates):
    """
    Find the selected feature among the CSV row values.

    Supports:
    - A selected feature appearing as a cell value.
    - A feature column containing True, 1, yes or selected.
    """

    values = {
        str(value).strip()
        for value in row.values()
        if value is not None
    }

    for candidate in candidates:
        if candidate in values:
            return candidate

        column_value = str(row.get(candidate, "")).strip().lower()

        if column_value in {"true", "1", "yes", "selected"}:
            return candidate

    raise ValueError(
        f"No selected feature found among: {candidates}\n"
        f"CSV row: {row}"
    )


def extract_configuration(row):
    """Extract all variability factors from a sample.csv row."""

    # Language
    language = selected_feature(row, ["Python", "Java"])

    # Execution environment
    if language == "Python":
        environment = selected_feature(row, ["CPython", "PyPy"])
    else:
        environment = selected_feature(row, ["OpenJDK", "GraalVM"])

    # Property
    property_feature = selected_feature(
        row,
        ["Associativity", "Distributivity"],
    )

    property_config = PROPERTIES[property_feature]

    # Repetitions
    repetitions_feature = selected_feature(
        row,
        list(REPETITIONS.keys()),
    )

    repetitions = REPETITIONS[repetitions_feature]

    # Interval
    interval_feature = selected_feature(
        row,
        list(INTERVALS.keys()),
    )

    min_value, max_value = INTERVALS[interval_feature]

    # Seed
    seed_feature = selected_feature(
        row,
        list(SEEDS.keys()),
    )

    seed = SEEDS[seed_feature]

    # Numeric type and random generator
    if language == "Python":
        numeric_feature = selected_feature(
            row,
            list(PYTHON_TYPES.keys()),
        )

        numeric_config = PYTHON_TYPES[numeric_feature]

        random_generator = selected_feature(
            row,
            sorted(PYTHON_GENERATORS),
        )

    else:
        numeric_feature = selected_feature(
            row,
            list(JAVA_TYPES.keys()),
        )

        numeric_config = JAVA_TYPES[numeric_feature]

        random_generator = selected_feature(
            row,
            sorted(JAVA_GENERATORS),
        )

    return {
        "language": language,
        "environment": environment,
        "property_name": property_config["name"],
        "lhs": property_config["lhs"],
        "rhs": property_config["rhs"],
        "repetitions": repetitions,
        "min_value": min_value,
        "max_value": max_value,
        "seed": seed,
        "numeric_config": numeric_config,
        "random_generator": random_generator,
    }


# ============================================================
# DOCKER HELPERS
# ============================================================

def check_docker_images(environments):
    """Verify that the required Docker images exist."""

    for environment in environments:
        image = DOCKER_IMAGES[environment]

        result = subprocess.run(
            ["docker", "image", "inspect", image],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Docker image not found: {image}\n"
                "Run: python3 part6/prepare_docker_containers.py"
            )


def run_in_docker(environment, command):
    """Execute a command inside the selected Docker image."""

    image = DOCKER_IMAGES[environment]

    docker_command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "-v",
        f"{ROOT}:/workspace",
        "-w",
        "/workspace",
        image,
        "sh",
        "-lc",
        command,
    ]

    return subprocess.run(
        docker_command,
        capture_output=True,
        text=True,
    )


# ============================================================
# VARIANT GENERATION
# ============================================================

def safe_name(value):
    """Convert a value into a filesystem-safe name."""

    return re.sub(r"[^a-zA-Z0-9_]", "_", str(value))


def generate_python(configuration, execution_seed, output_path):
    """Generate a Python variant using the Jinja template."""

    template = Template(
        PYTHON_TEMPLATE_PATH.read_text(encoding="utf-8")
    )

    numeric_config = configuration["numeric_config"]

    generated_code = template.render(
        property_name=configuration["property_name"],
        lhs=configuration["lhs"],
        rhs=configuration["rhs"],
        numeric_type=numeric_config["numeric_type"],
        random_generator=configuration["random_generator"],
        repetitions=configuration["repetitions"],
        seed=execution_seed,
        min_value=configuration["min_value"],
        max_value=configuration["max_value"],
    )

    output_path.write_text(generated_code, encoding="utf-8")


def generate_java(
    configuration,
    execution_seed,
    output_path,
    class_name,
):
    """Generate a Java variant using the Jinja template."""

    template = Template(
        JAVA_TEMPLATE_PATH.read_text(encoding="utf-8")
    )

    numeric_config = configuration["numeric_config"]

    generated_code = template.render(
        property_name=configuration["property_name"],
        class_name=class_name,
        lhs=configuration["lhs"],
        rhs=configuration["rhs"],
        type_name=numeric_config["type_name"],
        type_label=numeric_config["label"],
        random_generator=configuration["random_generator"],
        repetitions=configuration["repetitions"],
        seed=execution_seed,
        min_value=configuration["min_value"],
        max_value=configuration["max_value"],
    )

    output_path.write_text(generated_code, encoding="utf-8")


# ============================================================
# EXECUTION
# ============================================================

def parse_percentage(stdout):
    """Extract and validate the percentage from the JSON output."""

    lines = [
        line.strip()
        for line in stdout.splitlines()
        if line.strip()
    ]

    if not lines:
        raise ValueError("The generated program produced no output.")

    answer = json.loads(lines[-1])

    if "percentage" not in answer:
        raise ValueError(
            f"The JSON output does not contain 'percentage': {answer}"
        )

    return answer["percentage"]


def execute_python(configuration, source_path):
    """Execute a generated Python program inside Docker."""

    environment = configuration["environment"]
    relative_path = source_path.relative_to(ROOT).as_posix()

    if environment == "CPython":
        interpreter = "python"
    elif environment == "PyPy":
        interpreter = "/opt/pypy/bin/python"
    else:
        raise ValueError(f"Unsupported Python environment: {environment}")

    command = f"{interpreter} /workspace/{shlex.quote(relative_path)}"

    return run_in_docker(environment, command)


def execute_java(configuration, source_path, class_name):
    """Compile and execute a generated Java program inside Docker."""

    environment = configuration["environment"]
    relative_path = source_path.relative_to(ROOT).as_posix()

    command = (
        "mkdir -p /tmp/part6-classes && "
        f"javac -d /tmp/part6-classes "
        f"/workspace/{shlex.quote(relative_path)} && "
        f"java -cp /tmp/part6-classes {class_name}"
    )

    return run_in_docker(environment, command)


# ============================================================
# EXPERIMENT RUNNER
# ============================================================

def run_configuration(config_id, configuration, run_index):
    """Generate and execute one run of a configuration."""

    if VARY_SEED_PER_RUN:
        execution_seed = configuration["seed"] + run_index - 1
    else:
        execution_seed = configuration["seed"]

    run_directory = GENERATED_DIR / safe_name(config_id)
    run_directory.mkdir(parents=True, exist_ok=True)

    if configuration["language"] == "Python":

        filename = (
            f"run_{run_index:02d}_"
            f"{configuration['property_name']}_"
            f"{configuration['numeric_config']['label']}.py"
        )

        source_path = run_directory / filename

        generate_python(
            configuration,
            execution_seed,
            source_path,
        )

        result = execute_python(
            configuration,
            source_path,
        )

    else:
        # The prefix guarantees a valid Java class name.
        class_name = (
            f"Experiment{safe_name(config_id)}Run{run_index}"
        )

        filename = f"{class_name}.java"
        source_path = run_directory / filename

        generate_java(
            configuration,
            execution_seed,
            source_path,
            class_name,
        )

        result = execute_java(
            configuration,
            source_path,
            class_name,
        )

    if result.returncode != 0:
        raise RuntimeError(
            f"Execution failed for configuration {config_id}, "
            f"run {run_index}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    percentage = parse_percentage(result.stdout)

    print(
        f"  Run {run_index}/{RUNS_PER_CONFIGURATION}: "
        f"{percentage}%"
    )

    return percentage


# ============================================================
# MAIN
# ============================================================

def main():

    if not SAMPLE_PATH.exists():
        print(f"Sample file not found: {SAMPLE_PATH}")
        sys.exit(1)

    if not PYTHON_TEMPLATE_PATH.exists():
        print(f"Python template not found: {PYTHON_TEMPLATE_PATH}")
        sys.exit(1)

    if not JAVA_TEMPLATE_PATH.exists():
        print(f"Java template not found: {JAVA_TEMPLATE_PATH}")
        sys.exit(1)

    # Read sample.csv
    print("Loading sample configurations...")

    with SAMPLE_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        sample_rows = list(reader)
        sample_columns = reader.fieldnames

    if not sample_rows:
        print("No configurations found in sample.csv.")
        sys.exit(1)

    if not sample_columns:
        print("Could not read the columns of sample.csv.")
        sys.exit(1)

    # Extract configurations before checking Docker.
    configurations = []

    for index, row in enumerate(sample_rows, start=1):
        config_id = row.get("config_id") or f"config_{index}"

        configuration = extract_configuration(row)

        configurations.append(
            (config_id, row, configuration)
        )

    # Only check the Docker images actually needed.
    environments = {
        configuration["environment"]
        for _, _, configuration in configurations
    }

    print("\nChecking Docker images...")
    check_docker_images(environments)

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    # Execute experiments.
    results = []

    print("\n========================================")
    print("Starting experiments")
    print("========================================")
    print(f"Configurations: {len(configurations)}")
    print(f"Runs per configuration: {RUNS_PER_CONFIGURATION}")

    for index, (config_id, row, configuration) in enumerate(
        configurations,
        start=1,
    ):
        print(f"\n[{index}/{len(configurations)}] Configuration: {config_id}")

        print(
            f"  Environment: {configuration['environment']} | "
            f"Property: {configuration['property_name']} | "
            f"Type: {configuration['numeric_config']['label']}"
        )

        for run_index in range(1, RUNS_PER_CONFIGURATION + 1):

            percentage = run_configuration(
                config_id,
                configuration,
                run_index,
            )

            # Keep exactly the original sample.csv columns
            # and add only the results column.
            output_row = dict(row)
            output_row["results"] = percentage

            results.append(output_row)

    # Write results.csv
    fieldnames = list(sample_columns) + ["results"]

    with RESULTS_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n========================================")
    print("Experiments completed successfully")
    print("========================================")
    print(f"Configurations: {len(configurations)}")
    print(f"Total runs: {len(results)}")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()