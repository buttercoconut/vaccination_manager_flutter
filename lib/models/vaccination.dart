class Vaccination {
  final int id;
  final String vaccineName;
  final DateTime date;
  final List<String> sideEffects;

  Vaccination({
    required this.id,
    required this.vaccineName,
    required this.date,
    required this.sideEffects,
  });

  factory Vaccination.fromJson(Map<String, dynamic> json) {
    return Vaccination(
      id: json['id'],
      vaccineName: json['vaccine_name'],
      date: DateTime.parse(json['date']),
      sideEffects: List<String>.from(json['side_effects'] ?? []),
    );
  }
}
