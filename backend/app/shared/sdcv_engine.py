import subprocess


class BaseSdcvEngine:
    def __init__(self, prefix: list[str]):
        self.prefix = prefix

    def list(self) -> subprocess.CompletedProcess:
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
        filters = u_filters or []
        cmd = self.prefix + ["--json-output", "--exact-search", str(word)] + filters
        return subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", timeout=10
        )


class LinuxSdcvEngine(BaseSdcvEngine):
    def __init__(self):
        super().__init__(prefix=["sdcv"])


class DockerSdcvEngine(BaseSdcvEngine):
    def __init__(self, container_name: str):
        prefix = ["docker", "exec", container_name, "sdcv"]
        super().__init__(prefix=prefix)


DOCKER_TYPE = "docker"
LINUX_TYPE = "linux"


def create_engine(sdcv_type: str, container_name: str | None = None) -> BaseSdcvEngine:
    sdcv_type = sdcv_type.lower().replace(" ", "")

    if sdcv_type == DOCKER_TYPE:
        if container_name is None or container_name == "" or not container_name.strip():
            raise ValueError("Container name is required for Docker engine!")
        return DockerSdcvEngine(container_name.replace(" ", ""))

    if sdcv_type == LINUX_TYPE:
        return LinuxSdcvEngine()
