from time import process_time
from typing import ClassVar, Optional, Type


class Example:
    """This is the base class for all examples."""
    predecessor: ClassVar[Optional[Type['Example']]] = None

    @classmethod
    def set(cls):
        pass

    @classmethod
    def unset(cls):
        pass

    @classmethod
    def exec(cls):
        pass

    @classmethod
    def prepare(cls):
        if cls.predecessor is not None:
            cls.predecessor.prepare()
        cls.set()
        cls.unset()

    @classmethod
    def run(cls) -> tuple[str, float]:
        if cls.predecessor is not None:
            cls.predecessor.prepare()
        example: str = cls.__name__
        marker: str = '=' * 30
        print(f'{marker} Begin: {example} {marker}')
        cls.set()
        start: float = process_time()
        cls.exec()
        finish: float = process_time()
        elapsed: float = finish - start
        print(f'elapsed process time = {elapsed:.3f}')
        cls.unset()
        print(f'{marker} End:   {example} {marker}')

        return example, elapsed
