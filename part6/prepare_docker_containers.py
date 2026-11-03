import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

DOCKER_IMAGES = {
    "CPython": {
        "image": "repro-cpython:3.12",
        "base": "python:3.12-slim",
        "setup": [
            "RUN python -m pip install --no-cache-dir numpy"
        ],
        "check_command": ["python", "--version"],
    },
    "PyPy": {
        "image": "repro-pypy:3.12",
        "base": "pypy:3.12-slim",
        "setup": [],
        "check_command": ["python", "--version"],
    },
    "OpenJDK": {
        "image": "repro-openjdk:21",
        "base": "eclipse-temurin:21-jdk",
        "setup": [],
        "check_command": ["java", "-version"],
    },
    "GraalVM": {
        "image": "repro-graalvm:21",
        "base": "ghcr.io/graalvm/jdk-community:21",
        "setup": [],
        "check_command": ["java", "-version"],
    },
}


def check_docker():
    """Check that Docker is installed and available."""

    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: Docker is not installed or not running.")
        sys.exit(1)


def build_image(environment, config):
    """Build a Docker image for the selected environment."""

    image = config["image"]
    base = config["base"]

    print(f"\nBuilding image for {environment}: {image}")

    dockerfile = f"FROM {base}\n"

    for instruction in config["setup"]:
        dockerfile += instruction + "\n"

    command = [
        "docker",
        "build",
        "--pull",
        "-t",
        image,
        "-f",
        "-",
        str(ROOT),
    ]

    subprocess.run(
        command,
        input=dockerfile,
        text=True,
        check=True,
    )

    print(f"Image built successfully: {image}")


def check_image(environment, config):
    """Check that the image can execute its runtime."""

    image = config["image"]
    check_command = config["check_command"]

    print(f"\nChecking {environment}...")

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            image,
            *check_command,
        ],
        check=True,
    )


def main():
    check_docker()

    for environment, config in DOCKER_IMAGES.items():
        try:
            build_image(environment, config)
            check_image(environment, config)

        except subprocess.CalledProcessError as error:
            print(f"\nError while preparing {environment}: {error}")
            sys.exit(1)

    print("\nAll Docker images have been prepared successfully.")


if __name__ == "__main__":
    main()