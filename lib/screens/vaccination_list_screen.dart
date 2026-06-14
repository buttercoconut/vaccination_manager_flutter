import 'package:flutter/material.dart';
import '../widgets/vaccination_card.dart';
import '../services/api_service.dart';
import '../models/vaccination.dart';

class VaccinationListScreen extends StatefulWidget {
  const VaccinationListScreen({Key? key}) : super(key: key);

  @override
  State<VaccinationListScreen> createState() => _VaccinationListScreenState();
}

class _VaccinationListScreenState extends State<VaccinationListScreen> {
  List<Vaccination> _vaccinations = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchVaccinations();
  }

  Future<void> _fetchVaccinations() async {
    final data = await ApiService.getVaccinations();
    setState(() {
      _vaccinations = data;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Vaccination List')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _vaccinations.length,
              itemBuilder: (context, index) {
                return VaccinationCard(vaccination: _vaccinations[index]);
              },
            ),
    );
  }
}
