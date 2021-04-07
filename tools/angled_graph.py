from manim import *

class AngledGraph():
    def __init__(self, vertices_input, edges_input):
        """ The constructor assigns the vertices and edges of the angled graph so 
        that it is ready to be added to a scene. The vertices and edges are 
        stored as MObjects.The vertices are created by the 
        label(string)-coordinates(float, float) dictionary passed in by the 
        user. Internally, these will be stored as a dictionary of the form 
        label(string)-vertex(MObject). The edges are designated by the user 
        with a list of pairs of labels. The labels correspond to the vertexes 
        that the edge joins. Internally, this is stored as a 
        labelpair(String, String)-line(MObject) dictionary.
        For convenience the edges and vertices are grouped together with 
        an instance variable. """

        self.image = VGroup()
        self.vertices = {}
        self.edges = {}
        #group of all angles that are displayed on screen
        self.angleImage = VGroup()
        #mappings of angles from the edges they are about
        self.angles = {}

        for (vertex_label, coordinates) in vertices_input.items():
            right_sf = coordinates[0]
            up_sf = coordinates[1]
            new_dot = Dot(RIGHT*right_sf+UP*up_sf)
            self.vertices[vertex_label] = new_dot
            self.image += new_dot

        for (vertex1_label, vertex2_label) in edges_input:
            new_line = Line (
                self.vertices[vertex1_label].get_center(), 
                self.vertices[vertex2_label].get_center()
            )
            self.edges[(vertex1_label, vertex2_label)] = new_line
            self.image += new_line

    def add(self, input_scene):
        # This method takes the given scene and writes all the vertices and 
        # edges to it - non-animated.

        input_scene.add(self.image)

    def remove(self, input_scene):
        # This method takes the given scene and removes the overall image of all 
        # vertices and edges from it - non-animated.

        input_scene.remove(self.image)

    @staticmethod
    def generate_edge(edge, vertex1, vertex2):
        new_start = edge.start if vertex1 is None else vertex1.get_center()
        new_end = edge.end if vertex2 is None else vertex2.get_center()
        
        new_line = Line(
            new_start,
            new_end
        )

        new_line.set_start_and_end_attrs(new_start,new_end)
        return new_line

    def update_with_vertex_end(self, vertex):
        #Update function for a line based on a vertex. Updates the end of the 
        #line based on the vertex.
        
        return lambda line : line.put_start_and_end_on(line.start, vertex.get_center())

    def update_with_vertex_start(self, vertex):
        #Update function for a line based on a vertex. Updates the start of the 
        #line based on the vertex.
    
        return lambda line : line.put_start_and_end_on(vertex.get_center(), line.end)

    def update_with_vertices_both(self, vertex1, vertex2):
        # Updates both the start and the end of the line with the given vertices. 
        # The first vertex is used to update the start and the second vertex is 
        # used to update the end.

        return lambda line : line.put_start_and_end_on(vertex1.get_center(), vertex2.get_center())

    def update_with_vertices(self, vertices):
        #Update function for a line based on a vertex. A value is given as an 
        #argument along with the vertex in order to indicate whether the start 
        #or end of the line should be dependent on the vertex. 0 indicates the 
        #start of the line should be dependent on the vertex and 1 indicates 
        #the end of the line should be dependent on the vertex
        
        # if vertices[0] is None:
        #     #only updated on one vertex, second element, for its end
        #     return self.update_with_vertex_end(vertices[1])
        # elif vertices[1] is None:
        #     #only updated on one vertex, first element, for its start
        #     return self.update_with_vertex_start(vertices[0])
        # else:
        #     #Updated on both vertices. The first element updates its start and 
        #     #the second element updates its end.
        #     return self.update_with_vertices_both(vertices[0],vertices[1])
            
        return lambda line : line.become(AngledGraph.generate_edge(line,vertices[0],vertices[1]))

    def update_for_angle(self, edge1, edge2, intersection_vertex):
        #returns a function to update an angle based on the given parameters
        return lambda angle : angle.become(AngledGraph.generate_angle_arc(edge1, edge2, intersection_vertex))

    def move_vertex(self, input_scene, vertex_label, new_coordinates):
        # This method takes the given scene (first argument) and moves 
        # the vertex corresponding the label (second argument) to the 
        # new coordinates (third arguments). The coordinates are specified 
        # in the form of a tuple of numbers (int/float/..).

        #final coordinates
        right_sf = new_coordinates[0]
        up_sf = new_coordinates[1]

        #identify MObject corresponding to the vertex that is going to be 
        #moved
        vertex = self.vertices[vertex_label]

        #generate the animations required to move the vertex - this includes
        #the animations for the vertex and edges
        animations = []
        animations.append(vertex.animate.move_to(np.array([right_sf,up_sf,0])))

        for labels, line in self.edges.items():
            if labels[0] == vertex_label:
                animations.append(
                    UpdateFromFunc(
                        mobject = line,
                        update_function = lambda line : line.put_start_and_end_on(vertex.get_center(), line.end)
                    )
                )
            elif labels[1] == vertex_label:
                animations.append(
                    UpdateFromFunc(
                        mobject = line,
                        update_function = lambda line : line.put_start_and_end_on(line.start, vertex.get_center())
                    )
                )

        #finally perform
        input_scene.play(
            *animations
        )

    def move_vertices(self, input_scene, **movements):
        # This functions takes the given scene (first argument) and moves some 
        # given vertices to the given coordinates. The vertices and their 
        # corresponding coordinates to be moved to are passed in as keyword 
        # arguments which map vertex labels to coordinates.
        
        #List of animations to move the vertices - this consists of 
        #vertex and edge animations.
        animations = []

        edge_mappings = {} 

        #consider each vertex and the corresponding coordinates that it should 
        #be moved to
        for (vertex_label, new_coordinates) in movements.items():
            #final coordinates
            right_sf = new_coordinates[0]
            up_sf = new_coordinates[1]

            #Identify VMObject corresponding to the vertex that is going to 
            #be moved
            vertex = self.vertices[vertex_label]

            #consider vertex animation
            animations.append(
                vertex.animate.move_to(np.array([right_sf,up_sf,0]))
            )

            #Dictionary that maps edges to the pair of vertices they are 
            #updated with. The first vertex corresponds to the start of the 
            # edge and the second vertex corresponds to the end of the edge.

            #consider attached edge animations
            for labels,line in self.edges.items():
                if labels[0] == vertex_label:
                    if line in edge_mappings.keys():
                        #already updated based on one vertex - preserve this
                        prev = edge_mappings[line][1]
                        edge_mappings[line] = (vertex,prev)
                    else:
                        #otherwise
                        edge_mappings[line] = (vertex,self.vertices[labels[1]])
                elif labels[1] == vertex_label:
                    if line in edge_mappings.keys():
                        #already updated based on one vertex - preserve this
                        prev = edge_mappings[line][0]
                        edge_mappings[line] = (prev,vertex)
                    else:
                        #otherwise
                        edge_mappings[line] = (self.vertices[labels[0]],vertex)
        
        #consider how each edge should be updated based on how many and which 
        #vertices it is related to
        for line,vertices in edge_mappings.items():
            animations.append(
                UpdateFromFunc(
                    mobject = line,
                    update_function = self.update_with_vertices(vertices)
                )
            )    

        ##
        
        
        # animations.append(
        #                 UpdateFromFunc(
        #                     mobject = line,
        #                     update_function = self.update_with_vertex(vertex,1)
        #                 )
        # )
        ##

        for (edge1,edge2,intersection_vertex),angle in self.angles.items():
            animations.append(
                UpdateFromFunc(
                    mobject = angle,
                    update_function = self.update_for_angle(edge1,edge2,intersection_vertex)
                )
            )

        #finally perform the animations to move the vertices
        input_scene.play(
            *animations
        )

    def remove_angles(self, input_scene):
        #Method to remove all angle images from the given scene
        input_scene.remove(self.angleImage)
        self.angleImage = VGroup()
        self.angles = {}

    @staticmethod
    def generate_angle_arc(edge1, edge2, intersection_vertex):
        #generates the image to show an angle

        #Determine the intersection point of the two edges which the angle 
        #will be centered about
        intersection_point = intersection_vertex.get_center()

        #Determine the angle of the two edges away from the intersection
        edge1_angle = angle_of_vector(edge1.get_start() - edge1.get_end())
        edge2_angle = edge2.get_angle()

        #Determine the start angle, end angle and angle magnitude
        start = min(edge1_angle,edge2_angle)
        end = max(edge1_angle,edge2_angle)
        magnitude = end - start

        return Arc(
            arc_center = intersection_point,
            radius = 0.3,
            start_angle = start,
            angle = magnitude
        )

    def add_angles(self, input_scene, angles):
        # Method to add all the given angles to the scene. Angles are passed into 
        # this function with a dictionary where the keys represent the pair of 
        # edges the angle is between and the value is used to alternate which 
        # angle between the edges is shown (with 0 or 1). The edges are given 
        # with their corresponding pair of vertices. 

        #Remove previous angles so that only the current angles are retained
        self.remove_angles(input_scene)

        # Iterate through the passed in dictionary to consider each angle
        for givenEdges,av in angles.items():
            #create the actual angle
            edge1 = self.edges[givenEdges[0]]
            edge2 = self.edges[givenEdges[1]]
            intersection_vertex = self.vertices[givenEdges[0][1]]
            new_angle = AngledGraph.generate_angle_arc(edge1, edge2, intersection_vertex)
            self.angles[(edge1,edge2,intersection_vertex)] = new_angle
            self.angleImage += new_angle

        # Finally, add the angles to the scene
        input_scene.add(self.angleImage)
    

class AngledGraphTest(Scene):
    def construct(self):
        #example code demonstrating the angled graph

        #defining vertices
        initial_vertices = {"A" : (0,0), "B" : (0,1), "C" : (1,1), "D" : (1,0)}

        #defining edges
        initial_edges = {("A","B"), ("B","C"), ("C","D"), ("D","A")}

        #creates underlying representation
        my_angled_graph = AngledGraph(initial_vertices, initial_edges)
        my_angled_graph.add(self) 
        self.wait()

        #adding angles test
        my_angled_graph.add_angles(
            self, 
            {
                (("A","B"),("B","C")) : 0,
                (("B","C"),("C","D")) : 0,
                (("C","D"),("D","A")) : 0,
                (("D","A"),("A","B")) : 0,
            }
        )
        self.wait()

        #moving a single vertex test
        # my_angled_graph.move_vertex(self, "A", (-1,-1))
        # self.wait()

        #moving multiple vertices test
        my_angled_graph.move_vertices(self, A = (-1,-1), B = (-1,0))
        self.wait()

        my_angled_graph.move_vertices(self, C = (0,0), D = (0,-1))
        self.wait()