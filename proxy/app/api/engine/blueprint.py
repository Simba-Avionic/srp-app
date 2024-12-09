
from flask import Blueprint, jsonify, request
from someipy import MessageType, ReturnCode

from proxy.app.parser.custom_dataclasses.engineservice_dataclass import StartOut

engine_bp = Blueprint('engine', __name__)

from proxy.app.parser.services.engineservice import EngineServiceManager


@engine_bp.route('/SetMode', methods=['POST'])
async def SetMode():
    data = request.json or {}
    try:
        service_manager = EngineServiceManager()
        result = await service_manager.SetMode(data["setmode"])
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@engine_bp.route('/Start', methods=['POST'])
async def Start():
    global start
    try:
        service_manager = EngineServiceManager()
        method_result = await service_manager.Start()
        if method_result.message_type == MessageType.RESPONSE:
            print(
                f"Received result for method: {' '.join(f'0x{b:02x}' for b in method_result.payload)}"
            )
            if method_result.return_code == ReturnCode.E_OK:
                start = StartOut().deserialize(method_result.payload)
                print(f"result: {start.data.value}")
            else:
                print(
                    f"Method call returned an error: {method_result.return_code}"
                )
        elif method_result.message_type == MessageType.ERROR:
            print("Server returned an error..")
        return jsonify({"result": start.data.value}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
