from typing import Any, AsyncIterator


async def function_with_logic() -> None:
    pass


async def async_function_with_prefix() -> None:
    pass


def common_function() -> None:
    pass


class ClassWithAsyncMethod:
    def regular_method(self) -> None:
        pass

    async def async_method_with_prefix(self) -> None:
        await async_function_with_prefix()

    async def method_with_regular_name(self) -> None:
        print(AsyncClassWithPrefix())

    async def method_that_uses_iterator(self) -> None:
        async for value in self:
            pass

    async def method_that_uses_ctx_manager(self) -> None:
        async with self:
            pass

    async def __aiter__(self) -> AsyncIterator[int]:
        pass

    async def __aenter__(self, *args: Any) -> Any:
        pass

    async def __aexit__(self, *args: Any) -> Any:
        pass


class AsyncClassWithPrefix:
    pass
