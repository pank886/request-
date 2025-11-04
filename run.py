import pytest
import os

if __name__ == '__main__':
    pytest.main(['-vs', './testcase', '--reruns', '2'])
    os.system(f'allure serve ./report/temp')