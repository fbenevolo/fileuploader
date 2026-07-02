class EmptyFileException(Exception):
    pass


class FileTooLargeException(Exception):
    pass


class FileHasNoExtension(Exception):
    pass


class ModeNotFound(Exception):
    pass


class FileUploadException(Exception):
    pass


class S3StorageException(Exception):
    pass


class DynamoDBException(Exception):
    pass
