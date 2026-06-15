class Vaccination {
  final int id;
  final int userId;
  final int vaccineId;
  final DateTime date;
  final String? sideEffects;
  final String vaccineName; // for display

  Vaccination({
    required this.id,
    required this.userId,
    required this.vaccineId,
    required this.date,
    this.sideEffects,
    required this.vaccineName,
  });

  factory Vaccination.fromJson(Map<String, dynamic> json) {
    return Vaccination(
      id: json['id'],
      userId: json['user_id'],
      vaccineId: json['vaccine_id'],
      date: DateTime.parse(json['date']),
      sideEffects: json['side_effects'],
      vaccineName: json['vaccine_name'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'vaccine_id': vaccineId,
      'date': date.toIso8601String(),
      'side_effects': sideEffects,
      'vaccine_name': vaccineName,
    };
  }
}
