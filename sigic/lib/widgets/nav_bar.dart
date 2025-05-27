import 'package:flutter/material.dart';
import 'package:sigic/screen/developers.dart';
import 'package:sigic/screen/posibles_logos.dart';
import 'package:sigic/widgets/w_acerca_de.dart';

class SigicBar extends StatelessWidget {
  const SigicBar({super.key});
  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color.fromARGB(255, 32, 32, 32),
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 20.0),
            child: Text(
              'MENU',
              style: TextStyle(
                color: Colors.white,
                fontFamily: 'Roboto',
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          DrawerHeader(
            child: UserAccountsDrawerHeader(
              accountName: Text('SIGIC', style: TextStyle(color: Colors.white)),
              accountEmail: Text(
                'Sistema de Geolocalización Indigena',
                style: TextStyle(color: Colors.white),
              ),
              decoration: BoxDecoration(
                shape: BoxShape.rectangle,
                borderRadius: BorderRadius.circular(10),
                color: const Color.fromARGB(255, 126, 126, 126),
              ),
            ),
          ),
          ListTile(
            leading: Icon(Icons.home, color: Colors.white),
            title: Text('Inicio', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context); // Cierra el Drawer
            },
          ),
          ListTile(
            title: Text(
              'Desarrolladores',
              style: TextStyle(color: Colors.white),
            ),
            leading: Icon(Icons.person_rounded, color: Colors.white),
            onTap: () {
              // Acción al seleccionar "Desarrolladores"
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const DevelopersInfo()),
              );
            },
          ),
          ListTile(
            title: Text(
              'Posibles Logos',
              style: TextStyle(color: Colors.white),
            ),
            leading: Icon(Icons.image, color: Colors.white),
            onTap: () {
              // Acción al seleccionar "Posibles Logos"
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const PosiblesLogos()),
              );
            },
          ),
          ListTile(
            title: Text('Acerda de', style: TextStyle(color: Colors.white)),
            leading: Icon(Icons.info, color: Colors.white),
            onTap: () {
              // Acción al seleccionar "Acerca de"
              showModalBottomSheet(
                context: context,
                builder: (context) => acercaDe(),
                isScrollControlled: true,
                backgroundColor: Colors.transparent,
              );
            },
          ),
        ],
      ),
    );
  }
}
