=== First 5 rows ===
| Area        | Item   | Element   |   Year | Unit   |            Value |
|:------------|:-------|:----------|-------:|:-------|-----------------:|
| Afghanistan | Asses  | Stocks    |   1961 | Head   |      1.3e+06     |
| Afghanistan | Asses  | Stocks    |   1962 | Head   | 851850           |
| Afghanistan | Asses  | Stocks    |   1963 | Head   |      1.00111e+06 |
| Afghanistan | Asses  | Stocks    |   1964 | Head   |      1.15e+06    |
| Afghanistan | Asses  | Stocks    |   1965 | Head   |      1.3e+06     |

=== Summary statistics ===
|       |      Year |            Value |
|:------|----------:|-----------------:|
| count | 122458    | 120194           |
| mean  |   1991.38 |      1.0356e+07  |
| std   |     17.26 |      5.86939e+07 |
| min   |   1961    |      0           |
| 25%   |   1976    |   5300           |
| 50%   |   1992    | 102174           |
| 75%   |   2006    |      1.56157e+06 |
| max   |   2020    |      1.52594e+09 |

=== Data types ===
| Column   | Dtype   |
|:---------|:--------|
| Area     | object  |
| Item     | object  |
| Element  | object  |
| Year     | int64   |
| Unit     | object  |
| Value    | float64 |

=== Missing values ===
| Column   |   Missing count |   Missing % |
|:---------|----------------:|------------:|
| Area     |               0 |        0    |
| Item     |               0 |        0    |
| Element  |               0 |        0    |
| Year     |               0 |        0    |
| Unit     |               0 |        0    |
| Value    |            2264 |        1.85 |

=== Unique values per categorical column ===
| Column   |   Unique count |
|:---------|---------------:|
| Area     |            243 |
| Item     |             14 |
| Element  |              1 |
| Unit     |              3 |

=== Outlier summary (IQR method) ===
| Metric        |           Value |
|:--------------|----------------:|
| Q1            |  5300           |
| Q3            |     1.56157e+06 |
| IQR           |     1.55627e+06 |
| Lower bound   |    -2.32911e+06 |
| Upper bound   |     3.89598e+06 |
| Outlier count | 21030           |
| Outlier %     |    17.17        |