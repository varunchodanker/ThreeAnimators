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
        self.angles = VGroup()

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
                # .add_updater(lambda mobj, dt : 
                #     mobj.put_start_and_end_on(
                #         self.vertices[vertex1_label].get_center(), 
                #         self.vertices[vertex2_label].get_center()
                #     )
                # )
                #always_redraw(lambda : )
    
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

        #create target instance for final position
        vertex.generate_target()
        vertex.target.move_to(RIGHT*right_sf+UP*up_sf)

        #generate the animations required to move the vertex - this includes
        #the animations for the vertex and edges
        animations = []
        animations.append(MoveToTarget(vertex))

        for labels, line in self.edges.items():
            if labels[0] == vertex_label:
                line.generate_target()
                line.target.put_start_and_end_on(RIGHT*right_sf+UP*up_sf, line.end)
                animations.append(MoveToTarget(line))
            elif labels[1] == vertex_label:
                line.generate_target()
                line.target.put_start_and_end_on(line.start, RIGHT*right_sf+UP*up_sf)
                animations.append(MoveToTarget(line))

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

        #generate targets for each edge
        for line in self.edges.values():
            line.generate_target()

        #consider each vertex and the corresponding coordinates that it should 
        #be moved to
        for (vertex_label, new_coordinates) in movements.items():
            #final coordinates
            right_sf = new_coordinates[0]
            up_sf = new_coordinates[1]

            #Identify VMObject corresponding to the vertex that is going to 
            #be moved
            vertex = self.vertices[vertex_label]

            #create target instance for the final position
            vertex.generate_target()
            vertex.target.move_to(RIGHT*right_sf+UP*up_sf)

            #consider vertex animation
            animations.append(MoveToTarget(vertex))

            #consider attached edge animations
            for labels,line in self.edges.items():
                if labels[0] == vertex_label:
                    line.target = Line(RIGHT*right_sf+UP*up_sf, line.target.end)
                elif labels[1] == vertex_label:
                    line.target = Line(line.target.start, RIGHT*right_sf+UP*up_sf)
            
        #   add the animations for the movements of each edge
        for line in self.edges.values():
            animations.append(MoveToTarget(line))

        #finally perform the animations to move the vertices
        input_scene.play(
            *animations
        )

    def remove_angles(self, input_scene):
        #Method to remove all angle images from the given scene
        input_scene.remove(self.angles)
        self.angles = VGroup()

    def generate_angle_arc(self, givenEdges):
        #generates the image to show an angle

        #Determine the intersection point of the two edges which the angle 
        #will be centered about
        intersection_point = self.vertices[givenEdges[0][1]].get_center()

        #Determine the angle of the two edges away from the intersection
        edge1 = self.edges[givenEdges[0]]
        edge1_angle = angle_of_vector(edge1.get_start() - edge1.get_end())
        edge2_angle = self.edges[givenEdges[1]].get_angle()

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
            self.angles += always_redraw(
                    lambda : 
                       self.generate_angle_arc(givenEdges) 
                )

        # Finally, add the angles to the scene
        input_scene.add(self.angles)
    

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
        my_angled_graph.add_angles(self, {(("A","B"),("B","C")) : 0})
        self.wait()

        #moving a single vertex test
        # my_angled_graph.move_vertex(self, "A", (-1,-1))
        # self.wait()

        #moving multiple vertices test
        my_angled_graph.move_vertices(self, A = (-1,-1), B = (-1,0))
        self.wait()