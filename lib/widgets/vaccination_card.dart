import 'package:flutter/material.dart';
import '../models/vaccination.dart';

class VaccinationCard extends StatelessWidget {
  final Vaccination vaccination;

  const VaccinationCard({Key? key, required this.vaccination}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: ListTile(
        leading: const Icon(Icons.medical_services, color: Colors.blue),
        title: Text(vaccination.vaccineName),
        subtitle: Text('Date: ${vaccination.date.toLocal().toShortDateString()}\nSide Effects: ${vaccination.sideEffects ?? 'None'}'),
        trailing: IconButton(
          icon: const Icon(Icons.edit),
          onPressed: () {
            // TODO: navigate to edit screen
          },
        ),
      ),
    );
  }
}

extension DateTimeExtension on DateTime {
  String toShortDateString() {
    return '${this.year}-${this.month.toString().padLeft(2, '0')}-${this.day.toString().padLeft(2, '0')}';
  }
}
