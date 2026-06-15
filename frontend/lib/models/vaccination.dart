class Vaccination {
  final int id;
  final String vaccineName;
  final DateTime date;

  Vaccination({required this.id, required this.vaccineName, required this.date});

  factory Vaccination.fromJson(Map<String, dynamic> json) {
    return Vaccination(
      id: json['id'],
      vaccineName: json['vaccine_name'],
      date: DateTime.parse(json['date']),
    );
  }
}
