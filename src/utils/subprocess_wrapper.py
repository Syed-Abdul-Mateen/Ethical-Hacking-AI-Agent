import subprocess

def run_command(cmd: str | list) -> tuple[int, str, str]:
    """Runs a shell command and returns exit code, stdout, stderr."""
    if isinstance(cmd, str):
        cmd = cmd.split()
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr
