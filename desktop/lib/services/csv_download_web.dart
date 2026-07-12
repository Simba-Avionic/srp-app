// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

import 'package:desktop/services/base.dart';

void downloadCsvFile() {
  final anchor = html.AnchorElement(href: apiUrl('/save/download'))
    ..download = 'data.csv'
    ..target = '_blank';
  html.document.body?.append(anchor);
  anchor.click();
  anchor.remove();
}
