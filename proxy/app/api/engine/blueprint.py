from flask import Blueprint, jsonify, request

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
    data = request.json or {}
    try:
        service_manager = EngineServiceManager()
        result = await service_manager.Start(start=data["start"])
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

