import 'dart:convert';
import 'dart:io';

void main() async {
  String filePath = 'engine_service.json';

  File file = File(filePath);
  String jsonData = await file.readAsString();

  var jsonMap = jsonDecode(jsonData);

  var serviceName = jsonMap['someip'].keys.first;
  var service = jsonMap['someip'][serviceName];
  var serviceId = service['service_id'];
  var methods = service['methods'];
  var events = service['events'];

  Map<String, dynamic> serviceData = {
    "serviceName": serviceName,
    "serviceId": serviceId,
  };

  if (methods.isNotEmpty) {
    serviceData["methods"] = methods.entries.map((entry) {
      return {
        "name": entry.key,
        "id": entry.value['id'],
        "in_type": entry.value['data_structure']['in']['type'],
      };
    }).toList();
  }

  if (events.isNotEmpty) {
    serviceData["events"] = events.entries.map((entry) {
      return {
        "name": entry.key,
        "id": entry.value['id'],
      };
    }).toList();
  }
  var encoder = const JsonEncoder.withIndent('  ');
  String prettyJson = encoder.convert(serviceData);

  String serviceDataString = 'final Map<String, dynamic> $serviceName = $prettyJson;';

  print(serviceDataString);
}
