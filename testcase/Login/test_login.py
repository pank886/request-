import pytest

class TestLogin:

    @pytest.mark.order(0)
    @pytest.mark.maoyan
    def test_login(self):
        print('用户登录')
