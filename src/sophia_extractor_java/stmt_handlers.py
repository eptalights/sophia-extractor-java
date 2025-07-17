from sophia_extractor_java import models
from sophia_extractor_java import value_handlers


def handle_JIdentityStmt(block_index, stmt_type, stmt):
    """
    Assign special values to locals at the start of a method.
    Common for parameters and this.

    example::
    this := @this: target.exercise1.DemoClass;
    """

    _right = value_handlers.value_handler(
        value_type=stmt.getRightOp().getClass().getTypeName(),
        value=stmt.getRightOp(),
    )

    _left = value_handlers.value_handler(
        value_type=stmt.getLeftOp().getClass().getTypeName(),
        value=stmt.getLeftOp(),
    )

    return models.JIdentityStmtModel(
        left=_left,
        right=_right,
    )


def handle_JInvokeStmt(block_index, stmt_type, stmt):
    """
    represents a method invocation as a statement in Jimple, like:
    invoke static <MyClass: void foo()>()
    virtualinvoke r0.<MyClass: void bar(int)>(5)

    transfers the control flow to another method until the called method returns.
    """

    invoke_expr = stmt.getInvokeExpr()
    if not invoke_expr.isPresent():
        print(stmt)
        raise Exception("find why its not present")

    invoke_expr = invoke_expr.get()
    clsname = str(invoke_expr.getClass().getTypeName())

    if clsname == "sootup.core.jimple.common.expr.JSpecialInvokeExpr":
        method_signature = invoke_expr.getMethodSignature()
        method_name = method_signature.getName()
        method_base = invoke_expr.getBase().getName()
        method_name_type = str(method_signature.getClass().getTypeName())
        method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

    elif clsname == "sootup.core.jimple.common.expr.JInterfaceInvokeExpr":
        method_signature = invoke_expr.getMethodSignature()
        method_name = method_signature.getName()
        method_base = invoke_expr.getBase().getName()
        method_name_type = str(method_signature.getClass().getTypeName())
        method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

    elif clsname == "sootup.core.jimple.common.expr.JStaticInvokeExpr":
        method_signature = invoke_expr.getMethodSignature()
        method_name = method_signature.getName()
        method_base = None
        method_name_type = str(method_signature.getClass().getTypeName())
        method_base_type = None

    elif clsname == "sootup.core.jimple.common.expr.JVirtualInvokeExpr":
        method_signature = invoke_expr.getMethodSignature()
        method_name = method_signature.getName()
        method_base = invoke_expr.getBase().getName()
        method_name_type = str(method_signature.getClass().getTypeName())
        method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

    else:
        print(stmt)
        raise Exception("handle_JInvokeStmt", clsname)

    call_args = []
    for arg in invoke_expr.getArgs():
        _arg = value_handlers.value_handler(
            value_type=arg.getClass().getTypeName(),
            value=arg,
        )
        call_args.append(_arg)

    return models.JInvokeStmtModel(
        method_base=str(method_base) if method_base is not None else None,
        method_name=str(method_name) if method_name is not None else None,
        method_name_type=method_name_type,
        method_base_type=method_base_type,
        args=call_args,
    )


def handle_JReturnVoidStmt(block_index, stmt_type, stmt):
    """
    It represents a return; statement in a method that returns void.
    """

    return models.JReturnVoidStmtModel()


def handle_JNopStmt(block_index, stmt_type, stmt):
    return models.JNopStmtModel()


def handle_JReturnStmt(block_index, stmt_type, stmt):
    """
    It represents a return;
    """
    _arg = value_handlers.value_handler(
        value_type=stmt.getOp().getClass().getTypeName(),
        value=stmt.getOp(),
    )

    return models.JReturnStmtModel(
        arg=_arg,
    )


def handle_JThrowStmt(block_index, stmt_type, stmt):
    """
    Ends the execution inside the current Method if the thrown exception is
    not caught by a Trap, which redirects the execution to an exceptionhandler.
    """
    _arg = value_handlers.value_handler(
        value_type=stmt.getOp().getClass().getTypeName(),
        value=stmt.getOp(),
    )

    return models.JThrowStmtModel(
        arg=_arg,
    )


