import pytest

class TestAddUser:

    @pytest.mark.order(1)
    @pytest.mark.maoyan
    def test_addUser1(self):
        print('新增用户')

    @pytest.mark.order(2)
    def test_addUser2(self):
        print('新增用户')

    @pytest.mark.order3(3)
    def test_addUser(self):
        print('新增用户')