class MovingAverage {
  final int windowSize;
  final List<double> _values = [];

  MovingAverage(this.windowSize);

  double add(double value) {
    _values.add(value);
    if (_values.length > windowSize) {
      _values.removeAt(0);
    }
    return _values.reduce((a, b) => a + b) / _values.length;
  }
}
