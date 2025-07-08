import 'package:flutter/material.dart';

Widget acercaDe() => DraggableScrollableSheet(
  initialChildSize: 0.33,
  minChildSize: 0.2,
  maxChildSize: 0.9,
  builder:
      (_, scrollController) => Container(
        padding: EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color.fromARGB(255, 58, 58, 58),
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(20),
            topRight: Radius.circular(20),
          ),
        ),
        child: ListView(
          controller: scrollController,
          children: [
            Center(
              child: Container(
                width: 150,
                height: 7,
                decoration: BoxDecoration(
                  color: const Color.fromARGB(255, 32, 32, 32),
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
            SizedBox(height: 10),
            Center(
              child: Text(
                'Acerca de SIGIC',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            SizedBox(height: 16),
            Text(
              'SIGIC es una aplicación diseñada para facilitar la gestión de información y procesos. '
              'Nuestro objetivo es proporcionar herramientas eficientes y fáciles de usar para nuestros usuarios.',
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
            SizedBox(height: 16),
            Text(
              'Versión: 1.0.0',
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
            SizedBox(height: 16),
            Text(
              'Desarrollado por: Equipo SIGIC',
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
            SizedBox(height: 16),
            Center(
              child: Text(
                '© ${DateTime.now().year} SIGIC. Todos los derechos reservados.',
                style: TextStyle(fontSize: 14, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
);
