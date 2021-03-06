"""Exceptions raised by the dvc."""

from __future__ import unicode_literals

from dvc.utils.compat import str, builtin_str

import traceback


class DvcException(Exception):
    """Base class for all dvc exceptions.

    Args:
        msg (unicode): message for this exception.
        cause (Exception): optional cause exception.
    """

    def __init__(self, msg, cause=None):
        # NOTE: unlike python 3, python 2 doesn't have built-in support
        # for chained exceptions, so we are using our own implementation.
        self.cause = cause
        self.cause_tb = None
        if cause:
            try:
                self.cause_tb = traceback.format_exc()
            except AttributeError:  # pragma: no cover
                pass
        super(DvcException, self).__init__(msg)


class OutputDuplicationError(DvcException):
    """Thrown if a file/directory is specified as an output in more than one
    stage.

    Args:
        output (unicode): path to the file/directory.
        stages (list): list of paths to stages.
    """

    def __init__(self, output, stages):
        assert isinstance(output, str) or isinstance(output, builtin_str)
        assert isinstance(stages, list)
        assert all(
            isinstance(stage, str) or isinstance(stage, builtin_str)
            for stage in stages
        )
        msg = (
            "file/directory '{}' is specified as an output in more than one"
            "stage: {}"
        ).format(output, "\n    ".join(stages))
        super(OutputDuplicationError, self).__init__(msg)


class WorkingDirectoryAsOutputError(DvcException):
    """Thrown if directory that stage is going to be saved in is specified as
    an output of anothe stage.

    Args:
        cwd (str): path to the directory.
        fname (str): path to the stage file that has cwd specified as an
            output.
    """

    def __init__(self, cwd, fname):
        assert isinstance(cwd, str) or isinstance(cwd, builtin_str)
        assert isinstance(fname, str) or isinstance(fname, builtin_str)
        msg = (
            "current working directory '{cwd}' is specified as an output in"
            " '{fname}'. Use another CWD to prevent any data removal.".format(
                cwd=cwd, fname=fname
            )
        )
        super(WorkingDirectoryAsOutputError, self).__init__(msg)


class CircularDependencyError(DvcException):
    """Thrown if a file/directory specified both as an output and as a
    dependency.

    Args:
        dependency (str): path to the dependency.
    """

    def __init__(self, dependency):
        assert isinstance(dependency, str) or isinstance(
            dependency, builtin_str
        )

        msg = (
            "file/directory '{}' is specified as an output and as a "
            "dependency."
        )
        super(CircularDependencyError, self).__init__(msg.format(dependency))


class ArgumentDuplicationError(DvcException):
    """Thrown if a file/directory is specified as a dependency/output more
    than once.

    Args:
        path (str): path to the file/directory.
    """

    def __init__(self, path):
        assert isinstance(path, str) or isinstance(path, builtin_str)
        msg = "file '{}' is specified more than once."
        super(ArgumentDuplicationError, self).__init__(msg.format(path))


class MoveNotDataSourceError(DvcException):
    """Thrown if attempted to move a file/directory that is not an output
    in a data source stage.

    Args:
        path (str): path to the file/directory.
    """

    def __init__(self, path):
        msg = (
            "move is not permitted for stages that are not data sources. "
            "You need to either move '{path}' to a new location and edit "
            "it by hand, or remove '{path}' and create a new one at the "
            "desired location."
        )
        super(MoveNotDataSourceError, self).__init__(msg.format(path=path))


class NotDvcProjectError(DvcException):
    """Thrown if a directory is not a dvc project.

    Args:
        root (str): path to the directory.
    """

    def __init__(self, root):
        msg = "not a dvc repository (checked up to mount point '{}')"
        super(NotDvcProjectError, self).__init__(msg.format(root))


class DvcParserError(DvcException):
    """Base class for CLI parser errors."""

    def __init__(self):
        super(DvcParserError, self).__init__("parser error")


class CyclicGraphError(DvcException):
    def __init__(self, stages):
        assert isinstance(stages, list)
        stages = "\n".join("\t- {}".format(stage) for stage in stages)
        msg = (
            "you've introduced a cycle in your pipeline that involves"
            " the following stages:"
            "\n"
            "{stages}".format(stages=stages)
        )
        super(CyclicGraphError, self).__init__(msg)


class ConfirmRemoveError(DvcException):
    def __init__(self, path):
        super(ConfirmRemoveError, self).__init__(
            "unable to remove '{}' without a confirmation from the user. Use "
            "'-f' to force.".format(path)
        )
