# plantnet

Retrives the list of NSW Flora providing its Family (Subfamily), scientific name and common name.

```
pdm sync
pdm run python ./plantnet.py
```
The HTTP get request takes a 2 second delay to avoid spamming the website.
Output is stored as a excel compatible CSV called `out.csv`
