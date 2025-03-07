import 'package:flutter/material.dart';
import 'package:desktop/services/method_service.dart';

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

  Future<void> _sendRequest() async {
    setState(() {
      _result = 'Sending...';
    });

    try {
      final data = await MethodService.sendRequest(
        namespace: widget.namespace,
        methodName: widget.methodName,
        inType: widget.inType,
        input: _inputController.text,
      );

      setState(() {
        _result = 'Result: ${data['result']}';
      });
    } catch (e) {
      setState(() {
        _result = 'Request failed: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(12.0),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8.0),
          boxShadow: const [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 4.0,
              offset: Offset(0, 2),
            ),
          ],
        ),
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.code, color: Colors.black54),
                const SizedBox(width: 8),
                RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(
                        text: "${widget.methodName}\n",
                        style: const TextStyle(
                          color: Colors.black87,
                          fontSize: 20,
                        ),
                      ),
                      TextSpan(
                        text: "Method ID: ${widget.methodId}",
                        style: const TextStyle(
                          color: Colors.black87,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            if (widget.inType != "void") ...[
              Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Text(
                    "Input: ",
                    style: TextStyle(
                      color: Colors.black87,
                      fontSize: 16,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextField(
                      controller: _inputController,
                      style: const TextStyle(color: Colors.black),
                      decoration: InputDecoration(
                        hintText: widget.inType,
                        hintStyle: const TextStyle(color: Colors.grey),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16.0,
                          vertical: 12.0,
                        ),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30.0),
                          borderSide: const BorderSide(color: Colors.black),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30.0),
                          borderSide:
                          const BorderSide(color: Colors.black, width: 1.0),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30.0),
                          borderSide:
                          const BorderSide(color: Colors.blue, width: 2.0),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
            ],
            Row(
              children: [
                TextButton(
                  onPressed: _sendRequest,
                  style: TextButton.styleFrom(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16.0,
                      vertical: 12.0,
                    ),
                    backgroundColor: Theme.of(context).colorScheme.secondary,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(45.0),
                    ),
                  ),
                  child: const Text(
                    "SEND",
                    style: TextStyle(fontSize: 16.0),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Text(
                    _result,
                    style: const TextStyle(
                      fontSize: 16.0,
                      color: Colors.black87,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
