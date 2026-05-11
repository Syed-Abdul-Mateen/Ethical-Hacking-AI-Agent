"""Enterprise-grade subprocess wrapper with timeout, retry, and sandboxing controls."""

import subprocess
import shlex
import logging
import time
from typing import Optional, Tuple, List, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """Structured result from command execution."""
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False
    duration_seconds: float = 0.0
    attempts: int = 1


def run_command(
    cmd: Union[str, List[str]],
    timeout: int = 60,
    retries: int = 0,
    retry_delay: float = 1.0,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
    shell: bool = False,
    capture_output: bool = True,
    input_data: Optional[str] = None,
    safe_mode: bool = True,
) -> CommandResult:
    """
    Execute a shell command with timeout, retry, and safety controls.

    Args:
        cmd: Command to execute (string or list of arguments).
        timeout: Maximum execution time in seconds.
        retries: Number of retry attempts on failure (0 = no retries).
        retry_delay: Seconds to wait between retries.
        cwd: Working directory for the command.
        env: Environment variables to set (merged with current env).
        shell: Whether to run via shell (avoid when possible).
        capture_output: Whether to capture stdout/stderr.
        input_data: Data to send to stdin.
        safe_mode: If True, disallows shell=True and validates commands.

    Returns:
        CommandResult with exit code, stdout, stderr, and metadata.

    Raises:
        ValueError: If unsafe commands are detected in safe_mode.
    """
    # Parse string commands into lists for safety
    if isinstance(cmd, str) and not shell:
        try:
            cmd = shlex.split(cmd)
        except ValueError as e:
            logger.error(f"Failed to parse command: {e}")
            return CommandResult(exit_code=-1, stdout="", stderr=str(e))

    # Safety checks
    if safe_mode:
        if shell:
            logger.warning("shell=True is blocked in safe_mode. Use cmd as a list instead.")
            return CommandResult(
                exit_code=-1, stdout="",
                stderr="shell=True is not allowed in safe_mode."
            )

        # Block dangerous commands
        dangerous_commands = {"rm", "del", "format", "mkfs", "dd", "shutdown", "reboot"}
        cmd_name = cmd[0].lower() if isinstance(cmd, list) and cmd else ""
        if cmd_name in dangerous_commands:
            logger.error(f"Blocked dangerous command: {cmd_name}")
            return CommandResult(
                exit_code=-1, stdout="",
                stderr=f"Command '{cmd_name}' is blocked in safe_mode."
            )

    attempts = 0
    last_result = None

    while attempts <= retries:
        attempts += 1
        start_time = time.monotonic()

        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=env,
                shell=shell,
                input=input_data,
            )
            duration = time.monotonic() - start_time

            last_result = CommandResult(
                exit_code=result.returncode,
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                timed_out=False,
                duration_seconds=round(duration, 3),
                attempts=attempts,
            )

            if result.returncode == 0:
                return last_result

            # Non-zero exit code; retry if attempts remain
            if attempts <= retries:
                logger.warning(
                    f"Command failed (exit {result.returncode}), "
                    f"retrying in {retry_delay}s ({attempts}/{retries + 1})..."
                )
                time.sleep(retry_delay)

        except subprocess.TimeoutExpired:
            duration = time.monotonic() - start_time
            logger.error(f"Command timed out after {timeout}s: {cmd}")
            last_result = CommandResult(
                exit_code=-1,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds.",
                timed_out=True,
                duration_seconds=round(duration, 3),
                attempts=attempts,
            )
            if attempts <= retries:
                logger.info(f"Retrying timed-out command ({attempts}/{retries + 1})...")
                time.sleep(retry_delay)

        except FileNotFoundError:
            logger.error(f"Command not found: {cmd}")
            return CommandResult(
                exit_code=-1, stdout="",
                stderr=f"Command not found: {cmd[0] if isinstance(cmd, list) else cmd}",
                attempts=attempts,
            )

        except Exception as e:
            logger.error(f"Unexpected error running command: {e}")
            return CommandResult(
                exit_code=-1, stdout="",
                stderr=str(e),
                attempts=attempts,
            )

    return last_result or CommandResult(exit_code=-1, stdout="", stderr="Unknown error")


def run_command_streaming(
    cmd: Union[str, List[str]],
    timeout: int = 300,
    cwd: Optional[str] = None,
    callback=None,
) -> CommandResult:
    """
    Execute a command with real-time output streaming.

    Args:
        cmd: Command to execute.
        timeout: Maximum execution time in seconds.
        cwd: Working directory.
        callback: Function called with each output line (for real-time logging).

    Returns:
        CommandResult with full output.
    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    stdout_lines = []
    stderr_lines = []
    start_time = time.monotonic()

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
        )

        while True:
            elapsed = time.monotonic() - start_time
            if elapsed > timeout:
                process.kill()
                return CommandResult(
                    exit_code=-1,
                    stdout="\n".join(stdout_lines),
                    stderr="Timeout exceeded",
                    timed_out=True,
                    duration_seconds=round(elapsed, 3),
                )

            line = process.stdout.readline()
            if line:
                stdout_lines.append(line.rstrip())
                if callback:
                    callback(line.rstrip())
            elif process.poll() is not None:
                break

        # Capture remaining stderr
        remaining_stderr = process.stderr.read()
        if remaining_stderr:
            stderr_lines.append(remaining_stderr)

        duration = time.monotonic() - start_time
        return CommandResult(
            exit_code=process.returncode,
            stdout="\n".join(stdout_lines),
            stderr="\n".join(stderr_lines),
            duration_seconds=round(duration, 3),
        )

    except FileNotFoundError:
        return CommandResult(
            exit_code=-1, stdout="",
            stderr=f"Command not found: {cmd[0]}",
        )
    except Exception as e:
        return CommandResult(exit_code=-1, stdout="", stderr=str(e))
