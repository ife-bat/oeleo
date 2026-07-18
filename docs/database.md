# Database

The bookkeeping database contains one table called `filelist`:

| id  | processed_date             | local_name         | external_name                         | checksum                         | code |
|-----|:---------------------------|:-------------------|:--------------------------------------|:---------------------------------|-----:|
| 1   | 2022-07-05 15:55:02.521154 | file_number_1.xyz  | C:\oeleo\check\to\file_number_1.xyz   | c976e564825667d7c11ba200457af263 |    1 |
| 2   | 2022-07-05 15:55:02.536152 | file_number_10.xyz | C:\oeleo\check\to\file_number_10.xyz  | d502512c0d32d7503feb3fd3dd287376 |    1 |
| 3   | 2022-07-05 15:55:02.553157 | file_number_2.xyz  | C:\oeleo\check\to\file_number_2.xyz   | cb89d576f5bd57566c78247892baffa3 |    1 |

`processed_date` is when the file was last updated (the last time `oeleo` found a new checksum for it).

## Status codes

| code | meaning                       |
|:-----|:------------------------------|
| 0    | `should-be-copied`            |
| 1    | `should-be-copied-if-changed` |
| 2    | `should-not-be-copied`        |

You can **lock** a file (never copy it) by setting `code` to `2` manually.
