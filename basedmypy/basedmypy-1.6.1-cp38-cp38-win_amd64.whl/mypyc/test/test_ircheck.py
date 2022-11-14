from __future__ import annotations

import unittest

from mypyc.analysis.ircheck import FnError, can_coerce_to, check_func_ir
from mypyc.ir.class_ir import ClassIR
from mypyc.ir.func_ir import FuncDecl, FuncIR, FuncSignature
from mypyc.ir.ops import (
    Assign,
    BasicBlock,
    Goto,
    Integer,
    LoadAddress,
    LoadLiteral,
    Op,
    Register,
    Return,
)
from mypyc.ir.pprint import format_func
from mypyc.ir.rtypes import (
    RInstance,
    RType,
    RUnion,
    bytes_rprimitive,
    int32_rprimitive,
    int64_rprimitive,
    none_rprimitive,
    object_rprimitive,
    pointer_rprimitive,
    str_rprimitive,
)


def assert_has_error(fn: FuncIR, error: FnError) -> None:
    errors = check_func_ir(fn)
    assert errors == [error]


def assert_no_errors(fn: FuncIR) -> None:
    assert not check_func_ir(fn)


NONE_VALUE = Integer(0, rtype=none_rprimitive)


class TestIrcheck(unittest.TestCase):
    def setUp(self) -> None:
        self.label = 0

    def basic_block(self, ops: list[Op]) -> BasicBlock:
        self.label += 1
        block = BasicBlock(self.label)
        block.ops = ops
        return block

    def func_decl(self, name: str, ret_type: RType | None = None) -> FuncDecl:
        if ret_type is None:
            ret_type = none_rprimitive
        return FuncDecl(
            name=name,
            class_name=None,
            module_name="module",
            sig=FuncSignature(args=[], ret_type=ret_type),
        )

    def test_valid_fn(self) -> None:
        assert_no_errors(
            FuncIR(
                decl=self.func_decl(name="func_1"),
                arg_regs=[],
                blocks=[self.basic_block(ops=[Return(value=NONE_VALUE)])],
            )
        )

    def test_block_not_terminated_empty_block(self) -> None:
        block = self.basic_block([])
        fn = FuncIR(decl=self.func_decl(name="func_1"), arg_regs=[], blocks=[block])
        assert_has_error(fn, FnError(source=block, desc="Block not terminated"))

    def test_valid_goto(self) -> None:
        block_1 = self.basic_block([Return(value=NONE_VALUE)])
        block_2 = self.basic_block([Goto(label=block_1)])
        fn = FuncIR(decl=self.func_decl(name="func_1"), arg_regs=[], blocks=[block_1, block_2])
        assert_no_errors(fn)

    def test_invalid_goto(self) -> None:
        block_1 = self.basic_block([Return(value=NONE_VALUE)])
        goto = Goto(label=block_1)
        block_2 = self.basic_block([goto])
        fn = FuncIR(
            decl=self.func_decl(name="func_1"),
            arg_regs=[],
            # block_1 omitted
            blocks=[block_2],
        )
        assert_has_error(fn, FnError(source=goto, desc="Invalid control operation target: 1"))

    def test_invalid_register_source(self) -> None:
        ret = Return(value=Register(type=none_rprimitive, name="r1"))
        block = self.basic_block([ret])
        fn = FuncIR(decl=self.func_decl(name="func_1"), arg_regs=[], blocks=[block])
        assert_has_error(fn, FnError(source=ret, desc="Invalid op reference to register 'r1'"))

    def test_invalid_op_source(self) -> None:
        ret = Return(value=LoadLiteral(value="foo", rtype=str_rprimitive))
        block = self.basic_block([ret])
        fn = FuncIR(decl=self.func_decl(name="func_1"), arg_regs=[], blocks=[block])
        assert_has_error(
            fn, FnError(source=ret, desc="Invalid op reference to op of type LoadLiteral")
        )

    def test_invalid_return_type(self) -> None:
        ret = Return(value=Integer(value=5, rtype=int32_rprimitive))
        fn = FuncIR(
            decl=self.func_decl(name="func_1", ret_type=int64_rprimitive),
            arg_regs=[],
            blocks=[self.basic_block([ret])],
        )
        assert_has_error(
            fn, FnError(source=ret, desc="Cannot coerce source type int32 to dest type int64")
        )

    def test_invalid_assign(self) -> None:
        arg_reg = Register(type=int64_rprimitive, name="r1")
        assign = Assign(dest=arg_reg, src=Integer(value=5, rtype=int32_rprimitive))
        ret = Return(value=NONE_VALUE)
        fn = FuncIR(
            decl=self.func_decl(name="func_1"),
            arg_regs=[arg_reg],
            blocks=[self.basic_block([assign, ret])],
        )
        assert_has_error(
            fn, FnError(source=assign, desc="Cannot coerce source type int32 to dest type int64")
        )

    def test_can_coerce_to(self) -> None:
        cls = ClassIR(name="Cls", module_name="cls")
        valid_cases = [
            (int64_rprimitive, int64_rprimitive),
            (str_rprimitive, str_rprimitive),
            (str_rprimitive, object_rprimitive),
            (object_rprimitive, str_rprimitive),
            (RUnion([bytes_rprimitive, str_rprimitive]), str_rprimitive),
            (str_rprimitive, RUnion([bytes_rprimitive, str_rprimitive])),
            (RInstance(cls), object_rprimitive),
        ]

        invalid_cases = [
            (int64_rprimitive, int32_rprimitive),
            (RInstance(cls), str_rprimitive),
            (str_rprimitive, bytes_rprimitive),
        ]

        for src, dest in valid_cases:
            assert can_coerce_to(src, dest)
        for src, dest in invalid_cases:
            assert not can_coerce_to(src, dest)

    def test_duplicate_op(self) -> None:
        arg_reg = Register(type=int32_rprimitive, name="r1")
        assign = Assign(dest=arg_reg, src=Integer(value=5, rtype=int32_rprimitive))
        block = self.basic_block([assign, assign, Return(value=NONE_VALUE)])
        fn = FuncIR(decl=self.func_decl(name="func_1"), arg_regs=[], blocks=[block])
        assert_has_error(fn, FnError(source=assign, desc="Func has a duplicate op"))

    def test_pprint(self) -> None:
        block_1 = self.basic_block([Return(value=NONE_VALUE)])
        goto = Goto(label=block_1)
        block_2 = self.basic_block([goto])
        fn = FuncIR(
            decl=self.func_decl(name="func_1"),
            arg_regs=[],
            # block_1 omitted
            blocks=[block_2],
        )
        errors = [(goto, "Invalid control operation target: 1")]
        formatted = format_func(fn, errors)
        assert formatted == [
            "def func_1():",
            "L0:",
            "    goto L1",
            "  ERR: Invalid control operation target: 1",
        ]

    def test_load_address_declares_register(self) -> None:
        rx = Register(str_rprimitive, "x")
        ry = Register(pointer_rprimitive, "y")
        load_addr = LoadAddress(pointer_rprimitive, rx)
        assert_no_errors(
            FuncIR(
                decl=self.func_decl(name="func_1"),
                arg_regs=[],
                blocks=[
                    self.basic_block(
                        ops=[load_addr, Assign(ry, load_addr), Return(value=NONE_VALUE)]
                    )
                ],
            )
        )
