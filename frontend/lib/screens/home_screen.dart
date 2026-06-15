import 'package:flutter/material.dart';
import '../widgets/vaccination_card.dart';
import '../services/api_service.dart';
import '../models/vaccination.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Vaccination> _vaccinations = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchVaccinations();
  }

  Future<void> _fetchVaccinations() async {
    try {
      final data = await ApiService.getVaccinations();
      setState(() {
        _vaccinations = data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vaccination Manager'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text('Error: $_error'))
              : ListView.builder(
                  itemCount: _vaccinations.length,
                  itemBuilder: (context, index) {
                    return VaccinationCard(
                      vaccination: _vaccinations[index],
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navigate to add screen (not implemented yet)
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
