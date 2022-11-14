from nrarfcn.tables.Table import Table


def table_bands_fr1() -> Table:
    table_id = 'bands_fr1'
    table_release_3gpp = 17
    table_ts = "3GPP TS 38.104 V17.6.0"
    table_name = "Table 5.2-1: NR operating bands in FR1"
    table_header = ['band', 'f_ul_low', 'f_ul_high', 'f_dl_low', 'f_dl_high', 'duplex_mode']
    table_data = [
        ['n1', 1920, 1980, 2110, 2170, 'FDD'],
        ['n2', 1850, 1910, 1930, 1990, 'FDD'],
        ['n3', 1710, 1785, 1805, 1880, 'FDD'],
        ['n5', 824, 849, 869, 894, 'FDD'],
        ['n7', 2500, 2570, 2620, 2690, 'FDD'],
        ['n8', 880, 915, 925, 960, 'FDD'],
        ['n12', 699, 716, 729, 746, 'FDD'],
        ['n13', 777, 787, 746, 756, 'FDD'],
        ['n14', 788, 798, 758, 768, 'FDD'],
        ['n18', 815, 830, 860, 875, 'FDD'],
        ['n20', 832, 862, 791, 821, 'FDD'],
        ['n24', 1626.5, 1660.5, 1525, 1559, 'FDD'],
        ['n25', 1850, 1915, 1930, 1995, 'FDD'],
        ['n26', 814, 849, 859, 894, 'FDD'],
        ['n28', 703, 748, 758, 803, 'FDD'],
        ['n29', 'N/A', 'N/A', 717, 728, 'SDL'],
        ['n30', 2305, 2315, 2350, 2360, 'FDD'],
        ['n34', 2010, 2025, 2010, 2025, 'TDD'],
        ['n38', 2570, 2620, 2570, 2620, 'TDD'],
        ['n39', 1880, 1920, 1880, 1920, 'TDD'],
        ['n40', 2300, 2400, 2300, 2400, 'TDD'],
        ['n41', 2496, 2690, 2496, 2690, 'TDD'],
        ['n46', 5150, 5925, 5150, 5925, 'TDD'],
        ['n48', 3550, 3700, 3550, 3700, 'TDD'],
        ['n50', 1432, 1517, 1432, 1517, 'TDD'],
        ['n51', 1427, 1432, 1427, 1432, 'TDD'],
        ['n53', 2483.5, 2495, 2483.5, 2495, 'TDD'],
        ['n65', 1920, 2010, 2110, 2200, 'FDD'],
        ['n66', 1710, 1780, 2110, 2200, 'FDD'],
        ['n67', 'N/A', 'N/A', 738, 758, 'SDL'],
        ['n70', 1695, 1710, 1995, 2020, 'FDD'],
        ['n71', 663, 698, 617, 652, 'FDD'],
        ['n74', 1427, 1470, 1475, 1518, 'FDD'],
        ['n75', 'N/A', 'N/A', 1432, 1517, 'SDL'],
        ['n76', 'N/A', 'N/A', 1427, 1432, 'SDL'],
        ['n77', 3300, 4200, 3300, 4200, 'TDD'],
        ['n78', 3300, 3800, 3300, 3800, 'TDD'],
        ['n79', 4400, 5000, 4400, 5000, 'TDD'],
        ['n80', 1710, 1785, 'N/A', 'N/A', 'SUL'],
        ['n81', 880, 915, 'N/A', 'N/A', 'SUL'],
        ['n82', 832, 862, 'N/A', 'N/A', 'SUL'],
        ['n83', 703, 748, 'N/A', 'N/A', 'SUL'],
        ['n84', 1920, 1980, 'N/A', 'N/A', 'SUL'],
        ['n85', 698, 716, 728, 746, 'FDD'],
        ['n86', 1710, 1780, 'N/A', 'N/A', 'SUL'],
        ['n89', 824, 849, 'N/A', 'N/A', 'SUL'],
        ['n90', 2496, 2690, 2496, 2690, 'TDD'],
        ['n91', 832, 862, 1427, 1432, 'FDD'],
        ['n92', 832, 862, 1432, 1517, 'FDD'],
        ['n93', 880, 915, 1427, 1432, 'FDD'],
        ['n94', 880, 915, 1432, 1517, 'FDD'],
        ['n95', 2010, 2025, 'N/A', 'N/A', 'SUL'],
        ['n96', 5925, 7125, 5925, 7125, 'TDD'],
        ['n97', 2300, 2400, 'N/A', 'N/A', 'SUL'],
        ['n98', 1880, 1920, 'N/A', 'N/A', 'SUL'],
        ['n99', 1626.5, 1660.5, 'N/A', 'N/A', 'SUL'],
        ['n100', 874.4, 880, 919.4, 925, 'FDD'],
        ['n101', 1900, 1910, 1900, 1910, 'TDD'],
        ['n102', 5925, 6425, 5925, 6425, 'TDD'],
        ['n104', 6425, 7125, 6425, 7125, 'TDD']
    ]

    return Table(table_id, table_release_3gpp, table_ts, table_name, table_header, table_data)
