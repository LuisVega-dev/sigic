// ignore_for_file: avoid_unnecessary_containers

import 'package:flutter/material.dart';
import 'package:sigic/widgets/nav_bar.dart';

void main() {
  runApp(Sigic());
}

class Sigic extends StatelessWidget {
  const Sigic({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sigic',
      home: SigicHomme(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class SigicHomme extends StatefulWidget {
  const SigicHomme({super.key});

  @override
  State<SigicHomme> createState() => _SigicHommeState();
}

class _SigicHommeState extends State<SigicHomme> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 32, 32, 32),
      appBar: AppBar(
        title: Text(
          'Bienvenidos a Sigic',
          style: TextStyle(
            color: Colors.white,
            fontFamily: 'Roboto',
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: const Color.fromARGB(255, 32, 32, 32),
        iconTheme: IconThemeData(color: Colors.white),
      ),
      drawer: SigicBar(),
      body: Container(
        child: ListView(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset('assets/images/logo1.png', width: 150, height: 150),
                SizedBox(width: 20),
                Image.asset('assets/images/logo2.png', width: 150, height: 150),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
