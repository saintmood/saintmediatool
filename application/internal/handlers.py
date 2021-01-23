import abc


class BaseHandler(abc.ABC):
    """
        Define parent for all handlers.
        This is another implementation of "Chain Of Command" patter.
    """

    def __init__(self):
        self.next_to = None

    def set_next(self, handler) -> None:
        self.next_to = handler

    @abc.abstractmethod
    def process_input(self, *args, **kwargs):
        """Implement the actions."""

    def handle(self, *args, **kwargs):
        result = self.process_input(*args, **kwargs)
        if self.next_to is not None:
            return self.next_to.process_input(result)
        return result


class RetrieveSingleImageHandler(BaseHandler):

    def process_input(self, image_uuid: str):
        pass