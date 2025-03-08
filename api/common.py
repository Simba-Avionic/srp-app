from fastapi.responses import JSONResponse
from fastapi import status
from someipy import MessageType, ReturnCode
from typing import Optional, Type


def process_method_result(method_result, deserialization_class: Optional[Type] = None):
    try:
        if method_result.message_type == MessageType.RESPONSE:
            print(
                f"Received result for method: {' '.join(f'0x{b:02x}' for b in method_result.payload)}"
            )

            if method_result.return_code == ReturnCode.E_OK:
                result_value = method_result.payload  # Default value

                if deserialization_class:
                    deserialized_data = deserialization_class().deserialize(method_result.payload)
                    result_value = getattr(deserialized_data.data, 'value', deserialized_data)
                    print("result is back")

                print(f"result: {result_value}")
                return {
                    "result": result_value
                }

            else:
                print(f"Method call returned an error: {method_result.return_code}")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "Error in method call",
                        "code": method_result.return_code.name
                    }
                )

        elif method_result.message_type == MessageType.ERROR:
            print("Server returned an error.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Server error occurred"}
            )

    except Exception as e:
        print(f"Error processing method result: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )