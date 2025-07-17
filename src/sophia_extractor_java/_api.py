import jpype
import jpype.imports
from jpype.types import JClass
from sophia_extractor_java import models
from sophia_extractor_java import value_handlers
from sophia_extractor_java.stmt_handlers import stmt_handler
from pprint import pprint
from pathlib import Path

base_dir = Path(__file__).resolve().parent
jars = [
    f"{str(base_dir)}/jars/sootup.core-2.0.0-SNAPSHOT.jar",
    f"{str(base_dir)}/jars/sootup.java.core-2.0.0-SNAPSHOT.jar",
    f"{str(base_dir)}/jars/sootup.java.bytecode.frontend-2.0.0-SNAPSHOT.jar",
    f"{str(base_dir)}/jars/sootup.interceptors-2.0.0-SNAPSHOT.jar",
    f"{str(base_dir)}/jars/slf4j-api-2.0.17.jar",
    f"{str(base_dir)}/jars/guava-33.4.6-jre.jar",
    f"{str(base_dir)}/jars/failureaccess-1.0.3.jar",
    f"{str(base_dir)}/jars/asm-9.8.jar",
    f"{str(base_dir)}/jars/asm-util-9.8.jar",
    f"{str(base_dir)}/jars/asm-commons-9.8.jar",
    f"{str(base_dir)}/jars/asm-tree-9.8.jar",
    f"{str(base_dir)}/jars/commons-io-2.18.0.jar",
    f"{str(base_dir)}/jars/commons-lang3-3.17.0.jar",
    f"{str(base_dir)}/jars/jgrapht-core-1.5.2.jar",
]
jpype.startJVM(classpath=jars)

from sootup.core.inputlocation import AnalysisInputLocation
from sootup.core.views import View
from sootup.java.core.views import JavaView
from sootup.java.bytecode.frontend.inputlocation import (
    JavaClassPathAnalysisInputLocation,
)


