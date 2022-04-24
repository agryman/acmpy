from acmpy.acm1_4 import *


def main() -> None:
    parsed_ops: KTSOps = Parse_RadialOp_List([Radial_D2b])
    assert len(parsed_ops) == 1

    parsed_op: KTOp = parsed_ops[0]
    assert isinstance(parsed_op, KTOp)

    print(f'K={parsed_op.K}, T={parsed_op.T}')
    assert parsed_op.K == 0
    assert parsed_op.T == 2


if __name__ == '__main__':
    main()
