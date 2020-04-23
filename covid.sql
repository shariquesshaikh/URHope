-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2020 at 02:57 AM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `covid`
--

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `regno` varchar(100) DEFAULT NULL,
  `phone` char(11) DEFAULT NULL,
  `pin` char(6) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `sex` varchar(100) DEFAULT NULL,
  `currProfile` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `social` varchar(100) DEFAULT NULL,
  `services` varchar(100) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `about` varchar(255) DEFAULT NULL,
  `govtID` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`id`, `name`, `username`, `password`, `regno`, `phone`, `pin`, `role`, `website`, `age`, `sex`, `currProfile`, `address`, `social`, `services`, `branch`, `about`, `govtID`) VALUES
(19, 'Jino Jossy', 'jinojossy93@gmail.com', 'bf5bd1eb9ab20084c050fe41cd341d39', NULL, '9746785785', '691306', 'v', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(20, 'Jijo Jossy', 'jinojossy93+asc1@gmail.com', 'bf5bd1eb9ab20084c050fe41cd241d39', NULL, '9746785784', '691305', 'v', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(1, 'Zuhair Abbas', 'zuhairabs@gmail.com', 'bf5bd1eb9ec20084c050fe41cd341d39', NULL, '9022122553', '400055', 'v', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 'Sharique', 'sharique.shaikh.0123@gmail.com', '482c811da5d5b4bc6d497ffa98491e38', NULL, '8104150837', '401106', 'v', NULL, NULL, NULL, NULL, 'sharique.shaikh.0123@gmail.com', NULL, NULL, NULL, 'sharique.shaikh.0123@gmail.com', NULL),
(4, 'Test User', 'testuser@gmail.com', '32250170a0dca92d53ec9624f336ca24', NULL, '9869547044', '401107', 'v', 'https://www.website.com', NULL, NULL, NULL, 'Mumbai', 'www.facebook.com', 'Food', NULL, 'I am a test user', '123123123123'),
(6, 'User', 'user@gmail.com', 'ee11cbb19052e40b07aac0ca060c23ee', 'None', '9869547044', '401107', 'n', 'https://www.website.com', NULL, NULL, NULL, 'Gujarat', 'www.facebook.com', '---- Select Services ----', 'Mumbai', 'This is an NGO to help people', '123123123123');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `task` varchar(255) DEFAULT NULL,
  `posted` datetime NOT NULL DEFAULT current_timestamp(),
  `grp` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `location` varchar(6) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `vol_num` int(255) DEFAULT NULL,
  `task_det` varchar(255) DEFAULT NULL,
  `t_type` varchar(255) DEFAULT NULL,
  `abt_grp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`id`, `task`, `posted`, `grp`, `website`, `location`, `phone`, `vol_num`, `task_det`, `t_type`, `abt_grp`) VALUES
(1, 'Task 1', '0000-00-00 00:00:00', 'User', 'https://www.website.com', '401107', 2147483647, 12, 'will delete it', 'Food', NULL),
(2, 'Task 2', '0000-00-00 00:00:00', 'User', 'https://www.website.com', '401107', 2147483647, 90, 'New', 'Food', NULL),
(3, 'Task 3', '2020-04-19 03:22:10', 'User', 'https://www.website.com', '401107', 2147483647, 4, 'Updated', 'Shelter', NULL),
(4, 'Task4', '2020-04-19 04:44:10', 'User', 'https://www.website.com', '401107', 2147483647, 5, 'Task 5 is being added', 'Food', NULL),
(5, 'Task 8', '2020-04-19 04:49:25', 'User', 'https://www.website.com', '401107', 2147483647, 8, 'New TAsk', 'Medicine', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

--
-- Table structure for table `members`
--

CREATE TABLE `podata` (
  `pin` char(6) PRIMARY KEY,
  `officename` varchar(100) DEFAULT NULL,
  `divisionname` varchar(100) DEFAULT NULL,
  `regionname` varchar(100) DEFAULT NULL,
  `circlename` varchar(100) DEFAULT NULL,
  `taluk` varchar(100) DEFAULT NULL,
  `districtname` varchar(100) DEFAULT NULL,
  `relsuboffice` varchar(100) DEFAULT NULL,
  `statename` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
