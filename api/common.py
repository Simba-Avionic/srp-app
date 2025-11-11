from fastapi.responses import JSONResponse
from fastapi import status
from someipy import MessageType, ReturnCode
from typing import Optional, Type
from loguru import logger


def process_method_result(method_result, deserialization_class: Optional[Type] = None):
    try:
        if method_result.message_type == MessageType.RESPONSE:
            logger.debug("Received result for method: %s",
                         ' '.join(f'0x{b:02x}' for b in method_result.payload))

            if method_result.return_code == ReturnCode.E_OK:
                result_value = method_result.payload  # Default value

                if deserialization_class:
                    deserialized_data = deserialization_class().deserialize(method_result.payload)
                    result_value = getattr(deserialized_data.data, 'value', deserialized_data)
                    logger.debug("Deserialization completed; result is back")

                logger.info("Method result: %s", result_value)
                return {
                    "result": result_value
                }

            else:
                logger.warning("Method call returned an error: %s", method_result.return_code)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "Error in method call",
                        "code": method_result.return_code.name
                    }
                )

        elif method_result.message_type == MessageType.ERROR:
            logger.error("Server returned an error.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Server error occurred"}
            )

    except Exception as e:
        logger.exception("Error processing method result: %s", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )