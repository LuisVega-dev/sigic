// ignore_for_file: avoid_unnecessary_containers

import 'package:flutter/material.dart';

class PosiblesLogos extends StatelessWidget {
  const PosiblesLogos({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 32, 32, 32),
      appBar: AppBar(
        title: const Text(
          'Posibles Logos',
          style: TextStyle(
            color: Colors.white,
            fontFamily: 'Roboto',
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: const Color.fromARGB(255, 32, 32, 32),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Container(
        child: ListView(
          children: [
            Center(
              child: Text(
                'Posible logo 1',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Center(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(15),
                child: Image.asset(
                  'assets/images/logo1.png',
                  width: 250,
                  height: 250,
                ),
              ),
            ),
            SizedBox(height: 20),
            Center(
              child: Text(
                'Posible logo 2',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Center(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(15),
                child: Image.asset(
                  'assets/images/logo2.png',
                  width: 250,
                  height: 250,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
