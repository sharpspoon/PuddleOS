# PuddleOS

## How To Run
Listed below are two options to access the application.
1. Navigate to https://puddle-os.herokuapp.com
2. Follow the "Local Install Guide" below.

## Local Install Guide
1. Clone the repository locally.
2. Open a terminal as Admin/root.
3. Change to the root directory of PuddleOS.
4. Assuming Python 3 and `pip` is installed, run `pip install -r requirements.txt`. 
   This will install all the necessary libraries.
5. Now set the Flask environment variable. 
- Unix
`export FLASK_APP=app`
- Windows
`C:\path\to\app>set FLASK_APP=app.py`
- PowerShell
`PS C:\path\to\app> $env:FLASK_APP = "app.py"`
6. Run `python -m flask run`
7. The application should now be running under 127.0.0.1:5000

## User Guide
1. Settings
   1. Display - Toggle this to display or hide nodes within the specific layer
   2. Clustering Method - Select the desired clustering method for the specific layer
      1. Agglomerative Complete Linkage Hierarchical Clustering
2. Graph - Graphical representation of the nodes and Puddles.
3. Node Data - This is a dump of the JSON node data.
4. Link Data - This is a dump of the JSON link data.
5. Log - This is a table with data relating to the last run.
   1. id - The id of the node.
   2. target id - The id of the target node.
   3. px - The previous node x-axis location.
   4. py - The previous node y-axis location.
   5. pz - The previous node z-axis location.
   6. xa - The current node x-axis location.
   7. ya - The current node y-axis location.
   8. za - The current node z-axis location.
   9. xb - The target node x-axis location.
   10. yb - The target node y-axis location.
   11. zb - The target node z-axis location.
   12. dst - The distance from the current node to the target node.
   13. best dst - The current shortest distance for the current node.
   14. best dst id - The id of the best dst node.

## To-Do
Please review the "Issues" page for this repo.

## Contact
Robin Ward - rcw0024@auburn.edu

Matthew Freestone - maf0083@auburn.edu