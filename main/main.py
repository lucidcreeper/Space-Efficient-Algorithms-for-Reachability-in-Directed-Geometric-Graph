from asyncio.windows_events import NULL
import graphlib
from queue import PriorityQueue
from flask import *

app = Flask(__name__)

#graph part
class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []
    
    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight
    
def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D

g = Graph(9)
g.add_edge(0, 1, 4)
g.add_edge(0, 6, 7)
g.add_edge(1, 6, 11)
g.add_edge(1, 7, 20)
g.add_edge(1, 2, 9)
g.add_edge(2, 3, 6)
g.add_edge(2, 4, 2)
g.add_edge(3, 4, 10)
g.add_edge(3, 5, 5)
g.add_edge(4, 5, 15)
g.add_edge(4, 7, 1)
g.add_edge(4, 8, 5)
g.add_edge(5, 8, 12)
g.add_edge(6, 7, 1)
g.add_edge(7, 8, 3) 

@app.route("/")
def index():
     return render_template("index.html");

@app.route("/start")
def start():
     return render_template("start.html");

@app.route("/saveDetails", methods=["POST", "GET"])
def saveDetails():
    if request.method == "POST":
        try:
            start = request.form["startingnode"]
            print(start)
            D = dijkstra(g, int(start))
            msg = ""
            for vertex in range(len(D)):
                msg = msg + "Distance from vertex 0 to vertex"+str(vertex)+"is"+str(D[vertex])+"\n\n\n"
        except:
            msg = "counldnt start"
        finally:
            return render_template("suc.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
