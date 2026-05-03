-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2026 at 04:29 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_apotek_elvaa`
--

-- --------------------------------------------------------

--
-- Table structure for table `dokter_elva`
--

CREATE TABLE `dokter_elva` (
  `id_dokter_elva` int(11) NOT NULL,
  `nama_dokter_elva` varchar(50) NOT NULL,
  `spesialis_elva` varchar(100) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `kota_elva` varchar(100) NOT NULL,
  `no_tlp_elva` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dokter_elva`
--

INSERT INTO `dokter_elva` (`id_dokter_elva`, `nama_dokter_elva`, `spesialis_elva`, `alamat`, `kota_elva`, `no_tlp_elva`) VALUES
(1, 'Dr. Andi Suprianto', 'Umum', 'Jl. Padasuka No. 80 ', 'Kota Cimahi', '0821281211'),
(2, 'Dr. Budi Santoso', 'Umum', 'Jl. Citereup No.70 ', 'Kota Cimahi', '012818182'),
(3, 'Dr. Akram', 'Spesialis Umum', 'Jl. Kemangi KM. 1,5 No. 17, Citeureup, Kec. Cimahi Utara, Kota Cimahi, Jawa Barat 40512.', 'Kota Cimahi', '089735416254'),
(4, 'Dr.  Irsad', 'Jantung', 'Jl. Karya Bakti  No. 90, Citeureup, Kec. Cimahi Utara, Kota Cimahi, Jawa Barat 40512.', 'Kota Cimahi', '082117099284');

-- --------------------------------------------------------

--
-- Table structure for table `gudang_elva`
--

