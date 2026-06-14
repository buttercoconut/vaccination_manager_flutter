import 'package:flutter/material.dart';
import 'vaccination_list_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Vaccination Manager')),
      body: const Center(
        child: Text('Welcome to Vaccination Manager'),
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.list),
        onPressed: () {
          Navigator.of(context).push(
            MaterialPageRoute(builder: (_) => const VaccinationListScreen()),
          );
        },
      ),
    );
  }
}
