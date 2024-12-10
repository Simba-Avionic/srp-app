
import sys
import os

from flask import Blueprint, jsonify, request
from proxy.app.parser.custom_dataclasses.engineservice_dataclass import SetModeOut
from proxy.app.parser.custom_dataclasses.engineservice_dataclass import StartOut

engine_bp = Blueprint('engine', __name__)

from proxy.app.parser.services.engineservice import EngineServiceManager

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api"))
sys.path.append(base_path)
from common import process_method_result


@engine_bp.route('/setmode', methods=['POST'])
async def setmode():
    try:
        data = request.get_json()
        service_manager = EngineServiceManager()
        params = data if data else {}  
        method_result = await service_manager.SetMode(**params)
        return process_method_result(method_result, deserialization_class=SetModeOut)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@engine_bp.route('/start', methods=['POST'])
async def start():
    try:
        data = request.get_json()
        service_manager = EngineServiceManager()
        params = data if data else {}  
        method_result = await service_manager.Start(**params)
        return process_method_result(method_result, deserialization_class=StartOut)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

