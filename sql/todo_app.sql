-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2024. Dec 02. 23:01
-- Kiszolgáló verziója: 10.4.32-MariaDB
-- PHP verzió: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `todo_app`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `barati_felkeresek`
--

CREATE TABLE `barati_felkeresek` (
  `id` int(11) NOT NULL,
  `kuldte` int(11) NOT NULL,
  `fogadta` int(11) NOT NULL,
  `allapot` enum('függőben','elfogadva','elutasítva') DEFAULT 'függőben',
  `kuldve` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `baratok`
--

CREATE TABLE `baratok` (
  `id` int(11) NOT NULL,
  `felhasznalo_1` int(11) NOT NULL,
  `felhasznalo_2` int(11) NOT NULL,
  `baratsag_kezdete` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `feladatok`
--

CREATE TABLE `feladatok` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `priority` enum('Alacsony','Átlagos','Magas') DEFAULT 'Átlagos',
  `environment` varchar(50) DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `feladat_meghivottak`
--

CREATE TABLE `feladat_meghivottak` (
  `task_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_creator` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `felhasznalok`
--

CREATE TABLE `felhasznalok` (
  `id` int(11) NOT NULL,
  `keresztnev` varchar(120) NOT NULL,
  `vezeteknev` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `jelszo` text NOT NULL,
  `points` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `barati_felkeresek`
--
ALTER TABLE `barati_felkeresek`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kuldte` (`kuldte`),
  ADD KEY `fogadta` (`fogadta`);

--
-- A tábla indexei `baratok`
--
ALTER TABLE `baratok`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unikalis_baratsag` (`felhasznalo_1`,`felhasznalo_2`),
  ADD KEY `felhasznalo_2` (`felhasznalo_2`);

--
-- A tábla indexei `feladatok`
--
ALTER TABLE `feladatok`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- A tábla indexei `feladat_meghivottak`
--
ALTER TABLE `feladat_meghivottak`
  ADD PRIMARY KEY (`task_id`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- A tábla indexei `felhasznalok`
--
ALTER TABLE `felhasznalok`
  ADD PRIMARY KEY (`id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `barati_felkeresek`
--
ALTER TABLE `barati_felkeresek`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT a táblához `baratok`
--
ALTER TABLE `baratok`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT a táblához `feladatok`
--
ALTER TABLE `feladatok`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- AUTO_INCREMENT a táblához `felhasznalok`
--
ALTER TABLE `felhasznalok`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Megkötések a kiírt táblákhoz
--

--
-- Megkötések a táblához `barati_felkeresek`
--
ALTER TABLE `barati_felkeresek`
  ADD CONSTRAINT `barati_felkeresek_ibfk_1` FOREIGN KEY (`kuldte`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `barati_felkeresek_ibfk_2` FOREIGN KEY (`fogadta`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE;

--
-- Megkötések a táblához `baratok`
--
ALTER TABLE `baratok`
  ADD CONSTRAINT `baratok_ibfk_1` FOREIGN KEY (`felhasznalo_1`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `baratok_ibfk_2` FOREIGN KEY (`felhasznalo_2`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE;

--
-- Megkötések a táblához `feladatok`
--
ALTER TABLE `feladatok`
  ADD CONSTRAINT `feladatok_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE;

--
-- Megkötések a táblához `feladat_meghivottak`
--
ALTER TABLE `feladat_meghivottak`
  ADD CONSTRAINT `feladat_meghivottak_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `feladatok` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `feladat_meghivottak_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `felhasznalok` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
