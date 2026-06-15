import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl = 'http://localhost:8000/api';

  static Future<List> getVaccinations() async {
    final response = await http.get(Uri.parse('$_baseUrl/vaccinations'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body) as List;
    } else {
      throw Exception('Failed to load vaccinations');
    }
  }
}
