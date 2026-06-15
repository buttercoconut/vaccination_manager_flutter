import 'package:flutter/material.dart';
import '../widgets/vaccination_card.dart';
import '../models/vaccination.dart';

class VaccinationListScreen extends StatelessWidget {
  final List<Vaccination> vaccinations;

  const VaccinationListScreen({Key? key, required this.vaccinations}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vaccination History'),
      ),
      body: ListView.builder(
        itemCount: vaccinations.length,
        itemBuilder: (context, index) {
          return VaccinationCard(vaccination: vaccinations[index]);
        },
      ),
    );
  }
}
