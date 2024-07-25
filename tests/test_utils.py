from unittest.mock import patch, mock_open

import pytest

from rpm_lockfile import utils


@pytest.mark.parametrize(
    "dir,path,expected",
    [
        ("/topdir", "subdir", "/topdir/subdir"),
        ("/topdir", "/root", "/root"),
        ("/topdir", None, None),
    ]
)
def test_relative_to(dir, path, expected):
    assert utils.relative_to(dir, path) == expected


@pytest.mark.parametrize(
    "files,expected",
    [
        (["Containerfile"], "Containerfile"),
        (["Dockerfile"], "Dockerfile"),
        (["Containerfile", "Dockerfile"], "Containerfile"),
        (["foobar"], None),
        ([], None),
    ]
)
def test_find_containerfile(tmpdir, files, expected):
    for fn in files:
        (tmpdir / fn).write_text("", encoding="utf-8")
    actual = utils.find_containerfile(tmpdir)
    if expected:
        assert actual == tmpdir / expected
    else:
        assert actual is None


@pytest.mark.parametrize(
    "file,expected",
    [
        ("""FROM registry.io/repository/base
RUN something
""", "registry.io/repository/base"),
        ("""FROM registry.io/repository/build as build
RUN build
FROM registry.io/repository/base
COPY --from=build /artifact /
""", "registry.io/repository/base"),
    ]
)
def test_extract_image(file, expected):
    with patch("builtins.open", mock_open(read_data=file)):
        assert utils.extract_image(file) == expected


@pytest.mark.parametrize(
    "content,hash",
    [
        ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("hello\n", "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"),
    ],
)
def test_hash_file(content, hash, tmp_path):
    fn = tmp_path / "something"
    fn.write_text(content, encoding="utf-8")
    assert utils.hash_file(fn) == hash