def extract_class(jvm_class, binary_filepath):
    class_model = models.JVMClassModel(
        filename=binary_filepath,
        name=str(jvm_class.getName()),
        class_source=str(jvm_class.getClassSource()),
        is_public=jvm_class.isPublic(),
        is_private=jvm_class.isPrivate(),
        is_static=jvm_class.isStatic(),
        is_concrete=jvm_class.isConcrete(),
        is_abstract=jvm_class.isAbstract(),
        is_annotation=jvm_class.isAnnotation(),
        is_interface=jvm_class.isInterface(),
        is_application_class=jvm_class.isApplicationClass(),
        is_enum=jvm_class.isEnum(),
        is_final=jvm_class.isFinal(),
        is_inner_class=jvm_class.isInnerClass(),
        is_library_class=jvm_class.isLibraryClass(),
        is_super=jvm_class.isSuper(),
    )

    for iface in jvm_class.getInterfaces():
        class_model.interfaces.append(str(iface.toString()))

    # Some static fields are initialized with assigned values, which can be retrieved
    # by inspecting the <clinit> (class initializer) method.
    #
    # To determine the initial values of static fields, analyze the body of
    # the <clinit> method, where static field initializations are performed.
    #
    # For example, the Java field:
    #     public static boolean MUST_CALL_CONSTRUCTOR_BEFORE_RETURN = false;
    #
    # Will be compiled into:
    #     static void <clinit>() {
    #         MUST_CALL_CONSTRUCTOR_BEFORE_RETURN = 0;
    #     }
    for field in jvm_class.getFields():
        prop_model = models.ClassPropertyModel(
            name=str(field.getName()),
            is_public=field.isPublic(),
            is_private=field.isPrivate(),
            is_static=field.isStatic(),
            is_protected=field.isProtected(),
            is_final=field.isFinal(),
            type=str(field.getType().toString()),
        )
        class_model.class_props.append(prop_model)

    if jvm_class.hasOuterClass():
        class_model.outer_class = str(
            jvm_class.getOuterClass().get().getFullyQualifiedName()
        )

    if jvm_class.hasSuperclass():
        class_model.super_class = str(
            jvm_class.getSuperclass().get().getFullyQualifiedName()
        )

    mindex = 1
    for method in jvm_class.getMethods():
        method_model = models.MethodModel(
            name=str(method.getName()),
            return_type=str(method.getReturnType().toString()),
            is_public=method.isPublic(),
            is_private=method.isPrivate(),
            is_static=method.isStatic(),
            is_protected=method.isProtected(),
            is_native=method.isNative(),
            is_final=method.isFinal(),
            is_concrete=method.isConcrete(),
            is_abstract=method.isAbstract(),
            has_body=method.hasBody(),
            param_count=method.getParameterCount(),
        )

        # Some methods do not have a body because they are either abstract or native.
        # For such methods, a ResolveException is thrown.
        if method_model.has_body is False:
            # Manually generate the method parameters
            for idx, t in enumerate(method.getParameterTypes()):
                vtype = t.toString()
                vname = f"param_{idx}"
                var = value_handlers.fake_method_param_var(vtype, vname)
                method_model.param_vars.append(
                    models.VariableModel(var=var, vartype=str(vtype))
                )

            # Skip further processing since there is no body to analyze
            # write_method_to_filepath(method_model, path)
            class_model.methods.append(method_model)
            mindex = mindex + 1
            continue

        method_body = method.getBody()

        for v in method_body.getLocals():
            var = value_handlers.value_handler(
                value_type=v.getClass().getTypeName(),
                value=v,
            )
            vtype = v.getType().toString()
            method_model.local_vars.append(
                models.VariableModel(var=var, vartype=str(vtype))
            )

        for p in method_body.getParameterLocals():
            var = value_handlers.value_handler(
                value_type=p.getClass().getTypeName(),
                value=p,
            )
            ptype = p.getType().toString()
            method_model.param_vars.append(
                models.VariableModel(var=var, vartype=str(ptype))
            )

        graph = method_body.getStmtGraph()

        # Retrieve the mapping of all basic blocks.
        # Each block is an instance of:
        # <java class 'sootup.core.graph.MutableBasicBlockImpl'>
        blocks = []
        block_successors: dict[int, list[int]] = {}
        block_predecessors: dict[int, list[int]] = {}
        block_stmts: dict[int, list[...]] = {}

        for block in graph.getBlocksSorted():
            blocks.append(block)
            block_index = len(blocks) - 1
            block_successors[block_index] = []
            block_predecessors[block_index] = []
            block_stmts[block_index] = []

        for block_index, block in enumerate(blocks):
            succs: list[...] = block.getSuccessors()
            for succ in succs:
                succ_block_index = blocks.index(succ)
                block_predecessors[succ_block_index].append(block_index)
                block_successors[block_index].append(succ_block_index)

        """
        check of block index 0 has predecessors else something is wrong
        """
        if len(block_predecessors[0]) > 0:
            raise Exception("something is wrong with our blocks")

        for block_index, block in enumerate(blocks):
            for stmt in block.getStmts().toArray():
                block_stmts[block_index].append(stmt)

        for block_index, block in enumerate(blocks):
            for stmt in block_stmts[block_index]:
                stmt_model = stmt_handler(
                    block_index=block_index,
                    stmt_type=stmt.getClass().getSimpleName(),
                    stmt=stmt,
                    block_successors=block_successors,
                    body=method_body,
                    block_stmts=block_stmts,
                )
                stmt_model.block_index = block_index
                method_model.instructions.append(stmt_model)

                if stmt_model.op == models.StmtType.JIDENTITY:
                    new_right_tokens = []
                    local_var_tokens = []
                    breakpoint_vt_index = None

                    """
                    get all tokens before ":" and set it as the new tokens
                    """
                    for vt_idx, vt in enumerate(stmt_model.right.value_tokens):
                        if vt.token_value == ":":
                            breakpoint_vt_index = vt_idx
                            break

                        new_right_tokens.append(vt)

                        if vt.token_value == "@":
                            continue

                        local_var_tokens.append(vt)

                    """
                    get the type information which is after ":", " ", "type"
                    """
                    if breakpoint_vt_index is not None:
                        vtype = stmt_model.right.value_tokens[
                            breakpoint_vt_index + 2
                        ].token_value
                    else:
                        if local_var_tokens[0].token_value == "caughtexception":
                            vtype = "java.lang.Exception"
                        else:
                            pprint(stmt_model.model_dump())
                            print("\n")
                            raise Exception()

                    """
                    set instruction's value_tokens to new values before ":"
                    """
                    stmt_model.right.value_tokens = new_right_tokens

                    """
                    create a new var token to be saved in local_vars
                    """
                    var = models.ValueModel(
                        value_type=stmt_model.right.value_type,
                        value_tokens=local_var_tokens,
                    )
                    method_model.local_vars.append(
                        models.VariableModel(var=var, vartype=vtype)
                    )

        method_model.block_indices = list(block_successors.keys())
        method_model.block_successors = block_successors
        method_model.block_predecessors = block_predecessors

        class_model.methods.append(method_model)
        mindex = mindex + 1
    return class_model


def extract_classes(binary_filepath: str):
    inputLocation: AnalysisInputLocation = JavaClassPathAnalysisInputLocation(
        binary_filepath
    )
    view: View = JavaView(inputLocation)

    java_stream = view.getClasses()
    Collectors = JClass("java.util.stream.Collectors")
    class_list = java_stream.collect(Collectors.toList())

    for jvm_class in class_list:
        class_model = extract_class(jvm_class, binary_filepath)
        yield class_model


def dump_class_jimple(binary_filepath: str, class_name: str, method_name: str):
    inputLocation: AnalysisInputLocation = JavaClassPathAnalysisInputLocation(
        binary_filepath
    )
    view: View = JavaView(inputLocation)

    java_stream = view.getClasses()
    Collectors = JClass("java.util.stream.Collectors")
    class_list = java_stream.collect(Collectors.toList())

    class_found = False
    for jvm_class in class_list:
        if str(jvm_class.getName()) == class_name:
            class_found = True
            for method in jvm_class.getMethods():
                if str(method.getName()) == method_name:
                    if method.hasBody():
                        print(method.getBody())
                    else:
                        print("No Body ...")
                    break
            break

    if class_found is False:
        print(f"No class found for -- {class_name}")
