"""
Model classes for Flutter.
"""
class Vaccination {
  final int id;
  final int userId;
  final Vaccine vaccine;
  final DateTime date;

  Vaccination({required this.id, required this.userId, required this.vaccine, required this.date});
}

class Vaccine {
  final int id;
  final String name;
  final String manufacturer;
  final String efficacy;

  Vaccine({required this.id, required this.name, required this.manufacturer, required this.efficacy});
}
