import tomli
import os


def get_project_version() -> str:
    """_summary_

    Returns:
        _type_: _description_
    """
    script_running_directory = os.path.dirname(os.path.abspath(__file__))
    pyproject_toml_path = os.path.join(
        script_running_directory + "/../../" + "pyproject.toml"
    )
    print(f"pyproject.toml path: {pyproject_toml_path}")

    with open(pyproject_toml_path, "rb") as f:
        pyproject_data = tomli.load(f)

    # versionが見つからない場合は'No version found'を返す
    version = pyproject_data.get("project", {}).get("version", "No version found")
    print(f"Project version: {version}")
    return version


if __name__ == "__main__":
    get_project_version()
