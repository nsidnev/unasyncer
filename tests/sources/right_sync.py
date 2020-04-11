from typing import Any, Iterator


def function_with_logic() -> None:
    pass


def function_with_prefix() -> None:
    pass


def common_function() -> None:
    pass


class ClassWithAsyncMethod:
    def regular_method(self) -> None:
        pass

    def method_with_prefix(self) -> None:
        function_with_prefix()

    def method_with_regular_name(self) -> None:
        print(ClassWithPrefix())

    def method_that_uses_iterator(self) -> None:
        for value in self:
            pass

    def method_that_uses_ctx_manager(self) -> None:
        with self:
            pass

    def __iter__(self) -> Iterator[int]:
        pass

    def __enter__(self, *args: Any) -> Any:
        pass

    def __exit__(self, *args: Any) -> Any:
        pass


class ClassWithPrefix:
    pass
