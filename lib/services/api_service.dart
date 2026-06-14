import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/vaccination.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';

  static Future<List<Vaccination>> getVaccinations() async {
    final response = await http.get(Uri.parse('$baseUrl/vaccinations'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((e) => Vaccination.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load vaccinations');
    }
  }
}
