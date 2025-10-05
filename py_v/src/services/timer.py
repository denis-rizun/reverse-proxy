from time import perf_counter


class Timer:
    def __init__(self) -> None:
        self._marks = {}

    def mark(self, name: str) -> None:
        self._marks[name] = perf_counter()

    def elapsed_ms(self, start_name: str, end_name: str) -> float:
        return (self._marks[end_name] - self._marks[start_name]) * 1000
