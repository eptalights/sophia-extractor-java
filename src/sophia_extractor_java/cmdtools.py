import argparse
import logging
import os
import json
from ._api import extract_classes, dump_class_jimple


logging.basicConfig(
    level=logging.DEBUG, format="%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
_LOG = logging.getLogger(__name__)


def write_function_to_file(store_path, class_dump):
    current_dir = os.path.dirname(os.path.abspath(store_path))

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    with open(store_path, "w") as json_file:
        json.dump(class_dump, json_file, indent=2)


def extractor():
    parser = argparse.ArgumentParser(description="extract JAR/classes-dir into JSON")
    parser.add_argument("-b", "--binary-path", required=True)
    parser.add_argument(
        "-e", "--extract-path", required=False, default="./sophia_jimple_output"
    )
    args = parser.parse_args()

    for class_model in extract_classes(args.binary_path):
        store_path = f"{args.extract_path}/{class_model.class_source}.json"
        store_path = store_path.replace("$", "__")

        _LOG.info(f"Storing - {store_path} ...")
        write_function_to_file(store_path, class_model.model_dump())


def jimple_dump():
    parser = argparse.ArgumentParser(description="Dump class method Jimple")
    parser.add_argument("-b", "--binary-path", required=True)
    parser.add_argument("-c", "--class-name", required=True)
    parser.add_argument("-m", "--method-name", required=True)

    args = parser.parse_args()
    dump_class_jimple(args.binary_path, args.class_name, args.method_name)


if __name__ == "__main__":
    extractor()
