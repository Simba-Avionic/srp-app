import json
from pathlib import Path
from typing import Dict, Any, Set, List

STRUCT_REGISTRY: Dict[str, Dict[str, str]] = {}
BASE_OUTPUT_DIR = (Path(__file__).resolve().parent / "../../proxy/app/dataclasses").resolve()

# Mapping for byte size calculations
TYPE_SIZES = {
    "Bool": 1, "Uint8": 1, "Sint8": 1,
    "Uint16": 2, "Sint16": 2,
    "Uint32": 4, "Sint32": 4, "Float32": 4,
    "Uint64": 8, "Sint64": 8, "Float64": 8,
    "bytes": 0 # Special case, usually dynamic
}

def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r") as f:
        return json.load(f)

def find_structs(file_path: Path):
    data = load_json(file_path)
    structures = data.get("data_structure", {})
    for struct_name, fields in structures.items():
        STRUCT_REGISTRY[struct_name] = fields

def parse_type(data_type: str) -> str:
    type_mapping = {
        "void": "bytes", "bool": "Bool", "uint8": "Uint8", "uint16": "Uint16",
        "uint32": "Uint32", "uint64": "Uint64", "int8": "Sint8", "int16": "Sint16",
        "int32": "Sint32", "int64": "Sint64", "float32": "Float32", "float64": "Float64",
    }
    clean_type = data_type.split(".")[-1]
    if clean_type in STRUCT_REGISTRY:
        return clean_type
    return type_mapping.get(clean_type, "UnknownType")

def get_cast_function_name(data_type: str) -> str:
    cast_map = {
        "Bool": "bool", "Float32": "float", "Float64": "float",
        "Uint8": "int", "Uint16": "int", "Uint32": "int", "Uint64": "int",
        "Sint8": "int", "Sint16": "int", "Sint32": "int", "Sint64": "int",
    }
    return cast_map.get(data_type, "str")

def get_type_size(type_name: str) -> int:
    """Recursively calculates the size in bytes for a given type."""
    if type_name in TYPE_SIZES:
        return TYPE_SIZES[type_name]
    
    if type_name in STRUCT_REGISTRY:
        total_size = 0
        for field_type in STRUCT_REGISTRY[type_name].values():
            ptype = parse_type(field_type)
            total_size += get_type_size(ptype)
        return total_size
    
    return 0  # Fallback

def generate_class_definition(name: str, fields: Dict[str, str], is_struct: bool = False) -> str:
    name = name[0].upper() + name[1:]
    lines = ["@dataclass", f"class {name}:" if is_struct else f"class {name}(SomeIpPayload):"]
    
    # --- Fields and __init__ ---
    if not fields and not is_struct:
        lines.append("    data: bytes = b''")
    else:
        for field, f_type in fields.items():
            ptype = parse_type(f_type)
            if not is_struct:
                lines.append(f"    data: {ptype}")
                lines.append(f"    def __init__(self):")
                lines.append(f"        self.data = {ptype}()")
            else:
                lines.append(f"    {field}: {ptype}")

    lines.append("")
    
    if is_struct and fields:
        lines.append("    def __init__(self):")
        for field, f_type in fields.items():
            ptype = parse_type(f_type)
            lines.append(f"        self.{field} = {ptype}()")
        lines.append("")

    # --- from_json ---
    if fields or is_struct:
        arg_name = "json_obj" if is_struct else "json_argument"
        lines.append(f"    def from_json(self, {arg_name}):")
        
        target_items = fields.items() if is_struct else [("data", fields["type"])]
        
        for field, f_type in target_items:
            ptype = parse_type(f_type)
            target = f"self.{field}"
            
            if ptype in STRUCT_REGISTRY:
                lines.append(f"        {target}.from_json({arg_name}['{field}'])" if is_struct else f"        {target}.from_json({arg_name})")
            else:
                cast = get_cast_function_name(ptype)
                source = f"{arg_name}['{field}']" if is_struct else arg_name
                lines.append(f"        {target}.value = {cast}({source})")
        lines.append("")

    # --- deserialize (Only for Structs or Wrappers containing Structs) ---
    has_struct_field = False
    if not is_struct and fields:
        # Check if the wrapper contains a struct
        ptype = parse_type(fields["type"])
        if ptype in STRUCT_REGISTRY:
            has_struct_field = True
            lines.append("    def deserialize(self, payload: bytes):")
            lines.append("        self.data.deserialize(payload)")
            lines.append("        return self")

    if is_struct:
        lines.append("    def deserialize(self, payload: bytes):")
        current_offset = 0
        for field, f_type in fields.items():
            ptype = parse_type(f_type)
            size = get_type_size(ptype)
            
            end_offset = current_offset + size
            lines.append(f"        self.{field}.deserialize(payload[{current_offset}:{end_offset}])")
            current_offset = end_offset

    return "\n".join(lines)

