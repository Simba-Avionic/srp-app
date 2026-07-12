import 'package:flutter/material.dart';
import 'package:desktop/services/method_service.dart';
import 'package:desktop/utils/format_utils.dart';

class MethodWidget extends StatefulWidget {
  final String methodName;
  final int methodId;
  final String inType;
  final String namespace;

  const MethodWidget({
    super.key,
    required this.methodName,
    required this.methodId,
    required this.inType,
    required this.namespace,
  });

  @override
  _MethodWidgetState createState() => _MethodWidgetState();
}

class _MethodWidgetState extends State<MethodWidget> {
  String _result = '';
  final TextEditingController _inputController = TextEditingController();

  bool get _isValveMethod => widget.methodName.contains('Valve');

  bool get _isSetModeMethod => widget.methodName == 'SetMode';

  static const _modeOptions = [
    ['DISARM', '1'],
    ['ARM', '2'],
    ['LAUNCH', '3'],
    ['ABORT', '64'],
  ];

  Future<void> _sendRequest([String? input]) async {
    setState(() {
      _result = 'Sending...';
    });

    try {
      final data = await MethodService.sendRequest(
        namespace: widget.namespace,
        methodName: widget.methodName,
        inType: widget.inType,
        input: input ?? _inputController.text,
      );

      setState(() {
        _result = formatDisplayValue(data['result']);
      });
    } catch (e) {
      setState(() {
        _result = 'Error';
      });
    }
  }

  ButtonStyle _actionButtonStyle(BuildContext context) {
    return TextButton.styleFrom(
      padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
      backgroundColor: Theme.of(context).colorScheme.secondary,
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20.0),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8.0),
        boxShadow: const [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 2.0,
            offset: Offset(0, 1),
          ),
        ],
      ),
      padding: const EdgeInsets.all(10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            widget.methodName,
            style: const TextStyle(
              color: Colors.black87,
              fontSize: 13,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          if (_isValveMethod && widget.inType != "void")
            Row(
              children: [
                TextButton(
                  onPressed: () => _sendRequest('1'),
                  style: _actionButtonStyle(context),
                  child: const Text("OPEN (1)", style: TextStyle(fontSize: 12)),
                ),
                const SizedBox(width: 8),
                TextButton(
                  onPressed: () => _sendRequest('0'),
                  style: _actionButtonStyle(context),
                  child: const Text("CLOSE (0)", style: TextStyle(fontSize: 12)),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _result,
                    style: const TextStyle(fontSize: 12, color: Colors.black54),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            )
          else if (_isSetModeMethod && widget.inType != "void") ...[
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final mode in _modeOptions)
                  TextButton(
                    onPressed: () => _sendRequest(mode[1]),
                    style: _actionButtonStyle(context),
                    child: Text(
                      "${mode[0]} (${mode[1]})",
                      style: const TextStyle(fontSize: 12),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              _result,
              style: const TextStyle(fontSize: 12, color: Colors.black54),
            ),
          ]
          else ...[
            if (widget.inType != "void")
              SizedBox(
                height: 34,
                child: TextField(
                  controller: _inputController,
                  style: const TextStyle(color: Colors.black, fontSize: 13),
                  decoration: InputDecoration(
                    hintText: widget.inType,
                    hintStyle: const TextStyle(color: Colors.grey, fontSize: 12),
                    isDense: true,
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 12.0,
                      vertical: 8.0,
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(20.0),
                      borderSide: const BorderSide(color: Colors.black26),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(20.0),
                      borderSide: const BorderSide(color: Colors.black26),
                    ),
                  ),
                ),
              ),
            const SizedBox(height: 8),
            Row(
              children: [
                TextButton(
                  onPressed: () => _sendRequest(),
                  style: _actionButtonStyle(context),
                  child: const Text("SEND", style: TextStyle(fontSize: 12)),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _result,
                    style: const TextStyle(fontSize: 12, color: Colors.black54),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }
}
