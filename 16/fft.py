from typing import Iterable, List
from itertools import cycle, repeat, chain

def weights(n: int) -> Iterable[int]:
    it = cycle(chain(repeat(0, n), 
                     repeat(1, n),
                     repeat(0, n),
                     repeat(-1, n)))
    _ = next(it)
    return it

def apply_phase(signal: List[int]) -> List[int]:
    result: List[int] = []
    for n in range(len(signal)):
        result.append(sum(x * y for x, y in zip(signal, weights(n + 1))))
    return [abs(x) % 10 for x in result]

def ft(signal: List[int], phases: int) -> int:
    for _ in range(phases):
        signal = apply_phase(signal)
    return int(''.join(map(str, signal)))

def parse_into_signal(s: str, repeat: int=1) -> List[int]:
    return [int(x) for x in s] * repeat

def repeat_backsolve(signal: List[int], n_times: int=1) -> List[int]:
    for _ in range(n_times):
        signal = backsolve(signal)
    return signal

def backsolve(signal: List[int]) -> List[int]:
    """A backwards culative sum."""
    reversed_cumsum = 0
    reversed_cumsums: List[int] = [0] * len(signal)
    for i, n in enumerate(reversed(signal)):
        reversed_cumsum += n
        reversed_cumsums[i] = reversed_cumsum % 10
    return reversed_cumsums[::-1]


assert ft(parse_into_signal('12345678'), 4) == 1029498 
assert backsolve([1, 1, 1, 1]) == ([4, 3, 2, 1]) 

RAW_SIGNAL = '59765216634952147735419588186168416807782379738264316903583191841332176615408501571822799985693486107923593120590306960233536388988005024546603711148197317530759761108192873368036493650979511670847453153419517502952341650871529652340965572616173116797325184487863348469473923502602634441664981644497228824291038379070674902022830063886132391030654984448597653164862228739130676400263409084489497532639289817792086185750575438406913771907404006452592544814929272796192646846314361074786728172308710864379023028807580948201199540396460310280533771566824603456581043215999473424395046570134221182852363891114374810263887875638355730605895695123598637121'
TEST_SIGNAL = '03036732577212944063491565474664'

# assert str(ft(parse_into_signal(RAW_SIGNAL), 100))[:8] == '70856418'

# backsolved = repeat_backsolve(parse_into_signal(TEST_SIGNAL, repeat=10_000), n_times=100)
# message_location = int(TEST_SIGNAL[:7])
# message = backsolved[message_location : message_location + 8]
# assert message == [8, 4, 4, 6, 2, 0, 2, 6]

backsolved = repeat_backsolve(parse_into_signal(RAW_SIGNAL, repeat=10_000), n_times=100)
message_location = int(RAW_SIGNAL[:7])
message = backsolved[message_location : message_location + 8]
print(f"The message is {message}")
