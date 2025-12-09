import sys
import subprocess
from pathlib import Path


def test_cli_runs_and_prints_output():
    project_root = Path(__file__).resolve().parents[1]
    cli_path = project_root / "cli.py"

    result = subprocess.run(
        [sys.executable, str(cli_path), "Moscow", "--temp", "15"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.returncode == 0
    assert "Moscow" in result.stdout
    assert "15.0" in result.stdout