def handle_JAssignStmt(block_index, stmt_type, stmt, body=None):
    """
    assigns a Value from the right hand-side to the left hand-side.
    Left hand-side of an assignment can be a Local referencing a variable (i.e. a Local)
    or a FieldRef referencing a Field. Right hand-side of an assignment
    can be an expression (Expr), a Local, a FieldRef or a Constant.
    """
    _left = value_handlers.value_handler(
        value_type=stmt.getLeftOp().getClass().getTypeName(),
        value=stmt.getLeftOp(),
    )

    rtype = str(stmt.getRightOp().getClass().getTypeName())

    if rtype == "sootup.core.jimple.common.expr.JInstanceOfExpr":
        value = stmt.getRightOp()
        call_args = []

        arg1 = value_handlers.fake_method_param_var(
            value_type=str(value.getOp().getClass().getTypeName()),
            value_str=str(value.getOp().toString()),
        )
        call_args.append(arg1)

        arg2 = value_handlers.fake_method_param_type(
            value_type=str(value.getCheckType().getClass().getTypeName()),
            value_str=str(value.getCheckType().toString()),
        )
        call_args.append(arg2)

        return models.JInvokeStmtModel(
            method_base=None,
            method_name="instanceof",
            method_name_type=rtype,
            method_base_type=None,
            args=call_args,
            return_arg=_left,
        )

    if "Invoke" in rtype:
        if rtype not in [
            "sootup.core.jimple.common.expr.JStaticInvokeExpr",
            "sootup.core.jimple.common.expr.JVirtualInvokeExpr",
            "sootup.core.jimple.common.expr.JDynamicInvokeExpr",
            "sootup.core.jimple.common.expr.JInterfaceInvokeExpr",
            "sootup.core.jimple.common.expr.JSpecialInvokeExpr",
        ]:
            print(stmt.getRightOp())
            raise Exception(rtype)

        invoke_expr = stmt.getRightOp()
        call_args = []

        if rtype == "sootup.core.jimple.common.expr.JSpecialInvokeExpr":
            method_signature = invoke_expr.getMethodSignature()
            method_name = method_signature.getName()
            method_base = invoke_expr.getBase().getName()
            method_name_type = str(method_signature.getClass().getTypeName())
            method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

        if rtype == "sootup.core.jimple.common.expr.JInterfaceInvokeExpr":
            method_signature = invoke_expr.getMethodSignature()
            method_name = method_signature.getName()
            method_base = invoke_expr.getBase().getName()
            method_name_type = str(method_signature.getClass().getTypeName())
            method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

        if rtype == "sootup.core.jimple.common.expr.JStaticInvokeExpr":
            method_signature = invoke_expr.getMethodSignature()
            method_name = method_signature.getName()
            method_base = None
            method_name_type = str(method_signature.getClass().getTypeName())
            method_base_type = None

        if rtype == "sootup.core.jimple.common.expr.JVirtualInvokeExpr":
            method_signature = invoke_expr.getMethodSignature()
            method_name = method_signature.getName()
            method_base = invoke_expr.getBase().getName()
            method_name_type = str(method_signature.getClass().getTypeName())
            method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

        if rtype == "sootup.core.jimple.common.expr.JSpecialInvokeExpr":
            method_signature = invoke_expr.getMethodSignature()
            method_name = method_signature.getName()
            method_base = invoke_expr.getBase().getName()
            method_name_type = str(method_signature.getClass().getTypeName())
            method_base_type = str(invoke_expr.getBase().getClass().getTypeName())

        if rtype == "sootup.core.jimple.common.expr.JDynamicInvokeExpr":
            decl_class_type = str(
                invoke_expr.getBootstrapMethodSignature().getDeclClassType()
            )

            if decl_class_type not in [
                "java.lang.invoke.LambdaMetafactory",
                "java.lang.invoke.StringConcatFactory",
            ]:
                raise Exception(
                    f"JDynamicInvokeExpr for {decl_class_type} not supported"
                )

            if decl_class_type == "java.lang.invoke.StringConcatFactory":
                method_signature = invoke_expr.getMethodSignature()
                method_name = method_signature.getName()
                method_name_type = str(method_signature.getClass().getTypeName())
                method_base = str(
                    invoke_expr.getBootstrapMethodSignature()
                    .getDeclClassType()
                    .toString()
                )
                method_base_type = str(
                    invoke_expr.getBootstrapMethodSignature()
                    .getDeclClassType()
                    .getClass()
                    .getTypeName()
                )

                for immd_arg in invoke_expr.getBootstrapArgs():
                    _arg = value_handlers.value_handler(
                        value_type=immd_arg.getClass().getTypeName(),
                        value=immd_arg,
                    )
                    call_args.append(_arg)

            if decl_class_type == "java.lang.invoke.LambdaMetafactory":
                for immd_arg in invoke_expr.getBootstrapArgs():
                    type_name = "sootup.core.jimple.common.constant.MethodHandle"
                    if immd_arg.getClass().getTypeName() == type_name:
                        ref_sig = immd_arg.getReferenceSignature()
                        method_base = str(ref_sig.getDeclClassType().toString())
                        method_name = str(ref_sig.getName().toString())
                        method_name_type = str(ref_sig.getClass().getTypeName())
                        method_base_type = str(
                            ref_sig.getDeclClassType().getClass().getTypeName()
                        )

        for arg in invoke_expr.getArgs():
            _arg = value_handlers.value_handler(
                value_type=arg.getClass().getTypeName(),
                value=arg,
            )
            call_args.append(_arg)

        return models.JInvokeStmtModel(
            method_base=str(method_base) if method_base is not None else None,
            method_name=str(method_name) if method_name is not None else None,
            method_name_type=method_name_type,
            method_base_type=method_base_type,
            args=call_args,
            return_arg=_left,
        )

    else:
        _expr = None

        _right = value_handlers.value_handler(
            value_type=stmt.getRightOp().getClass().getTypeName(),
            value=stmt.getRightOp(),
        )
        if isinstance(_right, models.ValueModel):
            _expr = models.ExprModel(lhs=_right)

        elif isinstance(_right, models.ExprModel):
            _expr = _right

        else:
            raise Exception()

        return models.JAssignStmtModel(
            block_index=block_index,
            left=_left,
            right=_expr,
        )


