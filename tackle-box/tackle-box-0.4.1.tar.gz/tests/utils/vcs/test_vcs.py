"""Tests around cloning repositories and detection of errors at it."""
import os
import subprocess

import pytest

from tackle import exceptions
from tackle.utils import vcs


@pytest.fixture
def clone_dir(tmpdir):
    """Simulate creation of a directory called `clone_dir` inside of `tmpdir`. \
    Returns a str to said directory."""
    return str(tmpdir.mkdir('clone_dir'))


def test_clone_should_raise_if_vcs_not_installed(mocker, clone_dir):
    """In `clone()`, a `VCSNotInstalled` exception should be raised if no VCS \
    is installed."""
    mocker.patch('tackle.utils.vcs.is_vcs_installed', autospec=True, return_value=False)

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(exceptions.VCSNotInstalled):
        vcs.clone(repo_url, clone_to_dir=clone_dir)


def test_clone_should_rstrip_trailing_slash_in_repo_url(mocker, clone_dir):
    """In `clone()`, repo URL's trailing slash should be stripped if one is \
    present."""
    mocker.patch('tackle.utils.vcs.is_vcs_installed', autospec=True, return_value=True)

    mock_subprocess = mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
    )

    vcs.clone('https://github.com/foo/bar/', clone_to_dir=clone_dir, no_input=True)

    mock_subprocess.assert_called_once_with(
        ['git', 'clone', 'https://github.com/foo/bar'],
        cwd=clone_dir,
        stderr=subprocess.STDOUT,
    )


def test_clone_should_abort_if_user_does_not_want_to_reclone(mocker, tmpdir):
    """In `clone()`, if user doesn't want to reclone, Cookiecutter should exit \
    without cloning anything."""
    mocker.patch('tackle.utils.vcs.is_vcs_installed', autospec=True, return_value=True)
    mocker.patch(
        'tackle.utils.vcs.prompt_and_delete', side_effect=SystemExit, autospec=True
    )
    mock_subprocess = mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create repo_dir to trigger prompt_and_delete
    clone_to_dir.mkdir('cookiecutter-pytest-plugin')

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(SystemExit):
        vcs.clone(repo_url, clone_to_dir=str(clone_to_dir))
    assert not mock_subprocess.called


@pytest.mark.parametrize(
    'repo_type, repo_url, repo_name',
    [
        ('git', 'https://github.com/hello/world.git', 'world'),
        ('git', 'git@host:gitoliterepo', 'gitoliterepo'),
        ('git', 'git@gitlab.com:cookiecutter/cookiecutter.git', 'cookiecutter'),
        ('git', 'git@github.com:cookiecutter/cookiecutter.git', 'cookiecutter'),
    ],
)
def test_clone_should_invoke_vcs_command(
    mocker, clone_dir, repo_type, repo_url, repo_name
):
    """When `clone()` is called with a git/hg repo, the corresponding VCS \
    command should be run via `subprocess.check_output()`.

    This should take place:
    * In the correct dir
    * With the correct args.
    """
    mocker.patch('tackle.utils.vcs.is_vcs_installed', autospec=True, return_value=True)

    mock_subprocess = mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
    )
    expected_repo_dir = os.path.normpath(os.path.join(clone_dir, repo_name))

    branch = 'foobar'

    repo_dir = vcs.clone(
        repo_url, checkout=branch, clone_to_dir=clone_dir, no_input=True
    )

    assert repo_dir == expected_repo_dir

    mock_subprocess.assert_any_call(
        [repo_type, 'clone', repo_url], cwd=clone_dir, stderr=subprocess.STDOUT
    )
    mock_subprocess.assert_any_call(
        [repo_type, 'checkout', branch], cwd=expected_repo_dir, stderr=subprocess.STDOUT
    )


@pytest.mark.parametrize(
    'error_message',
    [
        (
            "fatal: repository 'https://github.com/hackebro/cookiedozer' not found"
        ).encode('utf-8'),
        'hg: abort: HTTP Error 404: Not Found'.encode('utf-8'),
    ],
)
def test_clone_handles_repo_typo(mocker, clone_dir, error_message):
    """In `clone()`, repository not found errors should raise an \
    appropriate exception."""
    # side_effect is set to an iterable here (and below),
    # because of a Python 3.4 unittest.mock regression
    # http://bugs.python.org/issue23661
    mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[subprocess.CalledProcessError(-1, 'cmd', output=error_message)],
    )

    repository_url = 'https://github.com/hackebro/cookiedozer'
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        vcs.clone(repository_url, clone_to_dir=clone_dir, no_input=True)

    assert str(err.value) == (
        'The repository {} could not be found, have you made a typo?'
    ).format(repository_url)


@pytest.mark.parametrize(
    'error_message',
    [
        (
            "error: pathspec 'unknown_branch' did not match any file(s) known to git"
        ).encode('utf-8'),
        "hg: abort: unknown revision 'unknown_branch'!".encode('utf-8'),
    ],
)
def test_clone_handles_branch_typo(mocker, clone_dir, error_message):
    """In `clone()`, branch not found errors should raise an \
    appropriate exception."""
    mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[subprocess.CalledProcessError(-1, 'cmd', output=error_message)],
    )

    repository_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin'
    with pytest.raises(exceptions.RepositoryCloneFailed) as err:
        vcs.clone(
            repository_url,
            clone_to_dir=clone_dir,
            checkout='unknown_branch',
            no_input=True,
        )

    assert str(err.value) == (
        'The unknown_branch branch of repository '
        '{} could not found, have you made a typo?'
    ).format(repository_url)


def test_clone_unknown_subprocess_error(mocker, clone_dir):
    """In `clone()`, unknown subprocess errors should be raised."""
    mocker.patch(
        'tackle.utils.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[
            subprocess.CalledProcessError(
                -1, 'cmd', output='Something went wrong'.encode('utf-8')
            )
        ],
    )

    with pytest.raises(subprocess.CalledProcessError):
        vcs.clone(
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin',
            clone_to_dir=clone_dir,
            no_input=True,
        )


@pytest.mark.parametrize(
    'which_return, result',
    [('', False), (None, False), (False, False), ('/usr/local/bin/git', True)],
)
def test_is_vcs_installed(mocker, which_return, result):
    """Verify `is_vcs_installed` function correctly handles `which` answer."""
    mocker.patch('tackle.utils.vcs.which', autospec=True, return_value=which_return)
    assert vcs.is_vcs_installed('git') == result
