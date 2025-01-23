-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2021 at 11:52 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sms`
--

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--

CREATE TABLE `Products` (
  `pid` int(11) NOT NULL,
  `productname` varchar(50) NOT NULL,
  `brand` varchar(100) NOT NULL,
  `price` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`pid`, `productname`, `brand`,`price`) VALUES
(1, 'Tea', 'Red Label', 175),
(2, 'Bread', 'Britania', 50),
(3, 'Butter', 'Amul', 70),
(4, 'Noodles', 'Nestle', 80),
(5, 'Milk', 'Nandini', 20);

-- --------------------------------------------------------

--
-- Table structure for table `Orders`
--

CREATE TABLE `Orders` (
  `oid` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `item` varchar(50) NOT NULL,
  `quantity` int(11) NOT NULL,
  `method` varchar(50) NOT NULL,
  `time` time NOT NULL,
  `date` date NOT NULL,
  `category` varchar(50) NOT NULL,
  `number` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Orders`
--

INSERT INTO `Orders` (`oid`, `email`, `name`, `item`, `quantity`, `method`, `time`, `date`, `category`, `number`) VALUES
(2, 'abc@gmail.com', 'Riya Singh', 'Bread', 1, 'cash', '21:20:00', '2024-07-04', 'Bakery', '9874561110'),
(5, 'bcd@gmail.com', 'Shyam Chaturvedi', 'Tea', 2, 'UPI', '18:06:00', '2024-07-03', 'Beverage', '9874563210');

--
-- Triggers `Orders`
--
DELIMITER $$
CREATE TRIGGER `OrdersDelete` BEFORE DELETE ON `Orders` FOR EACH ROW INSERT INTO trigr VALUES(null,OLD.oid,OLD.email,OLD.name,'ORDER DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `OrdersUpdate` AFTER UPDATE ON `Orders` FOR EACH ROW INSERT INTO trigr VALUES(null,NEW.oid,NEW.email,NEW.name,'ORDER UPDATED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Ordersinsertion` AFTER INSERT ON `Orders` FOR EACH ROW INSERT INTO trigr VALUES(null,NEW.oid,NEW.email,NEW.name,'ORDER INSERTED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `name`, `email`) VALUES
(1, 'ANEES', 'ARK@GMAIL.COM'),
(2, 'test', 'test@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `trigr`
--

CREATE TABLE `trigr` (
  `tid` int(11) NOT NULL,
  `oid` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trigr`
--

INSERT INTO `trigr` (`tid`, `oid`, `email`, `name`, `action`, `timestamp`) VALUES
(1, 2, 'abc@gmail.com', 'Riya Singh', 'ORDER INSERTED', '2020-12-02 16:35:10'),
(2, 5, 'bcd@gmail.com', 'Shyam Chaturvedi', 'ORDER INSERTED', '2020-12-02 16:37:34');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `usertype` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `usertype`, `email`, `password`) VALUES
(13, 'owner', 'Owner', 'owner@gmail.com', 'owner'),
(14, 'customer', 'Customer', 'customer@gmail.com', 'customer');
--
-- Indexes for dumped tables
--
--
-- Indexes for table `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`pid`);

--
-- Indexes for table `Orders`
--
ALTER TABLE `Orders`
  ADD PRIMARY KEY (`oid`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trigr`
--
ALTER TABLE `trigr`
  ADD PRIMARY KEY (`tid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Products`
--
ALTER TABLE `Products`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `Orders`
  MODIFY `oid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `trigr`
--
ALTER TABLE `trigr`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