def handle_JGotoStmt(block_index, stmt_type, stmt, block_successors):
    """
    we have two instances of JGotoStmt :
    "goto[?=return]" and "goto[?=(branch)]".
    """
    if not block_successors[block_index]:
        raise Exception("goto requires branches")

    return models.JGotoStmtModel(
        targets=block_successors[block_index],
    )


def handle_JIfStmt(block_index, stmt_type, stmt, block_successors):
    """
    we have two instances of JGotoStmt :
    "goto[?=return]" and "goto[?=(branch)]".
    """
    if not block_successors[block_index]:
        raise Exception("if requires branches")

    cond = stmt.getCondition()
    _expr = value_handlers.value_handler(
        value_type=cond.getClass().getTypeName(),
        value=cond,
    )

    return models.JIfStmtModel(
        src=_expr,
        true_block_index=block_successors[block_index][0],
        false_block_index=block_successors[block_index][1],
    )


def handle_JSwitchStmt(
    block_index, stmt_type, stmt, block_successors, body, block_stmts
):
    if not block_successors[block_index]:
        raise Exception("if requires branches")

    switch_index = value_handlers.value_handler(
        value_type=stmt.getKey().getClass().getTypeName(),
        value=stmt.getKey(),
    )
    switch_cases = []
    switch_targets = []

    edges = block_successors[block_index]

    """
    get the first stmt from each block edges
    """
    stmt_edges = [block_stmts[block_index][0] for block_index in edges]

    """
    get switch case values
    """
    for case_index, case in enumerate(stmt.getValues().toArray()):
        case_value = value_handlers.value_handler(
            value_type=case.getClass().getTypeName(),
            value=case,
        )
        switch_cases.append(case_value)

    """
    if cases are less than edges, it means switch has a default case
    """
    if len(switch_cases) < len(edges):
        case_value = value_handlers._generate_switch_default()
        switch_cases.append(case_value)

    for branch_stmt in stmt.getTargetStmts(body):
        if branch_stmt not in stmt_edges:
            raise Exception()

        stmt_block_index = stmt_edges.index(branch_stmt)
        switch_targets.append(edges[stmt_block_index])

    return models.JSwitchStmtModel(
        switch_index=switch_index,
        switch_cases=switch_cases,
        switch_targets=switch_targets,
    )


def stmt_handler(
    block_index, stmt_type, stmt, block_successors=None, body=None, block_stmts=None
):
    match stmt_type:
        case "JNopStmt":
            return handle_JNopStmt(block_index, stmt_type, stmt)
        case "JEnterMonitorStmt":
            return handle_JNopStmt(block_index, stmt_type, stmt)
        case "JExitMonitorStmt":
            return handle_JNopStmt(block_index, stmt_type, stmt)
        case "JBreakpointStmt":
            return handle_JNopStmt(block_index, stmt_type, stmt)
        case "JRetStmt":
            return handle_JNopStmt(block_index, stmt_type, stmt)
        case "JIdentityStmt":
            return handle_JIdentityStmt(block_index, stmt_type, stmt)
        case "JReturnStmt":
            return handle_JReturnStmt(block_index, stmt_type, stmt)
        case "JReturnVoidStmt":
            return handle_JReturnVoidStmt(block_index, stmt_type, stmt)
        case "JThrowStmt":
            return handle_JThrowStmt(block_index, stmt_type, stmt)
        case "JGotoStmt":
            return handle_JGotoStmt(block_index, stmt_type, stmt, block_successors)
        case "JIfStmt":
            return handle_JIfStmt(block_index, stmt_type, stmt, block_successors)
        case "JSwitchStmt":
            return handle_JSwitchStmt(
                block_index, stmt_type, stmt, block_successors, body, block_stmts
            )
        case "JInvokeStmt":
            return handle_JInvokeStmt(block_index, stmt_type, stmt)
        case "JAssignStmt":
            return handle_JAssignStmt(block_index, stmt_type, stmt, body=body)
        case _:
            raise Exception("stmt_type not found -- ", stmt_type, str(stmt))

    return True
