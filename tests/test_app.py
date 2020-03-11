from context import app


def test_app(capsys):
    # pylint: disable=W0612,W0613
    app.Dashboard.test()
    captured = capsys.readouterr()

    assert "Hello world!" in captured.out