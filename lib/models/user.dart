class User {
  final int id;
  final String name;
  final DateTime birthDate;
  final String phone;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.birthDate,
    required this.phone,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      birthDate: DateTime.parse(json['birth_date']),
      phone: json['phone'],
      email: json['email'],
    );
  }
}
