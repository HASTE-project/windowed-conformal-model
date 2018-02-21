Model intended for the HASTE Storage Client (https://github.com/HASTE-project/HasteStorageClient)

- Analyzes a window of microscopy images for a well-substream
- Queries MongoDB feature database to retrieve those features
- Performs conformal prediction based on image features
- Applies specified confidence level to return a binary decision.

Usage:

See `example.py`

Installation:

```
$ pip3 install git+ssh://git@github.com/HASTE-project/windowed_conformal_model.git@master
```