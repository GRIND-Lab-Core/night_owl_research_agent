"""
Code Executor — runs generated Python code in a sandboxed subprocess.
Handles timeout, output capture, and result extraction.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class CodeExecutor:
    """Executes Python code snippets safely in a subprocess."""

    def __init__(self, timeout_sec: int = 300, working_dir: str | Path = ".") -> None:
        self.timeout_sec = timeout_sec
        self.working_dir = Path(working_dir)

    def run_code(self, code: str, label: str = "script") -> dict:
        """
        Execute Python code and return results dict.

        Args:
            code: Python source code to execute
            label: Label for the temp file (for logging)

        Returns:
            Dict with: status, stdout, stderr, returncode
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", prefix=f"geo_agent_{label}_",
            delete=False, dir=self.working_dir
        ) as tmp:
            tmp.write(code)
            tmp_path = Path(tmp.name)

        try:
            proc = subprocess.run(
                ["python", str(tmp_path)],
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                cwd=str(self.working_dir),
            )
            return {
                "status": "success" if proc.returncode == 0 else "error",
                "stdout": proc.stdout[:3000],
                "stderr": proc.stderr[:1000],
                "returncode": proc.returncode,
                "script_path": str(tmp_path),
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "stdout": "", "stderr": f"Execution timed out after {self.timeout_sec}s", "returncode": -1}
        except Exception as e:
            return {"status": "error", "stdout": "", "stderr": str(e), "returncode": -1}
        finally:
            try:
                tmp_path.unlink()
            except Exception:
                pass

    def run_file(self, script_path: str | Path) -> dict:
        """Execute an existing Python file."""
        try:
            proc = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                cwd=str(self.working_dir),
            )
            return {
                "status": "success" if proc.returncode == 0 else "error",
                "stdout": proc.stdout[:3000],
                "stderr": proc.stderr[:1000],
                "returncode": proc.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "stdout": "", "stderr": "Timeout", "returncode": -1}
        except Exception as e:
            return {"status": "error", "stdout": "", "stderr": str(e), "returncode": -1}
