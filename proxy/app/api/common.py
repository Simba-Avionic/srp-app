from flask import jsonify
from someipy import MessageType, ReturnCode

def process_method_result(method_result, deserialization_class=None):
    try:
        if method_result.message_type == MessageType.RESPONSE:
            print(
                f"Received result for method: {' '.join(f'0x{b:02x}' for b in method_result.payload)}"
            )
            if method_result.return_code == ReturnCode.E_OK:
                if deserialization_class:
                    deserialized_data = deserialization_class().deserialize(method_result.payload)
                    result_value = getattr(deserialized_data.data, 'value', deserialized_data)
                else:
                    result_value = method_result.payload
                print(f"result: {result_value}")
                return jsonify({"result": result_value}), 200
            else:
                print(
                    f"Method call returned an error: {method_result.return_code}"
                )
                return jsonify({"error": "Error in method call", "code": method_result.return_code.name}), 400
        elif method_result.message_type == MessageType.ERROR:
            print("Server returned an error.")
            return jsonify({"error": "Server error occurred"}), 500
    except Exception as e:
        print(f"Error processing method result: {e}")
        return jsonify({"error": str(e)}), 500
