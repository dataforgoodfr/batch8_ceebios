# Ceebios x Data For Good x Museum d'Histoire Naturelle


## About this project

This repository has been created throughout Data For Good season 8 for a great project which aims to allow for an easier 
and nicer search and visualization of animal species in the biomimicry field.

## Repository architecture

```bash
├── data/                   # Data extracts from GBIF, MNHN
├── notebooks/              # Exploratory jupyter notebooks
├── batch8_ceebios/         # Python main module of this repository: clean GBIF taxon & Semantic Scholar, add all articles to MongoDB
├── gbif_modules_data/      # Python module used to clean some GBIF database 
├── lib/                    # Python library for multiprocessing
├── fastapi-api/            # Fast API connected to MongoDB
├── requirements.txt        # Project requirements
├── LICENSE
└── README.md
```


## Fast API

For more information on `fastapi-api` see its own `README.md` in the corresponding folder.

## Licence

MIT License, for more details, see `LICENCE`.