def generate_structs_file():
    if not STRUCT_REGISTRY:
        return

    used_types = set()
    classes = []

    # Two-pass to ensure used primitives are imported
    for name, fields in STRUCT_REGISTRY.items():
        for f_type in fields.values():
            ptype = parse_type(f_type)
            if ptype not in STRUCT_REGISTRY and ptype != "bytes":
                used_types.add(ptype)
        classes.append(generate_class_definition(name, fields, is_struct=True))

    imports = ["from dataclasses import dataclass", "from someipy.serialization import ("]
    imports.extend([f"    {t}," for t in sorted(used_types)])
    imports.append(")")

    content = "\n".join(imports) + "\n\n" + "\n\n".join(classes)
    
    output_path = BASE_OUTPUT_DIR / "structs.py"
    output_path.write_text(content)
    print(f"Generated: {output_path}")

def generate_service_dataclass_code(json_data: Dict[str, Any]) -> str:
    someip = json_data.get("someip", {})
    service_name = next(iter(someip))
    
    required_primitives = set()
    required_structs = set()
    classes = []

    for service in someip.values():
        for block in ("methods", "events"):
            for name, entry in service.get(block, {}).items():
                ds = entry.get("data_structure", {})
                for direction in ("in", "out"):
                    if direction in ds:
                        raw_type = ds[direction]["type"]
                        ptype = parse_type(raw_type)
                        
                        if ptype in STRUCT_REGISTRY:
                            required_structs.add(ptype)
                        elif ptype != "bytes":
                            required_primitives.add(ptype)
                            
                        class_name = f"{name}{direction.capitalize()}"
                        fields_mock = {"type": raw_type} if ptype != "bytes" else {}
                        classes.append(generate_class_definition(class_name, fields_mock, is_struct=False))

    import_groups = ["from dataclasses import dataclass"]
    
    someipy_lines = ["from someipy.serialization import (", "    SomeIpPayload,"]
    someipy_lines.extend([f"    {t}," for t in sorted(required_primitives)])
    someipy_lines.append(")")
    import_groups.append("\n".join(someipy_lines))
    
    if required_structs:
        struct_lines = ["from .structs import ("]
        struct_lines.extend([f"    {s}," for s in sorted(required_structs)])
        struct_lines.append(")")
        import_groups.append("\n".join(struct_lines))

    full_imports = "\n".join(import_groups)
    
    return f"{full_imports}\n\n" + "\n\n".join(classes), service_name

def process_directory(directory_path: Path):
    BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Scanning for structs...")
    for file in directory_path.rglob("*data_type.json"):
        find_structs(file)

    generate_structs_file()

    print("Generating service dataclass files...")
    for file in directory_path.rglob("*.json"):
        if file.name.endswith("data_type.json"):
            continue

        data = load_json(file)
        code, name = generate_service_dataclass_code(data)

        output_path = BASE_OUTPUT_DIR / f"{name.lower()}_dataclass.py"
        output_path.write_text(code)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    # Adjust path as necessary
    process_directory(Path("/home/krzysztof/rocket_test/app/system_definition/someip"))