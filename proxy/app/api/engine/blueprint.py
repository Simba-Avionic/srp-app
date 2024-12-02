
from flask import Blueprint, jsonify, request
import asyncio

engine_bp = Blueprint('engine', __name__)
from proxy.app.parser.services.engineservice import EngineServiceManager as manager


@engine_bp.route('/SetMode', methods=['POST'])
def SetMode():
    data = request.json or {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(manager.SetMode(**data))
    return jsonify({"result": result})

@engine_bp.route('/Start', methods=['POST'])
def Start():
    data = request.json or {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(manager.Start(**data))
    return jsonify({"result": result})

