import 'dart:convert';
import 'dart:io';

String processServiceFile(File file) {
  String jsonData = file.readAsStringSync();
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

  if (methods != null && (methods as Map).isNotEmpty) {
    serviceData["methods"] = methods.entries.map((entry) {
      return {
        "name": entry.key,
        "id": entry.value['id'],
        "in_type": entry.value['data_structure']['in']['type'],
      };
    }).toList();
  }

  if (events != null && (events as Map).isNotEmpty) {
    serviceData["events"] = events.entries.map((entry) {
      return {
        "name": entry.key,
        "id": entry.value['id'],
      };
    }).toList();
  }

  var encoder = const JsonEncoder.withIndent('  ');
  String prettyJson = encoder.convert(serviceData);

  return 'final Map<String, dynamic> $serviceName = $prettyJson;';
}

void main() async {
  String someipDir = '/home/krzysztof/rocket_test/app/system_definition/someip';

  List<File> serviceFiles = Directory(someipDir)
      .listSync(recursive: true)
      .whereType<File>()
      .where((f) => f.path.endsWith('service.json'))
      .toList()
    ..sort((a, b) => a.path.compareTo(b.path));

  for (File file in serviceFiles) {
    try {
      String output = processServiceFile(file);
      print(output);
      print('');
    } catch (e) {
      stderr.writeln('Error processing ${file.path}: $e');
    }
  }
}
