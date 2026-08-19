"""
测试执行入口，支持路径+marker双重筛选，自动生成Allure报告。

用法:
    python run.py                              # 全部路径 + 全部用例
    python run.py -p testcase/SubConfiguration/  # 只跑指定路径
    python run.py -m danyuan                    # 全部路径，只跑danyuan标记
    python run.py -p testcase/ -m danyuan        # 指定路径 + 指定标记
"""
import pytest
import os
import shutil
import sys
import subprocess
import webbrowser
import argparse
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
    if not REPORT_HTML.exists():
        print(f"错误: 报告目录不存在 {REPORT_HTML}")
        return
    kill_old_server()
    print(f"报告地址: http://localhost:{PORT}")
    print("按 Ctrl+C 停止服务器")
    webbrowser.open(f"http://localhost:{PORT}")
    python = BASE_DIR / ".venv" / "Scripts" / "python.exe"
    # 先切到报告目录再启动服务，比 -d 参数更稳定
    os.chdir(str(REPORT_HTML))
    subprocess.run(
        [str(python), "-m", "http.server", str(PORT)],
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='运行测试并生成Allure报告')
    parser.add_argument('-p', '--path', default='',
                        help='测试路径，如 testcase/SubConfiguration/（空=全部路径）')
    parser.add_argument('-m', '--mark', default='',
                        help='marker表达式，如 danyuan（空=全部marker）')
    args, _ = parser.parse_known_args()

    allure_results_dir = "./report/temp"
    allure_html_dir = str(REPORT_HTML)
    for d in (allure_results_dir, allure_html_dir):
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except PermissionError:
                print(f"警告: 无法删除 {d}，文件被占用，跳过清理")

    pytest_args = ['-c', 'pytest.ini', '-v', '-s',
                   f'--alluredir={allure_results_dir}']

    # 路径筛选（-p）
    target_path = args.path.strip() if args.path else ''
    if target_path:
        pytest_args.append(target_path)
        print(f"路径筛选: {target_path}")
    else:
        pytest_args.append('./testcase')

    # marker筛选（-m）
    if args.mark:
        pytest_args.extend(['-m', args.mark])
        print(f"标记筛选: -m {args.mark}")

    if not target_path and not args.mark:
        print("执行所有路径 + 所有用例")
    print(f"pytest参数: {' '.join(pytest_args)}")

    pytest.main(pytest_args)

    if os.path.exists('environment.xml'):
        shutil.copy('environment.xml', './report/temp')

    subprocess.run(
        [ALLURE, "generate", str(REPORT_TEMP), "-o", str(REPORT_HTML), "--clean"],
        cwd=BASE_DIR,
        shell=True,
    )
    serve_report()