import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const VaccinationApp());
}

class VaccinationApp extends StatelessWidget {
  const VaccinationApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vaccination Manager',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomeScreen(),
    );
  }
}
