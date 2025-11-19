import pytest
import os
import shutil

if __name__ == '__main__':
    allure_results_dir = "./report/temp"
    #删除上次报告，可以不用
    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir)

    pytest.main(['-v',
                 '-s',
                 './testcase',
                 f'--alluredir={allure_results_dir}'
                 ])

    os.system(f'allure serve ./report/temp')