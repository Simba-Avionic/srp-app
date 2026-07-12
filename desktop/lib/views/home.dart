import 'package:flutter/material.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import 'package:desktop/data/services_config.dart';
import '../widgets/service_widget.dart';

class Home extends StatelessWidget {
  final bool readOnly;

  const Home({
    super.key,
    this.readOnly = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      color: Colors.white,
      padding: const EdgeInsets.all(16),
      child: MasonryGridView.count(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisCount: 3,
        mainAxisSpacing: 12,
        crossAxisSpacing: 12,
        itemCount: serviceDefinitions.length,
        itemBuilder: (context, index) {
          final service = serviceDefinitions[index];
          return ServiceWidget(
            serviceName: service['serviceName'],
            serviceId: service['serviceId'],
            readOnly: readOnly,
            events: service['events'] != null
                ? List<Map<String, dynamic>>.from(service['events'])
                : null,
            methods: service['methods'] != null
                ? List<Map<String, dynamic>>.from(service['methods'])
                : null,
          );
        },
      ),
    );
  }
}
