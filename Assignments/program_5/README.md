Hello.
To use the following files, here are some helpeful tips and commands:

The data used is stored in the database files folder, in the program_5 folder.
They are zipped in the geojson_TeacherDB_Files and are in geo.json format.
I have included two text files here that displays commands on importing the
data to a MongoDB server.



Query1
This python program can be run from the gitbash commandline with:

python query1.py [query_radius] > airport_test.txt

python query1.py 500 > airport_test.txt

This will execute query1 where [query_radius] is the search radius
you would like to use in miles, while > airport_text.txt will create
or overwrite a file in the program_5 folder that will display information
regarding mouseclicks, starting and destination airports, as well as counting
down the miles for each airport listed by city,country and acronym along the
way until the destination is reached. A screenshot image will be generated
upon completion of processing and is saved as "screen_shot_query1.png".
NOTE: This query will take sometime to process the data, normally I would
mouse over the close or exit button on the pygame screen and when it would
light up and be available to click I would do so knowing that the data had been
processed.



Query2
This python program can be run from the gitbash commandline with:

python query2.py [query_radius]

python query2.py [feature] [field] [field_value] [min/max] [# of results] [query_radius]

python query2.py 100

The above command will display upon mouseclick on the pygame screen, all volcanos, earthquakes,
and meteorites in an area of 100 miles where clicked up to a value of 500 points plotted.
Volcanos in red, earthquakes in blue, and meteorites in green. They will then vanish after a few
seconds, though a screenshot will be captured and saved as "screen_shot_query2.png".

python query2.py earthquakes mag 7 min 10 200

python query2.py meteroites year 1990 min 30 300

The above commands are sample queries that will show:
Earthquakes with a magnitude of 7 minimum, 10 results if that many, in a 200 mile search radius upon click
Meteorites from the year 1990, 30 results if that many, in a 300 mile search radius.
Both of these will show for a few seconds, be screen captured like above and saved as the same file name.
In the file itself, when setting sys.argv[x] to variables there are more available fields to choose from.


Query3
This python program can be run from the gitbash commandline with:

python query3.py [feature] [min_pts] [eps]

python query3.py volcanos 5 15

The above command will display a pygame screen showing all of the volcanos in the data base
plotted onto a world map image. It will then show three bounding rectangles highlighting the
most densely packed or clustered areas of volcanos. A screenshot will be taken of this and
saved as "screen_shot_query3.png".

