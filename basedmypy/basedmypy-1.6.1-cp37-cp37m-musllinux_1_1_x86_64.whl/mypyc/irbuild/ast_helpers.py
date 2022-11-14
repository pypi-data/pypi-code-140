"""IRBuilder AST transform helpers shared between expressions and statements.

Shared code that is tightly coupled to mypy ASTs can be put here instead of
making mypyc.irbuild.builder larger.
"""

from __future__ import annotations

from mypy.nodes import (
    LDEF,
    BytesExpr,
    ComparisonExpr,
    Expression,
    FloatExpr,
    IntExpr,
    MemberExpr,
    NameExpr,
    OpExpr,
    StrExpr,
    UnaryExpr,
    Var,
)
from mypyc.ir.ops import BasicBlock
from mypyc.ir.rtypes import is_fixed_width_rtype, is_tagged
from mypyc.irbuild.builder import IRBuilder
from mypyc.irbuild.constant_fold import constant_fold_expr


def process_conditional(
    self: IRBuilder, e: Expression, true: BasicBlock, false: BasicBlock
) -> None:
    if isinstance(e, OpExpr) and e.op in ["and", "or"]:
        if e.op == "and":
            # Short circuit 'and' in a conditional context.
            new = BasicBlock()
            process_conditional(self, e.left, new, false)
            self.activate_block(new)
            process_conditional(self, e.right, true, false)
        else:
            # Short circuit 'or' in a conditional context.
            new = BasicBlock()
            process_conditional(self, e.left, true, new)
            self.activate_block(new)
            process_conditional(self, e.right, true, false)
    elif isinstance(e, UnaryExpr) and e.op == "not":
        process_conditional(self, e.expr, false, true)
    else:
        res = maybe_process_conditional_comparison(self, e, true, false)
        if res:
            return
        # Catch-all for arbitrary expressions.
        reg = self.accept(e)
        self.add_bool_branch(reg, true, false)


def maybe_process_conditional_comparison(
    self: IRBuilder, e: Expression, true: BasicBlock, false: BasicBlock
) -> bool:
    """Transform simple tagged integer comparisons in a conditional context.

    Return True if the operation is supported (and was transformed). Otherwise,
    do nothing and return False.

    Args:
        e: Arbitrary expression
        true: Branch target if comparison is true
        false: Branch target if comparison is false
    """
    if not isinstance(e, ComparisonExpr) or len(e.operands) != 2:
        return False
    ltype = self.node_type(e.operands[0])
    rtype = self.node_type(e.operands[1])
    if not (
        (is_tagged(ltype) or is_fixed_width_rtype(ltype))
        and (is_tagged(rtype) or is_fixed_width_rtype(rtype))
    ):
        return False
    op = e.operators[0]
    if op not in ("==", "!=", "<", "<=", ">", ">="):
        return False
    left_expr = e.operands[0]
    right_expr = e.operands[1]
    borrow_left = is_borrow_friendly_expr(self, right_expr)
    left = self.accept(left_expr, can_borrow=borrow_left)
    right = self.accept(right_expr, can_borrow=True)
    if is_fixed_width_rtype(ltype) or is_fixed_width_rtype(rtype):
        if not is_fixed_width_rtype(ltype):
            left = self.coerce(left, rtype, e.line)
        elif not is_fixed_width_rtype(rtype):
            right = self.coerce(right, ltype, e.line)
        reg = self.binary_op(left, right, op, e.line)
        self.builder.flush_keep_alives()
        self.add_bool_branch(reg, true, false)
    else:
        # "left op right" for two tagged integers
        self.builder.compare_tagged_condition(left, right, op, true, false, e.line)
    return True


def is_borrow_friendly_expr(self: IRBuilder, expr: Expression) -> bool:
    """Can the result of the expression borrowed temporarily?

    Borrowing means keeping a reference without incrementing the reference count.
    """
    if isinstance(expr, (IntExpr, FloatExpr, StrExpr, BytesExpr)):
        # Literals are immortal and can always be borrowed
        return True
    if (
        isinstance(expr, (UnaryExpr, OpExpr, NameExpr, MemberExpr))
        and constant_fold_expr(self, expr) is not None
    ):
        # Literal expressions are similar to literals
        return True
    if isinstance(expr, NameExpr):
        if isinstance(expr.node, Var) and expr.kind == LDEF:
            # Local variable reference can be borrowed
            return True
    if isinstance(expr, MemberExpr) and self.is_native_attr_ref(expr):
        return True
    return False
