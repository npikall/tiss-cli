from tiss_cli import greet


def test_that_testing_package_is_working():
    got = greet()
    want = "Hello from tiss-cli"

    assert got == want
