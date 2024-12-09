import json
from typing import Dict, Any, Set


def parse_type(data_type: str) -> str:
    type_mapping = {
        "void": "bytes",
        "bool": "Bool",
        "uint8": "Uint8",
        "uint16": "Uint16",
        "uint32": "Uint32",
        "uint64": "Uint64",
        "int8": "Sint8",
        "int16": "Sint16",
        "int32": "Sint32",
        "int64": "Sint64",
        "float32": "Float32",
        "float64": "Float64"
    }
    return type_mapping.get(data_type, "UnknownType")


def collect_required_types(json_data: Dict[str, Any]) -> Set[str]:
    required_types = set()
    someip = json_data.get("someip", {})

    for service_data in someip.values():
        for method_data in service_data.get("methods", {}).values():
            data_structure = method_data.get("data_structure", {})
            if "in" in data_structure:
                required_types.add(parse_type(data_structure["in"]["type"]))
            if "out" in data_structure:
                required_types.add(parse_type(data_structure["out"]["type"]))

        for event_data in service_data.get("events", {}).values():
            data_structure = event_data.get("data_structure", {})
            if "in" in data_structure:
                required_types.add(parse_type(data_structure["in"]["type"]))
            if "out" in data_structure:
                required_types.add(parse_type(data_structure["out"]["type"]))

    required_types.discard("UnknownType")
    return required_types


def generate_class(name: str, data_structure: Dict[str, Any]) -> str:
    in_data = data_structure.get("in")
    out_data = data_structure.get("out")

    in_type = parse_type(in_data["type"]) if in_data else "bytes"
    out_type = parse_type(out_data["type"]) if out_data else "bytes"

    class_definitions = []

    if in_type:
        in_class = [
            "@dataclass",
            f"class {name}In(SomeIpPayload):",
            f"    data: {in_type}",
            "",
            f"    def __init__(self):",
            f"        self.data = b''" if in_type == "bytes" else f"        self.data = {in_type}()",
            "",
        ]
        class_definitions.append("\n".join(in_class))

    if out_type:
        out_class = [
            "@dataclass",
            f"class {name}Out(SomeIpPayload):",
            f"    data: {out_type}",
            "",
            f"    def __init__(self):",
            f"        self.data = b''" if out_type == "bytes" else f"        self.data = {out_type}()",
            "",
        ]
        class_definitions.append("\n".join(out_class))


    return "\n\n".join(class_definitions)



def generate_code(json_data: Dict[str, Any]) -> str:
    required_types = collect_required_types(json_data)
    imports = [
        "from dataclasses import dataclass",
        "from someipy.serialization import (",
        "    SomeIpPayload,"
    ]

    for t in sorted(required_types):
        if t != "bytes":
            imports.append(f"    {t},")

    if len(imports) > 2:
        imports[-1] = imports[-1][:-1]
        imports.append(")")

    imports_output = "\n".join(imports)

    output = [imports_output]

    someip = json_data.get("someip", {})
    name = next(iter(someip))
    for service_name, service_data in someip.items():
        methods = service_data.get("methods", {})
        events = service_data.get("events", {})

        for method_name, method_data in methods.items():
            class_code = generate_class(method_name, method_data["data_structure"])
            output.append(class_code)

        for event_name, event_data in events.items():
            class_code = generate_class(event_name, event_data["data_structure"])
            output.append(class_code)

    return "\n\n\n".join(output), name


def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)


def save_code(file_path: str, code: str):
    with open(file_path, "w") as file:
        file.write(code)


json_input = load_json("sample_input/env_service.json")
generated_code, name = generate_code(json_input)

save_code(f"custom_dataclasses/{name.lower()}_dataclass.py", generated_code)
