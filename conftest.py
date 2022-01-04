import pytest

from ptbtest import mockbot



@pytest.fixture(scope="session")
def bot_setup():
    bot = mockbot