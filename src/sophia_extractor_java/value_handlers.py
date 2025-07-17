from sophia_extractor_java import models


def handle_common_expr_JNewExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JNewExpr
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        # Jimple.NEW
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="new"
        ),
        # " "
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT, token_value=" "
        ),
        # type
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.getType().toString()),
        ),
    ]
    return v


def handle_common_expr_JCastExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JCastExpr
    """
    vtoken_type = None
    vtype = str(value.getOp().getClass().getTypeName())
    if vtype in [
        "sootup.java.core.jimple.basic.JavaLocal",
        "sootup.core.jimple.basic.Local",
    ]:
        vtoken_type = models.ValueTokenType.VARIABLE
    elif vtype in [
        "sootup.core.jimple.common.constant.StringConstant",
        "sootup.core.jimple.common.constant.NullConstant",
        "sootup.core.jimple.common.constant.IntConstant",
    ]:
        vtoken_type = models.ValueTokenType.CONSTANT
    else:
        raise Exception(vtype)

    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        # (
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="("
        ),
        # type
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE,
            token_value=str(value.getType().toString()),
        ),
        # )
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value=")"
        ),
        models.ValueTokenModel(
            token_type=vtoken_type,
            token_value=str(value.getOp().toString()),
        ),
    ]
    return v


def handle_basic_JavaLocal(value_type, value):
    """
    sootup.java.core.jimple.basic.JavaLocal
    sootup.core.jimple.basic.Local
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getName()),
        ),
    ]
    return v


def handle_common_ref_JThisRef(value_type, value):
    """
    Eg.
    @this: sootup.core.BaseViewChangeListener
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="@"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value="this",
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value=":"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=" ",
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE,
            token_value=str(value.getType().toString()),
        ),
    ]
    return v


def handle_common_ref_JParameterRef(value_type, value):
    """
    Eg.
    @parameter0: sootup.core.model.Body
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="@"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=f"parameter{value.getIndex()}",
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value=":"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=" ",
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE,
            token_value=str(value.getType().toString()),
        ),
    ]
    return v


def handle_common_ref_JCaughtExceptionRef(value_type, value):
    """
    Eg.
    @caughtexception
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="@"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value="caughtexception",
        ),
    ]
    return v


def handle_common_constant_NullConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_constant_IntConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_constant_StringConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),  # str(value.getValue())
        ),
    ]
    return v


def handle_common_constant_LongConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_constant_DoubleConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_constant_FloatConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_constant_ClassConstant(value_type, value):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.toString()),
        ),
    ]
    return v


def handle_common_expr_JInstanceOfExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JInstanceOfExpr
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        # op
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getOp().toString()),
        ),
        # Jimple.INSTANCEOF
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="instanceof"
        ),
        # checkType
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE,
            token_value=str(value.getCheckType().toString()),
        ),
    ]
    return v


def handle_common_expr_JNewArrayExpr(value_type, value):
    arr_ref_type = str(value.getSize().getClass().getTypeName())
    if arr_ref_type == "sootup.core.jimple.common.constant.IntConstant":
        index_model = models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.getSize()),
        )
    elif arr_ref_type == "sootup.java.core.jimple.basic.JavaLocal":
        index_model = models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getSize()),
        )
    else:
        raise Exception(arr_ref_type)

    """
    sootup.core.jimple.common.expr.JNewArrayExpr
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="newarray"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="("
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE, token_value=str(value.getBaseType())
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value=")"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="["
        ),
        index_model,
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="]"
        ),
    ]
    return v


def handle_common_expr_JNewMultiArrayExpr(value_type, value):
    def array_index_to_vaue_token(ref_value):
        arr_ref_type = str(ref_value.getClass().getTypeName())
        if arr_ref_type == "sootup.core.jimple.common.constant.IntConstant":
            return models.ValueTokenModel(
                token_type=models.ValueTokenType.CONSTANT,
                token_value=str(ref_value),
            )
        elif arr_ref_type == "sootup.java.core.jimple.basic.JavaLocal":
            return models.ValueTokenModel(
                token_type=models.ValueTokenType.VARIABLE,
                token_value=str(ref_value),
            )
        else:
            raise Exception(arr_ref_type)

    """
    sootup.core.jimple.common.expr.JNewMultiArrayExpr
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="newmultiarray"
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="("
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE, token_value=str(value.getBaseType())
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value=")"
        ),
    ]

    for ref_value in value.getSizes():
        arr_index_model = array_index_to_vaue_token(ref_value)
        v.value_tokens.append(
            models.ValueTokenModel(
                token_type=models.ValueTokenType.SYMBOL, token_value="["
            )
        )
        v.value_tokens.append(arr_index_model)
        v.value_tokens.append(
            models.ValueTokenModel(
                token_type=models.ValueTokenType.SYMBOL, token_value="]"
            )
        )

    """
    if there was no array indices, use empty array `[]`
    """
    if len(v.value_tokens) == 4:
        v.value_tokens.append(
            models.ValueTokenModel(
                token_type=models.ValueTokenType.SYMBOL, token_value="["
            )
        )
        v.value_tokens.append(
            models.ValueTokenModel(
                token_type=models.ValueTokenType.SYMBOL, token_value="]"
            )
        )

    return v


def handle_common_ref_JArrayRef(value_type, value):
    arr_ref_type = str(value.getIndex().getClass().getTypeName())
    if arr_ref_type == "sootup.core.jimple.common.constant.IntConstant":
        index_model = models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value=str(value.getIndex()),
        )
    elif arr_ref_type == "sootup.java.core.jimple.basic.JavaLocal":
        index_model = models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getIndex()),
        )
    else:
        raise Exception(arr_ref_type)

    """
    sootup.core.jimple.common.ref.JArrayRef
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getBase().toString()),
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="["
        ),
        index_model,
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="]"
        ),
    ]
    return v


