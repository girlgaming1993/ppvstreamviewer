if you want to remake .exe on windows:

make sure you have python installed (currently using 3.13.7 for this)
CMD in folder with app.py in it:
  py -m pip install --upgrade pip
  py -m pip install flask requests pyinstaller
  py -m PyInstaller app.py --name StreamsViewer --onefile --add-data "templates;templates"

then use .exe in "dist\StreamsViewer.exe"




IN CASE OF ERRORS:::

-make sure the website (ppv.to) is up, if not, look for alternative ppv site
-make sure port 5000 is open
thats all i got lol
