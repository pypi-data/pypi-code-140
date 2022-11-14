"""Translate an Expression to a Type value."""

from __future__ import annotations

from mypy.fastparse import parse_type_string
from mypy.nodes import (
    BytesExpr,
    CallExpr,
    ComplexExpr,
    EllipsisExpr,
    Expression,
    FloatExpr,
    IndexExpr,
    IntExpr,
    ListExpr,
    MemberExpr,
    NameExpr,
    OpExpr,
    RefExpr,
    StrExpr,
    TupleExpr,
    UnaryExpr,
    get_member_expr_fullname,
)
from mypy.options import Options
from mypy.types import (
    ANNOTATED_TYPE_NAMES,
    CallableArgument,
    EllipsisType,
    ProperType,
    RawExpressionType,
    Type,
    TypeList,
    UnboundType,
    UnionType,
    UntypedType,
)


class TypeTranslationError(Exception):
    """Exception raised when an expression is not valid as a type."""


def _extract_argument_name(expr: Expression) -> str | None:
    if isinstance(expr, NameExpr) and expr.name == "None":
        return None
    elif isinstance(expr, StrExpr):
        return expr.value
    else:
        raise TypeTranslationError()


def expr_to_unanalyzed_type(
    expr: Expression,
    options: Options | None = None,
    allow_new_syntax: bool = False,
    _parent: Expression | None = None,
) -> ProperType:
    """Translate an expression to the corresponding type.

    The result is not semantically analyzed. It can be UnboundType or TypeList.
    Raise TypeTranslationError if the expression cannot represent a type.

    If allow_new_syntax is True, allow all type syntax independent of the target
    Python version (used in stubs).
    """
    # The `parent` parameter is used in recursive calls to provide context for
    # understanding whether an CallableArgument is ok.
    name: str | None = None
    if isinstance(expr, NameExpr):
        name = expr.name
        if name == "True":
            return RawExpressionType(
                True,
                "builtins.bool",
                line=expr.line,
                column=expr.column,
                expression=not allow_new_syntax,
            )
        elif name == "False":
            return RawExpressionType(
                False,
                "builtins.bool",
                line=expr.line,
                column=expr.column,
                expression=not allow_new_syntax,
            )
        else:
            return UnboundType(name, line=expr.line, column=expr.column)
    elif isinstance(expr, MemberExpr):
        fullname = get_member_expr_fullname(expr)
        if fullname:
            return UnboundType(fullname, line=expr.line, column=expr.column, expression=True)
        else:
            raise TypeTranslationError()
    elif isinstance(expr, IndexExpr):
        base = expr_to_unanalyzed_type(expr.base, options, allow_new_syntax, expr)
        if isinstance(base, UnboundType):
            if base.args:
                raise TypeTranslationError()
            if isinstance(expr.index, TupleExpr):
                args = expr.index.items
            else:
                args = [expr.index]

            if isinstance(expr.base, RefExpr) and expr.base.fullname in ANNOTATED_TYPE_NAMES:
                # TODO: this is not the optimal solution as we are basically getting rid
                # of the Annotation definition and only returning the type information,
                # losing all the annotations.

                return expr_to_unanalyzed_type(args[0], options, allow_new_syntax, expr)
            else:
                base.args = tuple(
                    expr_to_unanalyzed_type(arg, options, allow_new_syntax, expr) for arg in args
                )
            if not base.args:
                base.empty_tuple_index = True
            return base
        else:
            raise TypeTranslationError()
    elif (
        isinstance(expr, OpExpr)
        and expr.op == "|"
        and ((options and options.python_version >= (3, 10)) or allow_new_syntax)
    ):
        return UnionType(
            [
                expr_to_unanalyzed_type(expr.left, options, allow_new_syntax),
                expr_to_unanalyzed_type(expr.right, options, allow_new_syntax),
            ]
        )
    elif isinstance(expr, CallExpr) and isinstance(_parent, ListExpr):
        c = expr.callee
        names = []
        # Go through the dotted member expr chain to get the full arg
        # constructor name to look up
        while True:
            if isinstance(c, NameExpr):
                names.append(c.name)
                break
            elif isinstance(c, MemberExpr):
                names.append(c.name)
                c = c.expr
            else:
                raise TypeTranslationError()
        arg_const = ".".join(reversed(names))

        # Go through the constructor args to get its name and type.
        name = None
        default_type = UntypedType()
        typ: Type = default_type
        for i, arg in enumerate(expr.args):
            if expr.arg_names[i] is not None:
                if expr.arg_names[i] == "name":
                    if name is not None:
                        # Two names
                        raise TypeTranslationError()
                    name = _extract_argument_name(arg)
                    continue
                elif expr.arg_names[i] == "type":
                    if typ is not default_type:
                        # Two types
                        raise TypeTranslationError()
                    typ = expr_to_unanalyzed_type(arg, options, allow_new_syntax, expr)
                    continue
                else:
                    raise TypeTranslationError()
            elif i == 0:
                typ = expr_to_unanalyzed_type(arg, options, allow_new_syntax, expr)
            elif i == 1:
                name = _extract_argument_name(arg)
            else:
                raise TypeTranslationError()
        return CallableArgument(typ, name, arg_const, expr.line, expr.column)
    elif isinstance(expr, ListExpr):
        return TypeList(
            [expr_to_unanalyzed_type(t, options, allow_new_syntax, expr) for t in expr.items],
            line=expr.line,
            column=expr.column,
        )
    elif isinstance(expr, StrExpr):
        return parse_type_string(expr.value, "builtins.str", expr.line, expr.column)
    elif isinstance(expr, BytesExpr):
        return parse_type_string(expr.value, "builtins.bytes", expr.line, expr.column)
    elif isinstance(expr, UnaryExpr):
        typ = expr_to_unanalyzed_type(expr.expr, options, allow_new_syntax)
        if isinstance(typ, RawExpressionType):
            if isinstance(typ.literal_value, int) and expr.op == "-":
                typ.literal_value *= -1
                return typ
        raise TypeTranslationError()
    elif isinstance(expr, IntExpr):
        return RawExpressionType(
            expr.value,
            "builtins.int",
            line=expr.line,
            column=expr.column,
            expression=not allow_new_syntax,
        )
    elif isinstance(expr, FloatExpr):
        # Floats are not valid parameters for RawExpressionType , so we just
        # pass in 'None' for now. We'll report the appropriate error at a later stage.
        return RawExpressionType(None, "builtins.float", line=expr.line, column=expr.column)
    elif isinstance(expr, ComplexExpr):
        # Same thing as above with complex numbers.
        return RawExpressionType(None, "builtins.complex", line=expr.line, column=expr.column)
    elif isinstance(expr, EllipsisExpr):
        return EllipsisType(expr.line)
    else:
        raise TypeTranslationError()
