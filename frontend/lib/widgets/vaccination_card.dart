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
        leading: const Icon(Icons.medical_services),
        title: Text(vaccination.vaccineName),
        subtitle: Text('Date: ${vaccination.date.toLocal().toShortDateString()}'),
        trailing: IconButton(
          icon: const Icon(Icons.edit),
          onPressed: () {
            // Edit action (not implemented)
          },
        ),
      ),
    );
  }
}
