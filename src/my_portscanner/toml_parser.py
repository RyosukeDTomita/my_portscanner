import importlib.resources
import tomli
import importlib


def get_project_version() -> str:
    """_summary_

    Returns:
        _type_: _description_
    """
    pyproject_toml_path = importlib.resources.files("my_portscanner").joinpath(
        "pyproject.toml"
    )

    with open(pyproject_toml_path, "rb") as f:
        pyproject_data = tomli.load(f)

    # versionが見つからない場合は'No version found'を返す
    version = pyproject_data.get("project", {}).get("version", "No version found")
    return version


if __name__ == "__main__":
    version = get_project_version()
    print(f"Project version: {version}")
