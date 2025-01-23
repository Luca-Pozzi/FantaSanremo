# FantaSanremo

A simple Python script to extract best (and worst) possible teams of the [FantaSanremo](https://fantasanremo.com/), the Festival di Sanremo fantasy game.

## How to use
* Clone the repo, and `cd` into it.
* In the terminal, switch to the branch of the desired Sanremo edition (`fs2024` and `fs2025` are available):
```
git checkout <year>
```
* Have a look at the existing `FANTASANREPORT<year>.md` report ([`FANTASANREPORT2024.md`](./FANTASANREPORT2024.md) for the current branch) where you can find a summary of the stats regarding the selected edition.

To modify/extend/complement the info in the report, edit the [`fantasanremo.py`](./fantasanremo.py) script and re-generate the report as follows.

* Run the main script with:
```
python fantasanremo.py
```
* Check again the `FANTASANREPORT<year>.md` file to the updated report.

## Authors
* Luca ✉️ [luca6.pozzi@mail.polimi.it](mailto:luca6.pozzi@mail.polimi.it)
