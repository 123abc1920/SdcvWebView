import subprocess


import subprocess


class BaseSdcvEngine:
    """
    Base execution engine for interacting with the sdcv dictionary CLI tool.
    """

    def __init__(self, prefix: list[str]):
        """
        Initializes the base engine with a command prefix.

        Args:
            prefix (list[str]): The base command prefix used to invoke the sdcv process.
        """
        self.prefix = prefix

    def list(self) -> subprocess.CompletedProcess:
        """
        Lists all available dictionaries.

        Returns:
            subprocess.CompletedProcess: The completed process containing stdout with dictionary lists.
        """
        return subprocess.run(
            self.prefix + ["-l"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

    def translate(
        self, word: str, u_filters: list = None
    ) -> subprocess.CompletedProcess:
        """
        Looks up a word translation using optional dictionary filters.

        Args:
            word (str): The target word to translate.
            u_filters (list, optional): A list of specific dictionary names to filter the search results.

        Returns:
            subprocess.CompletedProcess: The completed process containing stdout with JSON translation data.
        """
        filters = u_filters or []
        cmd = self.prefix + ["--json-output", "--exact-search", str(word)] + filters
        return subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", timeout=10
        )


class LinuxSdcvEngine(BaseSdcvEngine):
    """
    Engine implementation for executing sdcv directly on a host Linux environment.
    """

    def __init__(self):
        """
        Initializes the Linux engine with the default standard local execution prefix.
        """
        super().__init__(prefix=["sdcv"])


class DockerSdcvEngine(BaseSdcvEngine):
    """
    Engine implementation for executing sdcv containerized inside a Docker environment.
    """

    def __init__(self, container_name: str):
        """
        Initializes the Docker engine linked to a specific container instance.

        Args:
            container_name (str): The name of the target running Docker container.
        """
        prefix = ["docker", "exec", container_name, "sdcv"]
        super().__init__(prefix=prefix)


DOCKER_TYPE = "docker"
"""Constant string representing a Docker environment selection identifier."""

LINUX_TYPE = "linux"
"""Constant string representing a local Linux environment selection identifier."""


def create_engine(sdcv_type: str, container_name: str | None = None) -> BaseSdcvEngine:
    """
    Factory function that instantiates the appropriate sdcv engine based on the environment type.

    Args:
        sdcv_type (str): The type of deployment environment ('docker' or 'linux').
        container_name (str, optional): The name of the target Docker container. Required if type is 'docker'.

    Raises:
        ValueError: If the environment type requires a container name, but none was provided or valid.

    Returns:
        BaseSdcvEngine: An initialized instance of a subclassed sdcv engine ready for queries.
    """
    sdcv_type = sdcv_type.lower().replace(" ", "")

    if sdcv_type == DOCKER_TYPE:
        if container_name is None or container_name == "" or not container_name.strip():
            raise ValueError("Container name is required for Docker engine!")
        return DockerSdcvEngine(container_name.replace(" ", ""))

    if sdcv_type == LINUX_TYPE:
        return LinuxSdcvEngine()
