double? parseNumericValue(dynamic value) {
  if (value == null) {
    return null;
  }

  if (value is num) {
    return value.toDouble();
  }

  final str = value.toString().trim();
  if (str.isEmpty) {
    return null;
  }

  return double.tryParse(str);
}

String formatDisplayValue(dynamic value) {
  if (value == null) {
    return '-';
  }

  if (value is int) {
    return value.toString();
  }

  if (value is double) {
    return _formatFloatingPoint(value);
  }

  if (value is num) {
    return _formatFloatingPoint(value.toDouble());
  }

  final str = value.toString().trim();
  if (str.isEmpty) {
    return str;
  }

  final parsed = double.tryParse(str);
  if (parsed != null && _looksLikeFloatingPoint(str, parsed)) {
    return _formatFloatingPoint(parsed);
  }

  return str;
}

bool _looksLikeFloatingPoint(String raw, double parsed) {
  if (raw.contains('.') || raw.toLowerCase().contains('e')) {
    return true;
  }
  return parsed % 1 != 0;
}

String _formatFloatingPoint(double value) {
  if (value % 1 == 0) {
    return value.toInt().toString();
  }
  return value.toStringAsFixed(2);
}
