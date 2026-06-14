import 'package:flutter/material.dart';
import '../models/vaccination.dart';

class VaccinationCard extends StatelessWidget {
  final Vaccination vaccination;

  const VaccinationCard({Key? key, required this.vaccination}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        title: Text(vaccination.vaccineName),
        subtitle: Text('Date: ${vaccination.date.toLocal()}'),
        trailing: vaccination.sideEffects.isNotEmpty
            ? const Icon(Icons.warning, color: Colors.red)
            : const Icon(Icons.check, color: Colors.green),
      ),
    );
  }
}
