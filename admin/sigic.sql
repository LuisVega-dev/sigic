-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-08-2025 a las 00:37:40
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
  `texto` mediumblob NOT NULL
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
  `imagen` varchar(255) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `contraseña`, `imagen`, `admin`) VALUES
(7, 'Luis Vega', 'luismanuelvegaramirez3@gmail.com', 'scrypt:32768:8:1$7Y68jZWEfpMSTVdL$2822b2c78ab0cf5f0cc36a2d0cced9e14a33fbd8d62107687c712d2b1dae5e15be6afbcdae78e22da0a60dd3eff078e07d9f6a2278417495d23e8e38d37661da', 'IMG_20250610_010413.jpg', 1),
(9, 'Andres Torres', 'andrestorres@gmail.com', 'scrypt:32768:8:1$QTfehHKWxxlJVB6l$d79e20d2357745a2aabf0777150d081344351b5c772ecceef822903ccffe4c8a1161f5247f891cdc341fd4fdc99d06861826d59ae3611b532e5cc3d152ea5991', NULL, 0),
(13, 'makutorres', 'karinameza@gmail.com', 'scrypt:32768:8:1$LgsMyxATnIH3bxzw$c89725f8c4c1ff75e634aacd610382f707a093f46b52e4c7ad5a0056f3b245b9adf609785c20f09dd8e8a185b86cc5d0d74e6d56acf4616cc4108d8e185c8723', NULL, 0),
(14, 'dwinarin villafañe', 'villafaneoctavio8@gmail.com', 'scrypt:32768:8:1$6DwOziGwpsRbThkt$ddc7ce30273e9126957cffa2d3535141d542e5298e6b5071f937709129f9cb3d2b6639c61919a0a3701e270f5c29483d5b420ce8671742d8fa2ff70e0ebaa8bf', NULL, 0),
(15, 'Luis Vega', 'pochoagario@gmail.com', 'scrypt:32768:8:1$8JkNrLu53Q8CON1S$e2dbb5ebbd121b8983b4438e225580e07af17e21ecfa5ce26b03d996bb7cb080df53fb278b242c4b4fd416a3c9b07ba0e0fdce6d3d681bc1c303b3938068a72a', NULL, 0);

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
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`id_contenido`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
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
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `contenido_id_imagen` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `permisos`
--
ALTER TABLE `permisos`
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
