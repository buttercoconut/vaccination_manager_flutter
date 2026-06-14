"""
Screen to display list of vaccinations.
"""
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../services/api_service.dart';
import '../models/vaccination.dart';

class VaccinationListScreen extends StatefulWidget {
  const VaccinationListScreen({Key? key}) : super(key: key);

  @override
  _VaccinationListScreenState createState() => _VaccinationListScreenState();
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
    final apiService = Provider.of<ApiService>(context, listen: false);
    final list = await apiService.getVaccinations();
    setState(() {
      _vaccinations = list;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Vaccination History')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _vaccinations.length,
              itemBuilder: (context, index) {
                final v = _vaccinations[index];
                return ListTile(
                  title: Text(v.vaccine.name),
                  subtitle: Text('Date: ${v.date}'),
                );
              },
            ),
    );
  }
}
