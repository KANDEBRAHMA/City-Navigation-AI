# City-Navigation-AI
Implemented a Google Maps prototype that provides the shortest route in terms of distance, the fastest route, the route with the fewest turns, and a scenic route that avoids roads when provided a source and destination. The algorithms used were DFS, BFS, A*, and Iterative Depth First Search.

## Approach to Road trip!

<h3>Abstraction:</h3>
<u><b>Set of Valid states</b></u>: Set of all probable segments which has routes in road-segments file.<br><br>
<u><b>Successor Function</b></u>: Set of all possible segments has route from city1 which consists of parameters such as <b>distance,speedlimit,city1,city2,highwayname</b><br>
After generating all the successor routes we calculate the heuristic_score and cost_function for specified cost_attribute.<br><br>
<u><b>Cost Function</b></u>: We have four cost functions such as:
<br><ol><li>
    <b>Segments:</b>The cost for this is uniform 1 since we have only one edge from city1 to city2.
</li>
<li>
    <b>Distance:</b> The cost for this is the distance between city1 and city2 which is specified in road-segments file.
</li>
<li>
    <b>Time:</b> The cost for this is the time taken to travel from city1 to city2 which is evaluated by distance divided by speed_limit provided in road-segmensts file.
</li>
<li>
    <b>Delivery:</b> The cost for this is the time taken to deliver a product from city1 to city2. This will be evaluated by following conditions.
    <ul>
        <li>If the speed_limit is above 50 then there is 5% chance of falling out of the truck and the product gets damaged. So, while using this the probability of mistake is calculated as tanh(distance/1000)</li>
        <li>So the time taken would incrase by two times because he has to go back to start city and pick the product.</li>
        <li>If the speed_limit is less than 50 then there is no extra time_taken to deliver the product.</li>
    </ul>
</li>
</ol>
<br>
<u><b>Goal State</b></u>: Reaching end city on shortest possible cost function which will be specified by the user.<br><br>
<u><b>Initial State</b></u>: Initial state is the start city provided by the user.<br><br>
<u><b>Heuristic Functions</b></u>: Finding distance using latitude and longitude from current city to destination city which are provided in city-gps file.
For some of the cities, langitudes and longitudes are missing so for the city which is missing we are considering the heuristic score of the previous city and adding to to the current path distance which will be used as current city's heuristic score.
<br>
<i><h3>Description of Algorithm:</h3></i>
Implemented using A<sup>*</sup> algorithm with an heuristic and specified cost function.
<ol>
<li>Intially by using pandas module loading all the data from specified files to get road-segments and gps details and converting them to lists for better accessing. As mentioned, including the bidirectional condition as well.</li>
<li>Calculating the time taken for all segments and mistakes for delivery cost function and adding to the list.</li>
<li>Adding the start city into the frontier(fringe)</li>
<li>Maintaing explored routes which is empty at the initial point.</li>
<li>Looping till the frontier is not empty:</li>
<ol><li>Pop the latest city using heappop method in heapq module which gives the minheap board which has less f_score.</li>
<li>Checking whether the board popped is the destination city. If yes, the return and print the segments, distance travelled, time taken and delivery.</li>
<li>Otherwise, add this segment to explored list</li>
<li>Generate all the successors segments for this current_city.</li>

<ol>
<li>For each successor route, calculates the F_score which is the sum of heuristic score and cost function based on cost_attribute.</li>
<li>If the successor route is not in explored and not in frontier, then heappush the board into frontier with f_score of travelled route.</li>
</ol></ol>

</ol></ol><br>