def handle_common_ref_JStaticFieldRef(value_type, value):
    """
    sootup.core.jimple.common.ref.JInstanceFieldRef
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=f"{str(value.getFieldSignature().getClass().getName())}.{str(value.getFieldSignature().getName())}",  # noqa: E501
        ),
    ]
    return v


def handle_common_ref_JInstanceFieldRef(value_type, value):
    """
    sootup.core.jimple.common.ref.JInstanceFieldRef
    """
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE,
            token_value=str(value.getBase().toString()),
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.SYMBOL, token_value="."
        ),
        models.ValueTokenModel(
            token_type=models.ValueTokenType.ATTRIBUTE,
            token_value=str(value.getFieldSignature().getName()),
        ),
    ]
    return v


def handle_common_expr_JAddExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JAddExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="+",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JSubExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JSubExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="-",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JDivExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JDivExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="/",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JAndExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JAndExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="&",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JXorExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JXorExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="^",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JMulExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JMulExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="*",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JOrExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JOrExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="|",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JNegExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JNegExpr
    """
    lhs = value_handler(value.getOp().getClass().getTypeName(), value.getOp())

    return models.ExprModel(
        expr_type="neg",
        lhs=lhs,
    )


def handle_common_expr_JCmpgExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JCmpgExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="cmpg",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JCmplExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JCmplExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="cmpl",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JCmpExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JCmpExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="cmp",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JRemExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JRemExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="%",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JLengthExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JLengthExpr
    """
    lhs = value_handler(value.getOp().getClass().getTypeName(), value.getOp())

    return models.ExprModel(
        expr_type="lengthof",
        lhs=lhs,
    )


def handle_common_expr_JShrExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JShrExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type=">>",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JUshrExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JUshrExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type=">>>",
        lhs=lhs,
        rhs=rhs,
    )


def handle_common_expr_JShlExpr(value_type, value):
    """
    sootup.core.jimple.common.expr.JShlExpr
    """
    lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
    rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

    return models.ExprModel(
        expr_type="<<",
        lhs=lhs,
        rhs=rhs,
    )


def handle_cond(value_type, value):
    expr_type = None
    lhs = None
    rhs = None

    match value_type:
        case "sootup.core.jimple.common.expr.JEqExpr":
            expr_type = "=="
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case "sootup.core.jimple.common.expr.JNeExpr":
            expr_type = "!="
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case "sootup.core.jimple.common.expr.JGeExpr":
            expr_type = ">="
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case "sootup.core.jimple.common.expr.JLtExpr":
            expr_type = "<"
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case "sootup.core.jimple.common.expr.JLeExpr":
            expr_type = "<="
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case "sootup.core.jimple.common.expr.JGtExpr":
            expr_type = ">"
            lhs = value_handler(value.getOp1().getClass().getTypeName(), value.getOp1())
            rhs = value_handler(value.getOp2().getClass().getTypeName(), value.getOp2())

        case _:
            raise Exception(value_type, str(value))

    return models.ExprModel(
        expr_type=expr_type,
        lhs=lhs,
        rhs=rhs,
    )


def _generate_switch_default():
    v = models.ValueModel(
        value_type="sootup.core.jimple.common.constant.StringConstant"
    )
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT,
            token_value="default",
        ),
    ]
    return v


def fake_method_param_var(value_type, value_str):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.VARIABLE, token_value=str(value_str)
        ),
    ]
    return v


def fake_method_param_const(value_type, value_str):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.CONSTANT, token_value=str(value_str)
        ),
    ]
    return v


def fake_method_param_type(value_type, value_str):
    v = models.ValueModel(value_type=str(value_type))
    v.value_tokens = [
        models.ValueTokenModel(
            token_type=models.ValueTokenType.TYPE, token_value=str(value_str)
        ),
    ]
    return v


def value_handler_for_sootup_core(value_type, value):
    if value_type in [
        "sootup.core.jimple.common.expr.JEqExpr",
        "sootup.core.jimple.common.expr.JNeExpr",
        "sootup.core.jimple.common.expr.JGeExpr",
        "sootup.core.jimple.common.expr.JLtExpr",
        "sootup.core.jimple.common.expr.JLeExpr",
        "sootup.core.jimple.common.expr.JGtExpr",
    ]:
        return handle_cond(value_type, value)

    match value_type:
        case "sootup.core.jimple.common.ref.JThisRef":
            return handle_common_ref_JThisRef(value_type, value)

        case "sootup.core.jimple.common.ref.JParameterRef":
            return handle_common_ref_JParameterRef(value_type, value)

        case "sootup.core.jimple.common.ref.JCaughtExceptionRef":
            return handle_common_ref_JCaughtExceptionRef(value_type, value)

        case "sootup.core.jimple.common.expr.JNewExpr":
            return handle_common_expr_JNewExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JCastExpr":
            return handle_common_expr_JCastExpr(value_type, value)

        case "sootup.core.jimple.basic.Local":
            return handle_basic_JavaLocal(value_type, value)

        case "sootup.core.jimple.common.constant.NullConstant":
            return handle_common_constant_NullConstant(value_type, value)

        case "sootup.core.jimple.common.constant.IntConstant":
            return handle_common_constant_IntConstant(value_type, value)

        case "sootup.core.jimple.common.constant.StringConstant":
            return handle_common_constant_StringConstant(value_type, value)

        case "sootup.core.jimple.common.constant.LongConstant":
            return handle_common_constant_LongConstant(value_type, value)

        case "sootup.core.jimple.common.constant.DoubleConstant":
            return handle_common_constant_DoubleConstant(value_type, value)

        case "sootup.core.jimple.common.constant.FloatConstant":
            return handle_common_constant_FloatConstant(value_type, value)

        case "sootup.core.jimple.common.constant.ClassConstant":
            return handle_common_constant_ClassConstant(value_type, value)

        case "sootup.core.jimple.common.expr.JInstanceOfExpr":
            return handle_common_expr_JInstanceOfExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JNewArrayExpr":
            return handle_common_expr_JNewArrayExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JNewMultiArrayExpr":
            return handle_common_expr_JNewMultiArrayExpr(value_type, value)

        case "sootup.core.jimple.common.ref.JArrayRef":
            return handle_common_ref_JArrayRef(value_type, value)

        case "sootup.core.jimple.common.ref.JStaticFieldRef":
            return handle_common_ref_JStaticFieldRef(value_type, value)

        case "sootup.core.jimple.common.ref.JInstanceFieldRef":
            return handle_common_ref_JInstanceFieldRef(value_type, value)

        case "sootup.core.jimple.common.expr.JAddExpr":
            return handle_common_expr_JAddExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JSubExpr":
            return handle_common_expr_JSubExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JDivExpr":
            return handle_common_expr_JDivExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JAndExpr":
            return handle_common_expr_JAndExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JXorExpr":
            return handle_common_expr_JXorExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JOrExpr":
            return handle_common_expr_JOrExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JMulExpr":
            return handle_common_expr_JMulExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JNegExpr":
            return handle_common_expr_JNegExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JCmpgExpr":
            return handle_common_expr_JCmpgExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JCmplExpr":
            return handle_common_expr_JCmplExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JCmpExpr":
            return handle_common_expr_JCmpExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JRemExpr":
            return handle_common_expr_JRemExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JLengthExpr":
            return handle_common_expr_JLengthExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JShrExpr":
            return handle_common_expr_JShrExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JUshrExpr":
            return handle_common_expr_JUshrExpr(value_type, value)

        case "sootup.core.jimple.common.expr.JShlExpr":
            return handle_common_expr_JShlExpr(value_type, value)

        case _:
            raise Exception(value_type, str(value))


def value_handler_for_sootup_java(value_type, value):
    match value_type:
        case "sootup.java.core.jimple.basic.JavaLocal":
            return handle_basic_JavaLocal(value_type, value)

        case _:
            raise Exception(value_type, str(value))


def value_handler(value_type, value):
    if str(value_type).startswith("sootup.core"):
        return value_handler_for_sootup_core(value_type, value)

    elif str(value_type).startswith("sootup.java"):
        return value_handler_for_sootup_java(value_type, value)

    else:
        raise Exception(
            f"value handler begining with {str(value_type)} isn't supported"
        )
