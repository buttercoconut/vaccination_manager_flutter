import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const VaccinationManagerApp());
}

class VaccinationManagerApp extends StatelessWidget {
  const VaccinationManagerApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vaccination Manager',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
    );
  }
}
