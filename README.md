# Game_of_breakthrough

Python 3.6.1 :: Anaconda 4.4.0

#### Have virtualenv installed, if not:
$ conda install virtualenv                                                                                                               


#### Create a virtualenv (right outside of "kanye_album"):
$ virtualenv env_name

- some_dir/
   - env_name/
   - Game_of_breakthrough/
      - requirements.txt

#### Activate virtualenv:
$ source activate env_name


#### Now cd into kanye_album and run (this installs all the packages into your virtualenv):
$ pip install -r requirements.txt


#### Once all packages are installed simply run the following to get the server running:
$ python main.py

#### The results will be displayed. To change game settings, update the 'action' decisions in main.py file.
