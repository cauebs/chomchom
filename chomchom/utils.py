from itertools import combinations, chain


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r)
                               for r in range(0, len(s)+1))


def format_dict(dict, prefix) -> str:
    return '\n'.join(
        f"{prefix}({str(nt)}) = {{{', '.join(str(f) for f in firsts)}}}"
        for nt, firsts in dict.items()
    )


def format_follow(grammar) -> str:
    return '\n'.join(
        f"follow({str(nt)}) = {{{', '.join(str(f) for f in follows)}}}"
        for nt, follows in grammar.follow.items()
    )
