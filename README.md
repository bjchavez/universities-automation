# Number of digitized and published theses by the universities of Perú.

## Description

This repository contains a dataset of digitized and published theses by the main universities of Perú.

## Why?

The data has been extracted from their institutional repositories with the purpose of serving as a reference, supporting, or
initiating academic and social research.

## List of universities and their repositories

| University | Acronym | Repository |
| ----------  | ------ | ----------- |
| Universidad Nacional Mayor de San Marcos | UNMSM | [https://cybertesis.unmsm.edu.pe/] |
| Universidad Nacional José Faustino Sánchez Carrión | UNJFSC | [https://repositorio.unjfsc.edu.pe/] |
| Universidad Nacional de Ingenieria | UNI | [https://cybertesis.uni.edu.pe/] |
| Universidad Nacional Agraria La Molina | UNALM | [https://repositorio.lamolina.edu.pe/] |
| Universidad Nacional San Cristobal de Huamanga | UNSCH | [http://repositorio.unsch.edu.pe/] |
| Universidad Científica del Sur | UCS | [https://repositorio.cientifica.edu.pe/] |
| Universidad César Vallejo | UCV | [https://repositorio.ucv.edu.pe/] |
| Universidad San Antonio Abad del Cusco | UNSAAC | [https://repositorio.unsaac.edu.pe/] |
| Pontificia Universidad Católica del Perú | PUCP | [https://repositorio.pucp.edu.pe/index/] |
| Universidad Nacional del Centro del Perú | UNCP | [https://repositorio.uncp.edu.pe/] |

## Folders and files

```

├── /bachelor_degree        # Contains a list of .py files for Peruvian universities
├── get_bachelors.py        # Main file with calls to the 'get' methods of universities
├── README.md               # Readme file
├── /tests                  # Test folders(test_pucp_bachelor)

```

## Usage

First, you must update the CSV files, in the project root, run:

```bash

python3 get_bachelors.py

```

Then, in the folder 'bachelor_degree/datasets', you will find all the updated CSV files.

```
├── PUCP_BACHELOR.csv
├── UCS_BACHELOR.csv
├── UCV_BACHELOR.csv
├── UNALM_BACHELOR.csv
├── UNI_BACHELOR.csv
├── UNJFSC_BACHELOR.csv
├── UNMSM_BACHELOR.csv
├── UNSAAC_BACHELOR.csv
├── UNSCH_BACHELOR.csv
```

## Technologies Used

- Python
- BeautifulSoup
- lxml

## Licence

MIT Licence