CREATE TABLE `gudang_elva` (
  `id_gudang_elva` int(11) NOT NULL,
  `nama_gudang_elva` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gudang_elva`
--

INSERT INTO `gudang_elva` (`id_gudang_elva`, `nama_gudang_elva`) VALUES
(1, 'Gudang Utama'),
(2, 'Gudang Utama Barat');

-- --------------------------------------------------------

--
-- Table structure for table `kategori_elva`
--

CREATE TABLE `kategori_elva` (
  `id_kategori_elva` int(11) NOT NULL,
  `nama_kategori_elva` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kategori_elva`
--

INSERT INTO `kategori_elva` (`id_kategori_elva`, `nama_kategori_elva`) VALUES
(1, 'Obat Bebas'),
(2, 'Obat Keras'),
(3, 'Vitamin'),
(4, 'Alat Kesehatan');

-- --------------------------------------------------------

--
-- Table structure for table `obat_elva`
--

CREATE TABLE `obat_elva` (
  `id_obat_elva` int(11) NOT NULL,
  `kode_obat_elva` varchar(50) DEFAULT NULL,
  `nama_obat_elva` varchar(100) DEFAULT NULL,
  `jenis_obat_elva` varchar(100) DEFAULT NULL,
  `stok_elva` int(11) DEFAULT NULL,
  `harga_elva` int(11) DEFAULT NULL,
  `tanggal_exp_elva` date DEFAULT NULL,
  `id_gudang_elva` int(11) DEFAULT NULL,
  `kategori_id_elva` int(11) DEFAULT NULL,
  `gambar_elva` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `obat_elva`
--

INSERT INTO `obat_elva` (`id_obat_elva`, `kode_obat_elva`, `nama_obat_elva`, `jenis_obat_elva`, `stok_elva`, `harga_elva`, `tanggal_exp_elva`, `id_gudang_elva`, `kategori_id_elva`, `gambar_elva`) VALUES
(1, 'OBT001', 'Paracetamol', 'tablet', 55, 5000, '2027-02-10', 1, 1, 'paracetamol.png'),
(2, 'OBT002', 'Amoxicillin', 'tablet', 35, 12000, '2028-02-16', 1, 2, 'amoxilin.png'),
(3, 'OBT003', 'Vitamin C 1000mg', 'tablet', 127, 7000, '2027-01-20', 1, 3, 'vitamin_c.png'),
(4, 'OBT004', 'Antasida Doen', 'tablet', 59, 3500, '2026-08-10', 2, 1, 'antasida-doen.png'),
(5, 'OBT005', 'OBH Sirup 100ml', 'Sirup', 80, 12000, '2026-11-30', 2, 1, 'obh-sirup.png'),
(8, 'OBT006', 'Asam Mefenamat 500mg', 'tablet', 92, 4000, '2027-03-05', 1, 2, 'Asam-Mefenamat-500mg.png'),
(9, 'OBT007', 'Cetirizine 10mg', 'kapsul', 107, 3500, '2026-09-25', 1, 2, 'Cetirizine-10mg.png'),
(10, 'OBT008', 'Salbutamol Tablet', 'tablet', 81, 5000, '2026-12-10', 2, 2, 'salbutamol-tablet.png'),
(19, 'OBT009', 'Hufagrip-bp', 'Sirup', 90, 15000, '2029-02-07', 1, 1, 'hufagrip-bp.png'),
(32, 'OBT010', 'Promagh', 'tablet', 105, 18453, '2031-01-10', 1, 1, 'promagh.png'),
(273, 'OBT011', 'Ibuprofen 400mg', 'tablet', 120, 8000, '2028-05-10', 1, 2, 'ibuprofen400.png'),
(274, 'OBT012', 'Ibuprofen 400mg', 'tablet', 95, 8000, '2028-07-15', 2, 2, 'ibuprofen400.png'),
(275, 'OBT013', 'Metformin 500mg', 'tablet', 140, 9000, '2029-03-20', 1, 2, 'metformin.png'),
(276, 'OBT014', 'Metformin 500mg', 'tablet', 110, 9000, '2029-06-18', 2, 2, 'metformin.png'),
(277, 'OBT015', 'Amlodipine 10mg', 'tablet', 100, 7500, '2028-09-12', 1, 2, 'amlodipine.png'),
(278, 'OBT016', 'Amlodipine 10mg', 'tablet', 90, 7500, '2028-11-01', 2, 2, 'amlodipine.png'),
(279, 'OBT017', 'Captopril 25mg', 'tablet', 130, 6000, '2027-12-11', 1, 2, 'captopril.png'),
(280, 'OBT018', 'Captopril 25mg', 'tablet', 105, 6000, '2027-10-09', 2, 2, 'captopril.png'),
(281, 'OBT019', 'Lansoprazole 30mg', 'kapsul', 80, 15000, '2029-01-01', 1, 2, 'lansoprazole.png'),
(282, 'OBT020', 'Lansoprazole 30mg', 'kapsul', 75, 15000, '2029-04-01', 2, 2, 'lansoprazole.png'),
(283, 'OBT021', 'Simvastatin 20mg', 'tablet', 160, 8500, '2028-08-14', 1, 2, 'simvastatin.png'),
(284, 'OBT022', 'Simvastatin 20mg', 'tablet', 130, 8500, '2028-10-21', 2, 2, 'simvastatin.png'),
(285, 'OBT023', 'Allopurinol 100mg', 'tablet', 120, 7000, '2029-02-15', 1, 2, 'allopurinol.png'),
(286, 'OBT024', 'Allopurinol 100mg', 'tablet', 88, 7000, '2029-05-10', 2, 2, 'allopurinol.png'),
(287, 'OBT025', 'Domperidone 10mg', 'tablet', 129, 5000, '2027-11-30', 1, 1, 'domperidone.png'),
(288, 'OBT026', 'Domperidone 10mg', 'tablet', 125, 5000, '2027-09-30', 2, 1, 'domperidone.png'),
(289, 'OBT027', 'Betadine 60ml', 'cair', 60, 12000, '2030-01-01', 1, 4, 'betadine.png'),
(290, 'OBT028', 'Betadine 60ml', 'cair', 54, 12000, '2030-03-01', 2, 4, 'betadine.png'),
(291, 'OBT029', 'Zinc 20mg', 'tablet', 200, 4000, '2028-12-12', 1, 3, 'zinc.png'),
(292, 'OBT030', 'Zinc 20mg', 'tablet', 180, 4000, '2028-10-10', 2, 3, 'zinc.png'),
(293, 'OBT031', 'Magnesium Trisilicate', 'tablet', 78, 6500, '2027-06-15', 1, 1, 'magnesium.png'),
(294, 'OBT032', 'Magnesium Trisilicate', 'tablet', 80, 6500, '2027-07-20', 2, 1, 'magnesium.png'),
(295, 'OBT033', 'Bisoprolol 5mg', 'tablet', 100, 10000, '2029-02-20', 1, 2, 'bisoprolol.png'),
(296, 'OBT034', 'Bisoprolol 5mg', 'tablet', 85, 10000, '2029-04-15', 2, 2, 'bisoprolol.png'),
(297, 'OBT035', 'Vitamin D3 1000IU', 'tablet', 150, 10000, '2029-06-01', 1, 3, 'vitamind.png'),
(298, 'OBT036', 'Vitamin D3 1000IU', 'tablet', 129, 10000, '2029-08-01', 2, 3, 'vitamind.png'),
(299, 'OBT037', 'ORS Sachet', 'serbuk', 245, 3000, '2028-05-05', 1, 1, 'ors.png'),
(300, 'OBT038', 'ORS Sachet', 'serbuk', 195, 3000, '2028-07-05', 2, 1, 'ors.png'),
(301, 'OBT039', 'Gentamicin Salep', 'salep', 70, 9000, '2027-03-03', 1, 2, 'gentamicin.png'),
(302, 'OBT040', 'Gentamicin Salep', 'salep', 65, 9000, '2027-04-04', 2, 2, 'gentamicin.png'),
(303, 'OBT041', 'Prednisone 5mg', 'tablet', 110, 8000, '2028-02-02', 1, 2, 'prednisone.png'),
(304, 'OBT042', 'Prednisone 5mg', 'tablet', 95, 8000, '2028-05-02', 2, 2, 'prednisone.png'),
(305, 'OBT043', 'Hydrocortisone Cream', 'salep', 75, 11000, '2029-09-09', 1, 2, 'hydrocortisone.png'),
(306, 'OBT044', 'Hydrocortisone Cream', 'salep', 60, 11000, '2029-11-11', 2, 2, 'hydrocortisone.png'),
(307, 'OBT045', 'Cetirizine Sirup', 'sirup', 84, 10000, '2027-06-06', 1, 1, 'cetirizinesirup.png'),
(308, 'OBT046', 'Cetirizine Sirup', 'sirup', 70, 10000, '2027-08-06', 2, 1, 'cetirizinesirup.png'),
(309, 'OBT047', 'Multivitamin Anak', 'tablet', 190, 12000, '2029-01-01', 1, 3, 'multivitamin.png'),
(310, 'OBT048', 'Multivitamin Anak', 'tablet', 170, 12000, '2029-03-01', 2, 3, 'multivitamin.png'),
(311, 'OBT049', 'Asam Folat 400mcg', 'tablet', 160, 5000, '2028-04-14', 1, 3, 'asamfolat.png'),
(312, 'OBT050', 'Asam Folat 400mcg', 'tablet', 140, 5000, '2028-06-14', 2, 3, 'asamfolat.png'),
(313, 'OBT051', 'Clindamycin 300mg', 'kapsul', 100, 15000, '2029-07-01', 1, 2, 'clindamycin.png'),
(314, 'OBT052', 'Dexamethasone 0.5mg', 'tablet', 120, 6000, '2028-09-01', 1, 2, 'dexamethasone.png'),
(315, 'OBT053', 'Ranitidine 150mg', 'tablet', 110, 7000, '2028-12-01', 1, 1, 'ranitidine.png'),
(316, 'OBT054', 'Miconazole Cream', 'salep', 90, 13000, '2029-05-01', 1, 2, 'miconazole.png'),
(317, 'OBT055', 'Salicylic Acid 2%', 'cair', 80, 10000, '2028-03-01', 1, 4, 'salicylic.png'),
(318, 'OBT056', 'Calcium Lactate', 'tablet', 140, 9000, '2029-04-01', 1, 3, 'calcium.png'),
(319, 'OBT057', 'Neurobion Forte', 'tablet', 150, 14000, '2029-08-01', 1, 3, 'neurobion.png'),
(320, 'OBT058', 'Ambroxol Sirup', 'sirup', 120, 11000, '2027-09-01', 1, 1, 'ambroxol.png'),
(321, 'OBT059', 'Loratadine 10mg', 'tablet', 160, 8000, '2028-01-01', 1, 1, 'loratadine.png'),
(322, 'OBT060', 'Ketoconazole Cream', 'salep', 75, 12000, '2028-11-01', 1, 2, 'ketoconazole.png'),
(323, 'OBT061', 'Spironolactone 25mg', 'tablet', 100, 9000, '2029-02-02', 2, 2, 'spironolactone.png'),
(324, 'OBT062', 'Glimepiride 2mg', 'tablet', 110, 9500, '2029-05-05', 2, 2, 'glimepiride.png'),
(325, 'OBT063', 'Meloxicam 7.5mg', 'tablet', 130, 8500, '2028-07-07', 2, 2, 'meloxicam.png'),
(326, 'OBT064', 'Nystatin Drop', 'cair', 60, 15000, '2029-09-09', 2, 2, 'nystatin.png'),
(327, 'OBT065', 'Erythromycin 250mg', 'tablet', 140, 10000, '2028-04-04', 2, 2, 'erythromycin.png'),
(328, 'OBT066', 'Vitamin K', 'tablet', 90, 11000, '2029-03-03', 2, 3, 'vitamink.png'),
(329, 'OBT067', 'Iron Tablet', 'tablet', 180, 6000, '2028-08-08', 2, 3, 'iron.png'),
(330, 'OBT068', 'Minyak Kayu Putih', 'cair', 199, 15000, '2031-01-01', 2, 1, 'minyak.png'),
(331, 'OBT069', 'Plester Luka', 'alat', 300, 2000, '2032-01-01', 2, 4, 'plester.png'),
(332, 'OBT070', 'Thermometer Digital', 'alat', 50, 50000, '2033-01-01', 2, 4, 'thermometer.png'),
(333, 'OBT071', 'Masker Medis Box', 'alat', 400, 25000, '2032-06-01', 1, 4, 'masker.png'),
(334, 'OBT072', 'Hand Sanitizer 100ml', 'cair', 250, 10000, '2031-09-01', 1, 4, 'handsanitizer.png'),
(335, 'OBT073', 'Alkohol 70% 100ml', 'cair', 220, 8000, '2030-03-01', 1, 4, 'alkohol.png'),
(336, 'OBT074', 'Tolak Angin Cair', 'cair', 180, 4000, '2028-02-02', 1, 1, 'tolakangin.png'),
(337, 'OBT075', 'Bodrex Extra', 'tablet', 200, 3500, '2028-06-06', 1, 1, 'bodrex.png'),
(338, 'OBT076', 'Panadol Anak', 'sirup', 150, 12000, '2027-12-12', 2, 1, 'panadol.png'),
(339, 'OBT077', 'Sangobion', 'tablet', 140, 9000, '2029-10-10', 2, 3, 'sangobion.png'),
(340, 'OBT078', 'Enervon-C', 'tablet', 210, 5000, '2028-05-05', 2, 3, 'enervon.png'),
(341, 'OBT079', 'OBH Combi', 'sirup', 160, 15000, '2028-08-08', 2, 1, 'obhcombi.png'),
(342, 'OBT080', 'Betahistine 6mg', 'tablet', 120, 7000, '2028-09-09', 2, 2, 'betahistine.png'),
(343, 'OBT081', 'Diclofenac 50mg', 'tablet', 130, 9000, '2028-11-11', 1, 2, 'diclofenac.png'),
(344, 'OBT082', 'Cefadroxil 500mg', 'kapsul', 100, 16000, '2029-01-15', 1, 2, 'cefadroxil.png'),
(345, 'OBT083', 'Tetracycline 250mg', 'kapsul', 110, 14000, '2028-03-03', 1, 2, 'tetracycline.png'),
(346, 'OBT084', 'Guaifenesin Sirup', 'sirup', 90, 11000, '2027-07-07', 1, 1, 'guaifenesin.png'),
(347, 'OBT085', 'Paracetamol Sirup', 'sirup', 150, 8000, '2028-12-12', 1, 1, 'paracetamolsirup.png'),
(348, 'OBT086', 'Chlorpheniramine 4mg', 'tablet', 180, 4000, '2028-10-10', 2, 1, 'ctm.png'),
(349, 'OBT087', 'Dextromethorphan', 'sirup', 130, 12000, '2027-05-05', 2, 1, 'dextro.png'),
(350, 'OBT088', 'Fluimucil Sachet', 'serbuk', 120, 17000, '2029-06-06', 2, 2, 'fluimucil.png'),
(351, 'OBT089', 'Acyclovir 400mg', 'tablet', 100, 20000, '2029-09-09', 2, 2, 'acyclovir.png'),
(352, 'OBT090', 'Isosorbide Dinitrate', 'tablet', 95, 10000, '2029-04-04', 2, 2, 'isosorbide.png'),
(353, 'OBT091', 'Cefixime 100mg', 'kapsul', 100, 18000, '2029-07-07', 1, 2, 'cefixime.png'),
(354, 'OBT092', 'Albendazole 400mg', 'tablet', 120, 6000, '2028-02-02', 1, 1, 'albendazole.png'),
(355, 'OBT093', 'Loperamide 2mg', 'tablet', 140, 5000, '2028-05-05', 1, 1, 'loperamide.png'),
(356, 'OBT094', 'Furosemide 40mg', 'tablet', 110, 7000, '2029-08-08', 1, 2, 'furosemide.png'),
(357, 'OBT095', 'Metoclopramide 10mg', 'tablet', 130, 6000, '2028-09-09', 1, 1, 'metoclopramide.png'),
(358, 'OBT096', 'Thiamine 100mg', 'tablet', 150, 5000, '2029-03-03', 2, 3, 'thiamine.png'),
(359, 'OBT097', 'Riboflavin', 'tablet', 140, 4000, '2029-04-04', 2, 3, 'riboflavin.png'),
(360, 'OBT098', 'Vitamin E', 'kapsul', 160, 9000, '2029-11-11', 2, 3, 'vitamine.png'),
(361, 'OBT099', 'Syringe 3ml', 'alat', 300, 1500, '2032-02-02', 2, 4, 'syringe.png'),
(362, 'OBT100', 'Infusion Set', 'alat', 200, 7000, '2032-06-06', 2, 4, 'infusionset.png'),
(363, 'OBT101', 'Carbamazepine 200mg', 'tablet', 120, 12000, '2029-06-01', 1, 2, 'carbamazepine.png'),
(364, 'OBT102', 'Phenytoin 100mg', 'kapsul', 100, 15000, '2029-08-01', 2, 2, 'phenytoin.png'),
(365, 'OBT103', 'Valproic Acid 250mg', 'kapsul', 90, 20000, '2029-07-01', 1, 2, 'valproic.png'),
(366, 'OBT104', 'Levofloxacin 500mg', 'tablet', 130, 18000, '2029-09-01', 2, 2, 'levofloxacin.png'),
(367, 'OBT105', 'Azithromycin 500mg', 'tablet', 150, 17000, '2029-10-01', 1, 2, 'azithromycin.png'),
(368, 'OBT106', 'Ciprofloxacin 500mg', 'tablet', 140, 16000, '2029-11-01', 2, 2, 'ciprofloxacin.png'),
(369, 'OBT107', 'Doxycycline 100mg', 'kapsul', 110, 14000, '2029-12-01', 1, 2, 'doxycycline.png'),
(370, 'OBT108', 'Fluconazole 150mg', 'kapsul', 90, 22000, '2029-05-01', 2, 2, 'fluconazole.png'),
(371, 'OBT109', 'Itraconazole 100mg', 'kapsul', 80, 25000, '2029-04-01', 1, 2, 'itraconazole.png'),
(372, 'OBT110', 'Clarithromycin 500mg', 'tablet', 120, 19000, '2029-03-01', 2, 2, 'clarithromycin.png'),
(373, 'OBT111', 'Gliclazide 80mg', 'tablet', 140, 8500, '2029-06-10', 1, 2, 'gliclazide.png'),
(374, 'OBT112', 'Pioglitazone 15mg', 'tablet', 100, 11000, '2029-07-15', 2, 2, 'pioglitazone.png'),
(375, 'OBT113', 'Losartan 50mg', 'tablet', 150, 9500, '2029-08-20', 1, 2, 'losartan.png'),
(376, 'OBT114', 'Valsartan 80mg', 'tablet', 120, 10500, '2029-09-25', 2, 2, 'valsartan.png'),
(377, 'OBT115', 'Telmisartan 40mg', 'tablet', 130, 10000, '2029-10-05', 1, 2, 'telmisartan.png'),
(378, 'OBT116', 'Clopidogrel 75mg', 'tablet', 100, 13000, '2029-11-15', 2, 2, 'clopidogrel.png'),
(379, 'OBT117', 'Aspirin 80mg', 'tablet', 200, 4000, '2029-12-20', 1, 1, 'aspirin.png'),
(380, 'OBT118', 'Warfarin 2mg', 'tablet', 90, 15000, '2029-06-30', 2, 2, 'warfarin.png'),
(381, 'OBT119', 'Digoxin 0.25mg', 'tablet', 80, 12000, '2029-07-30', 1, 2, 'digoxin.png'),
(382, 'OBT120', 'Propranolol 10mg', 'tablet', 150, 7000, '2029-08-30', 2, 2, 'propranolol.png'),
(383, 'OBT121', 'Atorvastatin 20mg', 'tablet', 160, 9500, '2029-09-10', 1, 2, 'atorvastatin.png'),
(384, 'OBT122', 'Rosuvastatin 10mg', 'tablet', 140, 12000, '2029-10-10', 2, 2, 'rosuvastatin.png'),
(385, 'OBT123', 'Fenofibrate 160mg', 'tablet', 120, 13000, '2029-11-10', 1, 2, 'fenofibrate.png'),
(386, 'OBT124', 'Montelukast 10mg', 'tablet', 150, 9000, '2029-12-10', 2, 2, 'montelukast.png'),
(387, 'OBT125', 'Theophylline 200mg', 'tablet', 100, 8500, '2029-06-05', 1, 2, 'theophylline.png'),
(388, 'OBT126', 'Salbutamol Inhaler', 'alat', 70, 45000, '2031-01-01', 2, 4, 'salbutamolinhaler.png'),
(389, 'OBT127', 'Insulin Glargine', 'cair', 60, 95000, '2029-02-01', 1, 2, 'insulin.png'),
(390, 'OBT128', 'Insulin Aspart', 'cair', 60, 98000, '2029-03-01', 2, 2, 'insulinaspart.png'),
(391, 'OBT129', 'Lactulose Sirup', 'sirup', 90, 20000, '2029-04-01', 1, 1, 'lactulose.png'),
(392, 'OBT130', 'Bisacodyl 5mg', 'tablet', 130, 6000, '2029-05-01', 2, 1, 'bisacodyl.png'),
(393, 'OBT131', 'Ondansetron 4mg', 'tablet', 120, 15000, '2029-06-01', 1, 2, 'ondansetron.png'),
(394, 'OBT132', 'Risperidone 2mg', 'tablet', 90, 20000, '2029-07-01', 2, 2, 'risperidone.png'),
(395, 'OBT133', 'Haloperidol 5mg', 'tablet', 80, 18000, '2029-08-01', 1, 2, 'haloperidol.png'),
(396, 'OBT134', 'Sertraline 50mg', 'tablet', 110, 21000, '2029-09-01', 2, 2, 'sertraline.png'),
(397, 'OBT135', 'Diazepam 5mg', 'tablet', 100, 12000, '2029-10-01', 1, 2, 'diazepam.png'),
(398, 'OBT136', 'Alprazolam 0.5mg', 'tablet', 90, 22000, '2029-11-01', 2, 2, 'alprazolam.png'),
(399, 'OBT137', 'Omeprazole 20mg', 'kapsul', 150, 8000, '2029-12-01', 1, 1, 'omeprazole.png'),
(400, 'OBT138', 'Pantoprazole 40mg', 'tablet', 120, 9000, '2029-06-01', 2, 2, 'pantoprazole.png'),
(401, 'OBT139', 'Sucralfate Sirup', 'sirup', 80, 18000, '2029-07-01', 1, 1, 'sucralfate.png'),
(402, 'OBT140', 'Metronidazole 500mg', 'tablet', 140, 8500, '2029-08-01', 2, 2, 'metronidazole.png'),
(403, 'OBT141', 'Tramadol 50mg', 'kapsul', 110, 15000, '2029-09-01', 1, 2, 'tramadol.png'),
(404, 'OBT142', 'Ketorolac 10mg', 'tablet', 120, 10000, '2029-10-01', 2, 2, 'ketorolac.png'),
(405, 'OBT143', 'Mefenamic Acid Sirup', 'sirup', 100, 12000, '2029-11-01', 1, 1, 'mefenamicsirup.png'),
(406, 'OBT144', 'Cetuximab Injection', 'cair', 40, 150000, '2030-01-01', 2, 2, 'cetuximab.png'),
(407, 'OBT145', 'Amiodarone 200mg', 'tablet', 90, 14000, '2029-06-15', 1, 2, 'amiodarone.png'),
(408, 'OBT146', 'Nifedipine 10mg', 'tablet', 130, 8000, '2029-07-15', 2, 2, 'nifedipine.png'),
(409, 'OBT147', 'Hydralazine 25mg', 'tablet', 80, 9000, '2029-08-15', 1, 2, 'hydralazine.png'),
(410, 'OBT148', 'Candesartan 16mg', 'tablet', 120, 10000, '2029-09-15', 2, 2, 'candesartan.png'),
(411, 'OBT149', 'Lisinopril 10mg', 'tablet', 140, 9500, '2029-10-15', 1, 2, 'lisinopril.png'),
(412, 'OBT150', 'Ramipril 5mg', 'tablet', 120, 9000, '2029-11-15', 2, 2, 'ramipril.png'),
(413, 'OBT151', 'Glucophage XR', 'tablet', 150, 11000, '2029-12-15', 1, 2, 'glucophage.png'),
(414, 'OBT152', 'Novorapid Flexpen', 'cair', 50, 105000, '2030-02-01', 2, 2, 'novorapid.png'),
(415, 'OBT153', 'Voltaren Gel', 'salep', 90, 25000, '2029-05-05', 1, 2, 'voltaren.png'),
(416, 'OBT154', 'Feldene 20mg', 'tablet', 80, 20000, '2029-06-06', 2, 2, 'feldene.png'),
(417, 'OBT155', 'Imodium', 'tablet', 140, 7000, '2029-07-07', 1, 1, 'imodium.png'),
(418, 'OBT156', 'Zovirax Cream', 'salep', 60, 30000, '2029-08-08', 2, 2, 'zovirax.png'),
(419, 'OBT157', 'Canesten Cream', 'salep', 70, 28000, '2029-09-09', 1, 2, 'canesten.png'),
(420, 'OBT158', 'Daktarin Oral Gel', 'salep', 60, 35000, '2029-10-10', 2, 2, 'daktarin.png'),
(421, 'OBT159', 'Betnovate Cream', 'salep', 80, 24000, '2029-11-11', 1, 2, 'betnovate.png'),
(422, 'OBT160', 'Lameson Cream', 'salep', 90, 20000, '2029-12-12', 2, 2, 'lameson.png'),
(423, 'OBT161', 'Folic Acid 5mg', 'tablet', 180, 4000, '2029-06-01', 1, 3, 'folicacid5.png'),
(424, 'OBT162', 'Vitamin B Complex', 'tablet', 200, 6000, '2029-07-01', 2, 3, 'vitbcomplex.png'),
(425, 'OBT163', 'Blackmores Vitamin C', 'tablet', 150, 35000, '2030-01-01', 1, 3, 'blackmoresc.png'),
(426, 'OBT164', 'Hemaviton', 'tablet', 170, 5000, '2029-08-01', 2, 3, 'hemaviton.png'),
(427, 'OBT165', 'Redoxon', 'tablet', 160, 45000, '2030-02-01', 1, 3, 'redoxon.png'),
(428, 'OBT166', 'Betadine Solution 100ml', 'cair', 120, 18000, '2031-01-01', 2, 4, 'betadine100.png'),
(429, 'OBT167', 'Hansaplast Roll', 'alat', 200, 15000, '2032-01-01', 1, 4, 'hansaplast.png'),
(430, 'OBT168', 'Micropore Tape', 'alat', 180, 12000, '2032-02-01', 2, 4, 'micropore.png'),
(431, 'OBT169', 'Gloves Latex Box', 'alat', 150, 40000, '2032-03-01', 1, 4, 'gloves.png'),
(432, 'OBT170', 'Nebulizer', 'alat', 39, 250000, '2033-01-01', 2, 4, 'nebulizer.png'),
(433, 'OBT171', 'Cataflam 50mg', 'tablet', 120, 12000, '2029-04-04', 1, 2, 'cataflam.png'),
(434, 'OBT172', 'Ponstan 500mg', 'tablet', 110, 10000, '2029-05-05', 2, 2, 'ponstan.png'),
(435, 'OBT173', 'Tempra Sirup', 'sirup', 130, 15000, '2029-06-06', 1, 1, 'tempra.png'),
(436, 'OBT174', 'Actifed', 'sirup', 120, 17000, '2029-07-07', 2, 1, 'actifed.png'),
(437, 'OBT175', 'Siladex', 'sirup', 110, 14000, '2029-08-08', 1, 1, 'siladex.png'),
(438, 'OBT176', 'Xanax', 'tablet', 80, 30000, '2029-09-09', 2, 2, 'xanax.png'),
(439, 'OBT177', 'Lexapro', 'tablet', 90, 40000, '2029-10-10', 1, 2, 'lexapro.png'),
(440, 'OBT178', 'Arcoxia 60mg', 'tablet', 100, 25000, '2029-11-11', 2, 2, 'arcoxia.png'),
(441, 'OBT179', 'Celebrex 200mg', 'kapsul', 100, 27000, '2029-12-12', 1, 2, 'celebrex.png'),
(442, 'OBT180', 'Symbicort Inhaler', 'alat', 60, 350000, '2031-05-01', 2, 4, 'symbicort.png'),
(443, 'OBT181', 'Bisolvon', 'sirup', 120, 15000, '2029-06-01', 1, 1, 'bisolvon.png'),
(444, 'OBT182', 'Rhinos SR', 'kapsul', 110, 18000, '2029-07-01', 2, 1, 'rhinos.png'),
(445, 'OBT183', 'Mylanta', 'sirup', 100, 20000, '2029-08-01', 1, 1, 'mylanta.png'),
(446, 'OBT184', 'Polysilane', 'tablet', 130, 12000, '2029-09-01', 2, 1, 'polysilane.png'),
(447, 'OBT185', 'Neozep', 'tablet', 140, 5000, '2029-10-01', 1, 1, 'neozep.png'),
(448, 'OBT186', 'Kalpanax Cream', 'salep', 100, 20000, '2029-11-01', 2, 2, 'kalpanax.png'),
(449, 'OBT187', 'Counterpain', 'salep', 120, 25000, '2029-12-01', 1, 1, 'counterpain.png'),
(450, 'OBT188', 'Salonpas', 'alat', 200, 8000, '2031-01-01', 2, 4, 'salonpas.png'),
(451, 'OBT189', 'FreshCare', 'cair', 180, 12000, '2031-02-01', 1, 1, 'freshcare.png'),
(452, 'OBT190', 'Antimo', 'tablet', 160, 6000, '2029-06-01', 2, 1, 'antimo.png'),
(453, 'OBT191', 'Dulcolax', 'tablet', 130, 8000, '2029-07-01', 1, 1, 'dulcolax.png'),
(454, 'OBT192', 'OB Herbal', 'sirup', 150, 10000, '2029-08-01', 2, 1, 'obherbal.png'),
(455, 'OBT193', 'Komix', 'sirup', 180, 3000, '2029-09-01', 1, 1, 'komix.png'),
(456, 'OBT194', 'Procold', 'tablet', 170, 4000, '2029-10-01', 2, 1, 'procold.png'),
(457, 'OBT195', 'Panadol Extra', 'tablet', 160, 6000, '2029-11-01', 1, 1, 'panadolextra.png'),
(458, 'OBT196', 'Stimuno', 'sirup', 120, 25000, '2029-12-01', 2, 3, 'stimuno.png'),
(459, 'OBT197', 'Curcuma Plus', 'sirup', 130, 18000, '2029-06-01', 1, 3, 'curcuma.png'),
(460, 'OBT198', 'Imboost', 'tablet', 140, 30000, '2029-07-01', 2, 3, 'imboost.png'),
(461, 'OBT199', 'Vitacimin', 'tablet', 200, 3000, '2029-08-01', 1, 3, 'vitacimin.png'),
(462, 'OBT200', 'Tolak Linu', 'tablet', 160, 4000, '2029-09-01', 2, 1, 'tolaklinu.png');

-- --------------------------------------------------------

--
-- Table structure for table `pasien_elva`
--

CREATE TABLE `pasien_elva` (
  `id_pasien_elva` int(11) NOT NULL,
  `nama_lengkap_elva` varchar(100) NOT NULL,
  `tanggal_lahir_elva` date NOT NULL,
  `jenis_kelamin_elva` enum('Laki-laki','Perempuan') NOT NULL,
  `alamat_elva` varchar(255) DEFAULT NULL,
  `no_telepon_elva` varchar(15) DEFAULT NULL,
  `alergi_elva` text DEFAULT NULL,
  `catatan_khusus_elva` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_elva`
--

INSERT INTO `pasien_elva` (`id_pasien_elva`, `nama_lengkap_elva`, `tanggal_lahir_elva`, `jenis_kelamin_elva`, `alamat_elva`, `no_telepon_elva`, `alergi_elva`, `catatan_khusus_elva`) VALUES
(1, 'Arya Supian', '2026-02-14', 'Laki-laki', 'Jl. Amir machmud', '0812121212', 'tidak ada', 'jangan lupa minum obatnya'),
(2, 'Athar', '2026-02-15', 'Laki-laki', 'Jl. Amir machmud', '086543433', 'tidak ada', 'Jangan lupa minum obat'),
(3, 'Irsyad', '2026-04-04', 'Laki-laki', 'Cimahi', '0821782378', '-', '-\r\n'),
(4, 'Naisha', '2026-04-01', 'Perempuan', 'Jl. Kamarung KM. 1,5 No. 69, Citeureup, Kec. Cimahi Utara, Kota Cimahi, Jawa Barat 40512.', '083130568812', 'dingin', '-'),
(5, 'Bilqis Azahra', '2026-04-01', 'Perempuan', 'Jl. Anggrek No. 50, Citeureup, Kec. Cimahi Utara, Kota Cimahi, Jawa Barat 40512.', '089241523091', 'Dingin', '-');

-- --------------------------------------------------------

--
-- Table structure for table `pengiriman_elva`
--

CREATE TABLE `pengiriman_elva` (
  `id_pengiriman_elva` int(11) NOT NULL,
  `id_transaksi_elva` int(11) DEFAULT NULL,
  `no_resi_elva` varchar(100) DEFAULT NULL,
  `id_kurir_elva` int(11) DEFAULT NULL,
  `status_elva` enum('diverifikasi','dikemas','diserahkan_ke_kurir','dalam_perjalanan','sampai','menunggu_verifikasi') DEFAULT 'menunggu_verifikasi',
  `keterangan_elva` text DEFAULT NULL,
  `waktu_update_elva` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `foto_bukti_elva` varchar(255) DEFAULT NULL,
  `qr_resi_elva` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `racikan_elva`
--

CREATE TABLE `racikan_elva` (
  `id_racikan_elva` int(11) NOT NULL,
  `nama_obat_elva` varchar(100) DEFAULT NULL,
  `dosis_elva` varchar(100) DEFAULT NULL,
  `catatan_elva` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `racikan_elva`
--

INSERT INTO `racikan_elva` (`id_racikan_elva`, `nama_obat_elva`, `dosis_elva`, `catatan_elva`) VALUES
(2, 'Paracetamol + CTM', '3x1', 'Sesudah makan'),
(3, 'Amoxicillin Sirup + OBH', '2x1', 'Kocok dahulu'),
(4, 'Salep Asam Salisilat + Sulfur', 'Oles 2x sehari', 'Untuk pemakaian luar'),
(5, 'Vitamin B Kompleks + Vitamin C', '1x1', 'Sesudah makan pagi');

-- --------------------------------------------------------

--
-- Table structure for table `resep_detail_elva`
--

CREATE TABLE `resep_detail_elva` (
  `id_detail_elva` int(11) NOT NULL,
  `id_resep_elva` int(11) DEFAULT NULL,
  `id_obat_elva` int(11) DEFAULT NULL,
  `id_racikan_elva` int(11) DEFAULT NULL,
  `jenis_obat_elva` varchar(100) NOT NULL,
  `dosis_elva` varchar(50) DEFAULT NULL,
  `jumlah_elva` int(11) DEFAULT NULL,
  `catatan_elva` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `resep_detail_elva`
--

INSERT INTO `resep_detail_elva` (`id_detail_elva`, `id_resep_elva`, `id_obat_elva`, `id_racikan_elva`, `jenis_obat_elva`, `dosis_elva`, `jumlah_elva`, `catatan_elva`) VALUES
(11, 23, 3, NULL, 'tablet', '-', 1, '-'),
(12, 23, 19, NULL, 'sirup', '-', 1, '-'),
(13, 23, 32, NULL, 'tablet', '-', 1, '-'),
(14, 23, NULL, 2, 'racikan', '3x1', 1, 'Sesudah makan'),
(15, 23, NULL, 3, 'racikan', '2x1', 1, 'Kocok dahulu'),
(16, 24, 2, NULL, 'tablet', '-', 1, '-'),
(17, 24, 3, NULL, 'tablet', '-', 1, '-'),
(18, 24, 4, NULL, 'tablet', '-', 1, '-'),
(19, 24, NULL, 2, 'racikan', '3x1', 1, 'Sesudah makan'),
(20, 24, NULL, 3, 'racikan', '2x1', 1, 'Kocok dahulu'),
(21, 25, 1, NULL, 'tablet', '-', 12, '-'),
(22, 25, 2, NULL, 'tablet', '-', 1, '-'),
(23, 27, NULL, 2, 'Racikan', '-', 1, '-'),
(24, 27, NULL, 3, 'Racikan', '-', 1, '-'),
(25, 27, NULL, 4, 'Racikan', '-', 1, '-'),
(26, 28, NULL, 2, 'Racikan', '-', 1, '-'),
(27, 28, NULL, 3, 'Racikan', '-', 1, '-'),
(28, 28, NULL, 4, 'Racikan', '-', 1, '-'),
(29, 29, NULL, 2, 'Racikan', '-', 1, '-'),
(30, 29, NULL, 3, 'Racikan', '-', 1, '-'),
(31, 30, NULL, 2, 'Racikan', '3x1', 2, 'Sesudah makan'),
(32, 30, NULL, 3, 'Racikan', '2x1', 1, 'Kocok dahulu'),
(33, 31, 1, NULL, 'tablet', '-', 1, '-'),
(34, 31, 2, NULL, 'tablet', '-', 1, '-'),
(35, 31, 3, NULL, 'tablet', '-', 1, '-'),
(36, 31, NULL, 2, 'Racikan', '3x1', 1, 'Sesudah makan'),
(37, 43, 1, NULL, 'tablet', '-', 1, '-'),
(38, 43, 2, NULL, 'tablet', '-', 1, '-'),
(39, 43, 3, NULL, 'tablet', '-', 1, '-'),
(40, 43, NULL, 2, 'Racikan', '3x1', 1, 'Sesudah makan');

-- --------------------------------------------------------

--
-- Table structure for table `resep_elva`
--

CREATE TABLE `resep_elva` (
  `id_resep_elva` int(11) NOT NULL,
  `no_resep_elva` varchar(50) DEFAULT NULL,
  `id_pasien_elva` int(11) NOT NULL,
  `id_dokter_elva` int(11) NOT NULL,
  `id_transaksi_elva` int(11) NOT NULL,
  `tanggal_resep_elva` datetime NOT NULL,
  `no_tlp_pengambil` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `resep_elva`
--

INSERT INTO `resep_elva` (`id_resep_elva`, `no_resep_elva`, `id_pasien_elva`, `id_dokter_elva`, `id_transaksi_elva`, `tanggal_resep_elva`, `no_tlp_pengambil`) VALUES
(22, 'RSP001', 1, 1, 18, '2026-02-16 07:59:33', '0'),
(23, 'RSP002', 2, 2, 19, '2026-02-16 08:13:09', '0'),
(24, 'RSP003', 1, 2, 20, '2026-02-16 08:17:45', '0'),
(25, 'RSP004', 1, 1, 29, '2026-02-17 07:29:26', '0'),
(26, 'RSP007', 1, 1, 34, '2026-02-19 23:20:49', '0'),
(27, 'RSP008', 3, 1, 39, '2026-04-04 21:17:13', '0'),
(28, 'RSP009', 3, 1, 40, '2026-04-04 21:21:05', '0'),
(29, 'RSP010', 3, 1, 41, '2026-04-04 21:58:53', '0'),
(30, 'RSP011', 2, 1, 42, '2026-04-04 22:05:54', '0'),
(31, 'RSP005', 4, 3, 69, '2026-04-17 15:36:57', '0'),
(43, 'RSP0020', 5, 4, 88, '2026-04-26 22:20:03', '');

-- --------------------------------------------------------

--
-- Table structure for table `tracking_pengiriman_elva`
--

CREATE TABLE `tracking_pengiriman_elva` (
  `id_tracking` int(11) NOT NULL,
  `id_pengiriman_elva` int(11) DEFAULT NULL,
  `status_tracking` varchar(50) DEFAULT NULL,
  `keterangan_tracking` text DEFAULT NULL,
  `waktu_tracking` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tracking_pengiriman_elva`
--

INSERT INTO `tracking_pengiriman_elva` (`id_tracking`, `id_pengiriman_elva`, `status_tracking`, `keterangan_tracking`, `waktu_tracking`) VALUES
(27, 8, 'sampai', 'Paket telah sampai ke tujuan', '2026-02-17 13:16:34'),
(28, 9, 'diproses', 'Pesanan sedang diproses', '2026-02-17 14:16:46'),
(29, 10, 'diproses', 'Pesanan sedang diproses', '2026-02-17 17:04:33'),
(30, 11, 'diproses', 'Pesanan sedang diproses', '2026-04-04 17:13:54'),
(31, 12, 'diproses', 'Pesanan sedang diproses', '2026-04-04 17:15:55'),
(32, 12, 'dikemas', 'Paket sedang dikemas', '2026-04-04 17:16:14'),
(33, 12, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-04 17:16:16'),
(34, 13, 'diproses', 'Pesanan sedang diproses', '2026-04-04 17:18:37'),
(35, 12, 'dalam_perjalanan', 'Sedang menuju alamat tujuan', '2026-04-04 17:24:53'),
(36, 12, 'sampai', 'Paket telah sampai ke tujuan', '2026-04-04 17:28:01'),
(37, 14, 'diproses', 'Pesanan sedang diproses', '2026-04-04 17:31:26'),
(38, 14, 'dikemas', 'Paket sedang dikemas', '2026-04-04 17:31:56'),
(39, 14, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-04 17:32:01'),
(40, 15, 'diproses', 'Pesanan sedang diproses', '2026-04-04 23:56:56'),
(41, 16, 'diproses', 'Pesanan sedang diproses', '2026-04-04 23:57:07'),
(42, 17, 'diproses', 'Pesanan sedang diproses', '2026-04-04 23:57:07'),
(43, 17, 'dikemas', 'Paket sedang dikemas', '2026-04-04 23:57:40'),
(44, 16, 'dikemas', 'Paket sedang dikemas', '2026-04-04 23:57:45'),
(45, 15, 'dikemas', 'Paket sedang dikemas', '2026-04-04 23:57:47'),
(46, 17, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-04 23:57:48'),
(47, 16, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-04 23:57:49'),
(48, 15, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-04 23:57:49'),
(49, 17, 'dalam_perjalanan', 'Sedang menuju alamat tujuan', '2026-04-04 23:58:11'),
(50, 17, 'sampai', 'Paket telah sampai ke tujuan', '2026-04-04 23:58:41'),
(51, 18, 'diproses', 'Pesanan sedang diproses', '2026-04-05 20:55:10'),
(52, 19, 'diproses', 'Pesanan sedang diproses', '2026-04-05 20:56:38'),
(53, 20, 'diproses', 'Pesanan sedang diproses', '2026-04-05 21:47:11'),
(54, 21, 'diproses', 'Pesanan sedang diproses', '2026-04-05 21:52:29'),
(55, 22, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:11:54'),
(56, 23, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:17:22'),
(57, 24, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:18:24'),
(58, 25, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:19:45'),
(59, 26, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:23:22'),
(60, 27, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:27:30'),
(61, 28, 'diproses', 'Pesanan sedang diproses', '2026-04-05 22:32:34'),
(62, 29, 'diproses', 'Pesanan sedang diproses', '2026-04-17 05:51:03'),
(63, 30, 'diproses', 'Pesanan sedang diproses', '2026-04-17 05:56:01'),
(64, 31, 'diproses', 'Pesanan sedang diproses', '2026-04-17 05:57:42'),
(65, 32, 'diproses', 'Pesanan sedang diproses', '2026-04-17 12:42:02'),
(66, 33, 'diproses', 'Pesanan sedang diproses', '2026-04-17 12:43:51'),
(67, 34, 'diproses', 'Pesanan sedang diproses', '2026-04-17 12:58:13'),
(68, 35, 'diproses', 'Pesanan sedang diproses', '2026-04-17 13:05:21'),
(69, 36, 'diproses', 'Pesanan sedang diproses', '2026-04-17 13:05:34'),
(70, 37, 'diproses', 'Pesanan sedang diproses', '2026-04-17 13:09:04'),
(71, 38, 'diproses', 'Pesanan sedang diproses', '2026-04-17 13:12:01'),
(72, 39, 'diproses', 'Pesanan sedang diproses', '2026-04-17 13:42:27'),
(73, 40, 'diproses', 'Pesanan sedang diproses', '2026-04-17 15:28:01'),
(74, 41, 'diproses', 'Pesanan sedang diproses', '2026-04-17 15:39:29'),
(75, 41, 'dikemas', 'Paket sedang dikemas', '2026-04-17 15:39:52'),
(76, 41, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-04-17 15:39:54'),
(77, 41, 'dalam_perjalanan', 'Sedang menuju alamat tujuan', '2026-04-17 15:40:39'),
(78, 41, 'sampai', 'Paket telah sampai ke tujuan', '2026-04-17 15:41:12'),
(79, 42, 'diproses', 'Pesanan sedang diproses', '2026-04-19 13:10:19'),
(80, 43, 'diproses', 'Pesanan sedang diproses', '2026-04-19 13:14:41'),
(81, 44, 'diproses', 'Pesanan sedang diproses', '2026-04-22 09:38:03'),
(82, 45, 'diproses', 'Pesanan sedang diproses', '2026-04-23 10:26:45'),
(83, 46, 'diproses', 'Pesanan sedang diproses', '2026-04-26 13:52:14'),
(84, 47, 'diproses', 'Pesanan sedang diproses', '2026-04-26 19:40:19'),
(85, 53, 'diverifikasi', 'Pesanan telah diverifikasi admin', '2026-05-02 21:23:07'),
(86, 53, 'dikemas', 'Paket sedang dikemas', '2026-05-02 21:24:40'),
(87, 53, 'diserahkan_ke_kurir', 'Paket telah diserahkan kepada kurir', '2026-05-02 21:24:41'),
(88, 53, 'dalam_perjalanan', 'Sedang menuju alamat tujuan', '2026-05-02 21:31:03'),
(89, 53, 'sampai', 'Paket telah sampai ke tujuan', '2026-05-02 21:31:25');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_detail_elva`
--

CREATE TABLE `transaksi_detail_elva` (
  `id_detail_elva` int(11) NOT NULL,
  `id_transaksi_elva` int(11) DEFAULT NULL,
  `id_obat_elva` int(11) DEFAULT NULL,
  `id_racikan_elva` int(11) DEFAULT NULL,
  `jumlah_elva` int(11) DEFAULT NULL,
  `harga_elva` int(11) DEFAULT NULL,
  `diskon_elva` int(11) DEFAULT NULL,
  `total_elva` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `transaksi_detail_elva`
--
DELIMITER $$
CREATE TRIGGER `trg_kurangi_stok_elva` AFTER INSERT ON `transaksi_detail_elva` FOR EACH ROW BEGIN
    UPDATE obat_elva
    SET stok_elva = stok_elva - NEW.jumlah_elva
    WHERE id_obat_elva = NEW.id_obat_elva;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_elva`
--

CREATE TABLE `transaksi_elva` (
  `id_transaksi_elva` int(11) NOT NULL,
  `no_faktur_elva` varchar(50) DEFAULT NULL,
  `tanggal_elva` datetime DEFAULT NULL,
  `id_user_elva` int(11) DEFAULT NULL,
  `id_pasien_elva` int(11) DEFAULT NULL,
  `alamat_elva` text DEFAULT NULL,
  `metode_bayar_elva` varchar(20) DEFAULT NULL,
  `kurir_elva` varchar(50) DEFAULT NULL,
  `ongkir_elva` int(11) DEFAULT NULL,
  `total_elva` int(11) DEFAULT NULL,
  `tipe_elva` enum('online','offline') DEFAULT NULL,
  `status_elva` varchar(255) DEFAULT NULL,
  `waktu_selesai_elva` datetime DEFAULT NULL,
  `status_pengiriman_elva` varchar(50) DEFAULT 'diproses',
  `status_pembayaran_elva` enum('belum_bayar','lunas') DEFAULT 'belum_bayar',
  `bukti_bayar_elva` varchar(255) DEFAULT NULL,
  `status_verifikasi_elva` varchar(50) DEFAULT 'menunggu',
  `metode_detail_elva` varchar(50) DEFAULT NULL,
  `tanggal_pengambilan_elva` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `transaksi_elva`
--
DELIMITER $$
CREATE TRIGGER `before_insert_transaksi_elva` BEFORE INSERT ON `transaksi_elva` FOR EACH ROW BEGIN

    -- ONLINE
    IF NEW.tipe_elva = 'online' THEN
        
        IF NEW.metode_bayar_elva = 'COD' THEN
            SET NEW.status_pembayaran_elva = 'belum_bayar';
        ELSE
            SET NEW.status_pembayaran_elva = 'lunas';
        END IF;

    END IF;

    -- OFFLINE selalu lunas
    IF NEW.tipe_elva = 'offline' THEN
        SET NEW.status_pembayaran_elva = 'lunas';
    END IF;

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users_elva`
--

CREATE TABLE `users_elva` (
  `id_user_elva` int(11) NOT NULL,
  `nama_elva` varchar(100) DEFAULT NULL,
  `username_elva` varchar(50) DEFAULT NULL,
  `password_elva` varchar(255) DEFAULT NULL,
  `role_elva` enum('admin','kurir','kasir','customer') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_elva`
--

INSERT INTO `users_elva` (`id_user_elva`, `nama_elva`, `username_elva`, `password_elva`, `role_elva`) VALUES
(1, 'Elva Celia', 'elva', 'scrypt:32768:8:1$tMfcMPYCCj3Y9tH3$caa9011b21e2b0cb08b522e9b39c76bede59def7795f84a38cea8331eef5aebd5c42b443d0220568a409517af7d3cbb0bb4473b72346d4c1dfef85fe8619e7dd', 'customer'),
(2, 'administrator', 'admin', 'scrypt:32768:8:1$FgMcvR3gdJe3g4ym$e4ff615c92cf76da1bbac4c22fb477e18c37b9597322a2a5fd5018004bdb5ff6f11d656053f64f67406dfa6c8690952e77e00f5b087c187f952c8746b9e0ffd4', 'admin'),
(6, 'Arya Samsul', 'arya', 'scrypt:32768:8:1$ZqJu40271aMc6llN$6fefc2be4cbfe65684859e1ebe0a28b4669381fa379537b211beb0c6b2a96905e80ba07ace0e8eaec26e88fbdd3da8bebdc39a61559256b3effe9bcbb7eb272d', 'kasir'),
(7, 'Saepul Saepudin', 'saepul', 'scrypt:32768:8:1$oiP6m0XQutL7lwX3$461a185cf4ba6a38e03a5d0884da0444cfa39583b4d22c97eaff4f9b18cad9150b93329c242c9cf67e5b8090a78041a3673226308ceb955261bcec4d7a4c97b3', 'kurir'),
(9, 'Anisa Jaya Lestari', 'anisa', 'scrypt:32768:8:1$myzOZ0Zjqtz67I73$793329e110000e163f9b0395dba0a511c03024039a6a78e70e0449f72b146c8cae42710b755d158dfbebe3bf6f8deb6f77adf3dff15c929fbd4fe7372b757a04', 'customer'),
(10, 'novi', 'novi ropiah', 'scrypt:32768:8:1$GnK5I4mAyx6P0xni$f06591ebc88d188f21bb1f7c9a4a6f4175408b29565904698b570b10495c87756142f74c92944e08e58f8371e0a0d9cfe371c010aba34411b2c52e626ce082cb', 'customer'),
(11, 'sazkiya lutfiah', 'sazkiya', 'scrypt:32768:8:1$lJiN8DrUdy0FVewe$f3a3dac88bc5ba46f23df047897df5fbb081e2e0bfe59cba1e9e957aae5983f86fb5007bc5c61e3efb2455105ba7a5eedad8a520332593f5363f74ef6ae999d3', 'customer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dokter_elva`
--
ALTER TABLE `dokter_elva`
  ADD PRIMARY KEY (`id_dokter_elva`);

--
-- Indexes for table `gudang_elva`
--
ALTER TABLE `gudang_elva`
  ADD PRIMARY KEY (`id_gudang_elva`);

--
-- Indexes for table `kategori_elva`
--
ALTER TABLE `kategori_elva`
  ADD PRIMARY KEY (`id_kategori_elva`);

--
-- Indexes for table `obat_elva`
--
ALTER TABLE `obat_elva`
  ADD PRIMARY KEY (`id_obat_elva`),
  ADD KEY `id_gudang_elva` (`id_gudang_elva`),
  ADD KEY `fk_kategori_elva` (`kategori_id_elva`);

--
-- Indexes for table `pasien_elva`
--
ALTER TABLE `pasien_elva`
  ADD PRIMARY KEY (`id_pasien_elva`);

--
-- Indexes for table `pengiriman_elva`
--
ALTER TABLE `pengiriman_elva`
  ADD PRIMARY KEY (`id_pengiriman_elva`),
  ADD KEY `id_transaksi_elva` (`id_transaksi_elva`);

--
-- Indexes for table `racikan_elva`
--
ALTER TABLE `racikan_elva`
  ADD PRIMARY KEY (`id_racikan_elva`);

--
-- Indexes for table `resep_detail_elva`
--
ALTER TABLE `resep_detail_elva`
  ADD PRIMARY KEY (`id_detail_elva`),
  ADD KEY `id_resep_elva` (`id_resep_elva`),
  ADD KEY `id_obat_elva` (`id_obat_elva`),
  ADD KEY `id_racikan_elva` (`id_racikan_elva`);

--
-- Indexes for table `resep_elva`
--
ALTER TABLE `resep_elva`
  ADD PRIMARY KEY (`id_resep_elva`),
  ADD UNIQUE KEY `no_resep_elva` (`no_resep_elva`),
  ADD KEY `id_pasien_elva` (`id_pasien_elva`,`id_dokter_elva`,`id_transaksi_elva`),
  ADD KEY `fk_dokter` (`id_dokter_elva`),
  ADD KEY `fk_transaksi` (`id_transaksi_elva`);

--
-- Indexes for table `tracking_pengiriman_elva`
--
ALTER TABLE `tracking_pengiriman_elva`
  ADD PRIMARY KEY (`id_tracking`),
  ADD KEY `id_pengiriman_elva` (`id_pengiriman_elva`);

--
-- Indexes for table `transaksi_detail_elva`
--
ALTER TABLE `transaksi_detail_elva`
  ADD PRIMARY KEY (`id_detail_elva`),
  ADD KEY `id_transaksi_elva` (`id_transaksi_elva`),
  ADD KEY `id_obat_elva` (`id_obat_elva`),
  ADD KEY `fk_racikan` (`id_racikan_elva`);

--
-- Indexes for table `transaksi_elva`
--
ALTER TABLE `transaksi_elva`
  ADD PRIMARY KEY (`id_transaksi_elva`),
  ADD KEY `id_pasien_elva` (`id_pasien_elva`),
  ADD KEY `id_user_elva` (`id_user_elva`);

--
-- Indexes for table `users_elva`
--
ALTER TABLE `users_elva`
  ADD PRIMARY KEY (`id_user_elva`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dokter_elva`
--
ALTER TABLE `dokter_elva`
  MODIFY `id_dokter_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `gudang_elva`
--
ALTER TABLE `gudang_elva`
  MODIFY `id_gudang_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `kategori_elva`
--
ALTER TABLE `kategori_elva`
  MODIFY `id_kategori_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `obat_elva`
--
ALTER TABLE `obat_elva`
  MODIFY `id_obat_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=463;

--
-- AUTO_INCREMENT for table `pasien_elva`
--
ALTER TABLE `pasien_elva`
  MODIFY `id_pasien_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `pengiriman_elva`
--
ALTER TABLE `pengiriman_elva`
  MODIFY `id_pengiriman_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `racikan_elva`
--
ALTER TABLE `racikan_elva`
  MODIFY `id_racikan_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `resep_detail_elva`
--
ALTER TABLE `resep_detail_elva`
  MODIFY `id_detail_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `resep_elva`
--
ALTER TABLE `resep_elva`
  MODIFY `id_resep_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `tracking_pengiriman_elva`
--
ALTER TABLE `tracking_pengiriman_elva`
  MODIFY `id_tracking` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `transaksi_detail_elva`
--
ALTER TABLE `transaksi_detail_elva`
  MODIFY `id_detail_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=220;

--
-- AUTO_INCREMENT for table `transaksi_elva`
--
ALTER TABLE `transaksi_elva`
  MODIFY `id_transaksi_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT for table `users_elva`
--
ALTER TABLE `users_elva`
  MODIFY `id_user_elva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `obat_elva`
--
ALTER TABLE `obat_elva`
  ADD CONSTRAINT `fk_gudang` FOREIGN KEY (`id_gudang_elva`) REFERENCES `gudang_elva` (`id_gudang_elva`),
  ADD CONSTRAINT `fk_kategori_elva` FOREIGN KEY (`kategori_id_elva`) REFERENCES `kategori_elva` (`id_kategori_elva`),
  ADD CONSTRAINT `obat_elva_ibfk_1` FOREIGN KEY (`id_gudang_elva`) REFERENCES `gudang_elva` (`id_gudang_elva`);

--
-- Constraints for table `pengiriman_elva`
--
ALTER TABLE `pengiriman_elva`
  ADD CONSTRAINT `pengiriman_elva_ibfk_1` FOREIGN KEY (`id_transaksi_elva`) REFERENCES `transaksi_elva` (`id_transaksi_elva`);

--
-- Constraints for table `resep_detail_elva`
--
ALTER TABLE `resep_detail_elva`
  ADD CONSTRAINT `resep_detail_elva_ibfk_1` FOREIGN KEY (`id_resep_elva`) REFERENCES `resep_elva` (`id_resep_elva`),
  ADD CONSTRAINT `resep_detail_elva_ibfk_2` FOREIGN KEY (`id_obat_elva`) REFERENCES `obat_elva` (`id_obat_elva`),
  ADD CONSTRAINT `tbl_shipment_azka_ibfk_3` FOREIGN KEY (`id_racikan_elva`) REFERENCES `racikan_elva` (`id_racikan_elva`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
