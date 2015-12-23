Optimor Coding Test
===================

A Python/Selenium script to report the calling tariffs for a range of O2 Pay Monthly contracts.

## How to run

1. Ensure you have Python 2.7 and recent version of Firefox installed (the script depends on Firefox to run).
2. Initialize a virtualenv using `virtualenv env` then `source env/bin/activate` (`env\Scripts\activate` on Windows).  The `env` folder is in the `.gitignore` so it's recommended you use the name `env` for your virtualenv folder.  If the `virtualenv` command fails you might need to install it using `pip install virtualenv`.
3. `pip install -r requirements.txt` to install the dependencies.
4. [Optional] Run the tests using `py.test tests.py`.
5. Run `python app.py`.  The results will be printed in the terminal.
