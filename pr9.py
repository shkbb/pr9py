from typing import Any, Callable, Iterable, TypeVar, Union, Dict, Tuple, List

T = TypeVar('T')
S = TypeVar('S')


def process_data(data: Union[List[T], Tuple[T, ...], Dict[Any, T]],
                 operation: Callable[[T], S],
                 dict_mode: str = 'values') -> Union[List[S], Tuple[S, ...], Dict[Any, S]]:
    try:
        if isinstance(data, dict):
            if dict_mode == 'keys':
                return {operation(k): v for k, v in data.items()}  
            elif dict_mode == 'values':
                return {k: operation(v) for k, v in data.items()} 
            elif dict_mode == 'both':
                return {operation(k): operation(v) for k, v in data.items()}  
            else:
                raise ValueError(f"Invalid dict_mode: {dict_mode}")
        elif isinstance(data, list):
            return [operation(elem) for elem in data] 
        elif isinstance(data, tuple):
            return tuple(operation(elem) for elem in data)  
        else:
            raise TypeError("Unsupported data type. Use list, tuple, or dict.")
    except Exception as e:
        return f"Error in process_data: {e}"


def filter_data(data: Union[List[T], Tuple[T, ...], Dict[Any, T]],
                predicate: Callable[[T], bool],
                dict_mode: str = 'values') -> Union[List[T], Tuple[T, ...], Dict[Any, T]]:
    try:
        if isinstance(data, dict):
            if dict_mode == 'keys':
                return {k: data[k] for k in data if predicate(k)} 
            elif dict_mode == 'values':
                return {k: v for k, v in data.items() if predicate(v)} 
            elif dict_mode == 'items':
                return {k: v for k, v in data.items() if predicate((k, v))} 
            else:
                raise ValueError(f"Invalid dict_mode: {dict_mode}")
        elif isinstance(data, list):
            return [elem for elem in data if predicate(elem)]
        elif isinstance(data, tuple):
            return tuple(elem for elem in data if predicate(elem)) 
        else:
            raise TypeError("Unsupported data type. Use list, tuple, or dict.")
    except Exception as e:
        return f"Error in filter_data: {e}"


def combine_values(*args: Union[int, float, str],
                   separator: str = '',
                   start: Union[int, float] = 0) -> Union[int, float, str]:
    try:
        if not args:
            raise ValueError("At least one argument is required.")

        first = args[0]
        if isinstance(first, (int, float)):
            total = start + first
            for val in args[1:]:
                if not isinstance(val, (int, float)):
                    raise TypeError("Cannot combine non-numeric value with numeric types.")
                total += val
            return total
        elif isinstance(first, str):
            parts = [first]
            for val in args[1:]:
                if not isinstance(val, str):
                    raise TypeError("Cannot combine non-string value with string types.")
                parts.append(val)
            return separator.join(parts)
        else:
            raise TypeError("Unsupported type. Use numeric or string types.")
    except Exception as e:
        return f"Error in combine_values: {e}"


if __name__ == "__main__":
    print(process_data([1, 2, 3], lambda x: x * 2))
    print(process_data((1, 2, 3), lambda x: x + 1))
    print(process_data({'a': 1, 'b': 2}, lambda x: x ** 2, dict_mode='values'))
    print(process_data({'a': 1, 'b': 2}, lambda x: x.upper(), dict_mode='keys'))

    print(filter_data([1, 2, 3, 4], lambda x: x % 2 == 0))
    print(filter_data(("a", "bb", "ccc"), lambda s: len(s) > 1))
    print(filter_data({'a': 1, 'b': 2, 'c': 3}, lambda v: v > 1, dict_mode='values'))

    print(combine_values(1, 2, 3, start=10))
    print(combine_values('a', 'b', 'c', separator='-'))
    print(combine_values())
