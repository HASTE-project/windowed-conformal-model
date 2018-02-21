## Conformal Model for Predicting Interestingness of Microscopy Images based on Windowed Analysis of Image Features

- Intended for the HASTE Storage Client (https://github.com/HASTE-project/HasteStorageClient)
- Analyzes a window of microscopy images for a well-substream
- Queries the HASTE feature database (MongoDB) to retrieve those features
- Performs conformal prediction based on image features
- Applies specified confidence level to return a binary decision.

## Usage:

See `example.py`

## Installation:

```
$ pip3 install git+ssh://git@github.com/HASTE-project/windowed-conformal-model.git@master
```

or 

```
git clone https://github.com/HASTE-project/windowed-conformal-model.git
cd windowed-conformal-model
pip3 install -e .
```

## Contributors

Ben Blamey