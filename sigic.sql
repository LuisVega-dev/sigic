-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-07-2025 a las 17:07:19
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sigic`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contenido`
--

CREATE TABLE `contenido` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `tipo` enum('textual','imagen','video') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `editor`
--

CREATE TABLE `editor` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `editor`
--

INSERT INTO `editor` (`id`, `nombre`, `correo`, `contraseña`, `id_usuario`, `imagen`) VALUES
(2, 'Luis Vega', 'luismanuelvegaramirez3@gmail.com', 'scrypt:32768:8:1$ifYGVCUqiVAREcU5$4a94845a95c8f5b11604d5f76e52032af469da747dc1f9ac9a13734def250422fac57e41251e0f4dfd84c1555f5300e8ed6d09e1c0653e538f1a3869e8fe4ee9', 7, 'Imagen_de_WhatsApp_2025-06-10_a_las_01.13.37_2c108031.jpg'),
(3, 'Andres Torres', 'andrestorres@gmail.com', 'scrypt:32768:8:1$HQ4dDxaVcK42CxCq$629b82696be63a36e13978b1faf2b843d58f32840bf6648dcd63a38b9c613cfb33a9e16de50e238cddbf6031d00f3f6b22f64cabe41f540ecef90ce1b0f44ead', 9, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `id_contenido` int(11) NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `id_editor` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_permiso` datetime NOT NULL,
  `datos_permiso` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `textual`
--

CREATE TABLE `textual` (
  `id_contenido` int(11) NOT NULL,
  `texto` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `contraseña`, `imagen`) VALUES
(7, 'Luis Vega', 'luismanuelvegaramirez3@gmail.com', 'scrypt:32768:8:1$d9jvolArhWQQuiyz$0afb3a3ed435af6c79f921e45c87996c0aa69098776b56e503cd11ebafee4a6d7fcf0cbd37b6ea126968bdead33aaed404f4d00aeddd74186264091bf2cc1e97', 'Imagen_de_WhatsApp_2025-06-10_a_las_01.13.37_2c108031.jpg'),
(9, 'Andres Torres', 'andrestorres@gmail.com', 'scrypt:32768:8:1$SqE6oHKDzMSo9TI6$7dfcf74785a8bc38fbaf4d934c31c57fede771ed1cdb1057e4180cb8da9308a926e60a37219a0a6a1e36aa67b51d34534430b58afc6ed6be295e3162801ea453', NULL),
(13, 'Karina Meza', 'karinameza@gmail.com', 'scrypt:32768:8:1$Opel6hvEXe1GtYQO$4f1e9686b910ba979da90f4ae9f4450a6065d29b953298c565526e0f77971b172e66162170322aa296ffc8ec33b11c05b229db6037810ff94dfc53f12533e1b9', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `video`
--

CREATE TABLE `video` (
  `id_contenido` int(11) NOT NULL,
  `video` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contenido`
--
ALTER TABLE `contenido`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `editor`
--
ALTER TABLE `editor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id_editor` (`id_usuario`);

--
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`id_contenido`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `editor_id_editor_permisos` (`id_editor`),
  ADD KEY `usuario_id_usuario_permisos` (`id_usuario`);

--
-- Indices de la tabla `textual`
--
ALTER TABLE `textual`
  ADD PRIMARY KEY (`id_contenido`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`id_contenido`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contenido`
--
ALTER TABLE `contenido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `editor`
--
ALTER TABLE `editor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `editor`
--
ALTER TABLE `editor`
  ADD CONSTRAINT `usuario_id_editor` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `contenido_id_imagen` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD CONSTRAINT `editor_id_editor_permisos` FOREIGN KEY (`id_editor`) REFERENCES `editor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usuario_id_usuario_permisos` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `textual`
--
ALTER TABLE `textual`
  ADD CONSTRAINT `contenido_id_textual` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `video`
--
ALTER TABLE `video`
  ADD CONSTRAINT `contenido_id_video` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
