import pytest
import os
import shutil
import sys
import subprocess
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).parent
ALLURE = r"E:\pycharm-2025.1\allure\allure-2.21.0\bin\allure.bat"
REPORT_TEMP = BASE_DIR / "report" / "temp"
REPORT_HTML = BASE_DIR / "report" / "html"
PORT = 63333


def kill_old_server():
    """杀掉占用端口的旧进程"""
    import subprocess as _sp
    try:
        result = _sp.run(
            ["netstat", "-ano"], capture_output=True, text=True, shell=True
        )
        for line in result.stdout.splitlines():
            if f":{PORT}" in line and "LISTENING" in line:
                pid = line.strip().split()[-1]
                _sp.run(["taskkill", "/pid", pid, "/f"], capture_output=True)
    except Exception:
        pass


def serve_report():
    kill_old_server()
    print(f"报告地址: http://localhost:{PORT}")
    print("按 Ctrl+C 停止服务器")
    webbrowser.open(f"http://localhost:{PORT}")
    python = BASE_DIR / ".venv" / "Scripts" / "python.exe"
    subprocess.run(
        [str(python), "-m", "http.server", str(PORT), "-d", str(REPORT_HTML)],
        cwd=BASE_DIR,
    )


if __name__ == '__main__':
    allure_results_dir = "./report/temp"
    if os.path.exists(allure_results_dir):
        try:
            shutil.rmtree(allure_results_dir)
        except PermissionError:
            print("警告: 无法删除旧报告目录，文件被占用，跳过清理")

    args = ['-v', '-s', f'--alluredir={allure_results_dir}']

    if len(sys.argv) > 1:
        mark_name = sys.argv[1]
        print(f"正在执行标记为 [{mark_name}] 的测试...")
        args.extend(['-m', mark_name])
    else:
        print("未指定标记，执行所有测试...")
        args.append('./testcase')

    pytest.main(args)

    if os.path.exists('environment.xml'):
        shutil.copy('environment.xml', './report/temp')

    subprocess.run(
        [ALLURE, "generate", str(REPORT_TEMP), "-o", str(REPORT_HTML), "--clean"],
        cwd=BASE_DIR,
        shell=True,
    )
    serve_report()