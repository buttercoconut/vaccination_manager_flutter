import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/vaccination.dart';

class ApiService {
  static const String _baseUrl = 'http://localhost:8000/api';

  static Future<List<Vaccination>> getVaccinations() async {
    final response = await http.get(Uri.parse('$_baseUrl/vaccinations'));
    if (response.statusCode == 200) {
      final List<dynamic> jsonData = jsonDecode(response.body);
      return jsonData.map((e) => Vaccination.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load vaccinations');
    }
  }
}
