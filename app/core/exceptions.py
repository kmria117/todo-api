"""Exception domain. Layer API yang menerjemahkannya ke kode HTTP."""


class TaskError(Exception):
    """Base class untuk semua error domain."""


class TaskNotFoundError(TaskError):
    pass


class InvalidTaskError(TaskError):
    pass


class TaskAlreadyDoneError(TaskError):
    pass
