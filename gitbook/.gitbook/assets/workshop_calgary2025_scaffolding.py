#! python3
# venv: brg-csd

from math import ceil

import rhinoscriptsyntax as rs

import compas_rhino.conversions
import compas_rhino.objects
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector
from compas.geometry import bounding_box
from compas.geometry import intersection_polyline_plane
from compas.geometry import midpoint_point_point
from compas.geometry import trimesh_slice
from compas.scene import Scene

DIVISION_DISTANCE_U = 50
DIVISION_DISTANCE_V = 50
THICKNESS = 2
GAP_JOINT = 1
Z_OFFSET = -40


# Select Mesh
guids = compas_rhino.objects.select_meshes()
polygons = []
for guid in guids:
    mesh = compas_rhino.conversions.meshobject_to_compas(guid)
    polygons.extend(mesh.to_polygons())

mesh = Mesh.from_polygons(polygons)

# Select Boundary Polygon
guid = rs.GetObject("Select a polyline as a region.", rs.filter.curve)
rh_pline = obj = compas_rhino.objects.find_object(guid).Geometry.ToPolyline()
polyline = compas_rhino.conversions.polyline_to_compas(rh_pline)

# Select Primary Direction
guid = rs.GetObject("Select a line as a direction.", rs.filter.curve)
rh_line = compas_rhino.objects.find_object(guid).Geometry
line = Line([rh_line.PointAtStart.X, rh_line.PointAtStart.Y, rh_line.PointAtStart.Z], [rh_line.PointAtEnd.X, rh_line.PointAtEnd.Y, rh_line.PointAtEnd.Z])


class Waffle:
    def __init__(self, mesh: Mesh, region: Polyline, direction: line, zoffset: float = 40):
        self.mesh = mesh
        self.region = region
        self.direction = line
        self.proces_region()

        aabb_mesh = self.mesh.aabb()
        aabb_region = Box.from_points(bounding_box(self.region.points))
        aabb_direction = Box.from_points(bounding_box([self.direction.start, self.direction.end]))
        self.region.transform(Translation.from_vector([0, 0, aabb_mesh.zmin - aabb_region.zmin + zoffset]))
        self.direction.transform(Translation.from_vector([0, 0, aabb_mesh.zmin - aabb_direction.zmin + zoffset]))

        self.planes_u = []
        self.planes_v = []

        self.bottom_lines_u: list[list[Line]] = []
        self.bottom_lines_v: list[list[Line]] = []

        self.top_polylines_u: list[list[Polyline]] = []
        self.top_polylines_v: list[list[Polyline]] = []

        self.polygons_u: list[Polygon] = []
        self.polygons_v: list[Polygon] = []

        self.polylines_u_with_cuts: list[Polyline] = []
        self.polylines_v_with_cuts: list[Polyline] = []
        self.frames_u_with_cuts: list[Frame] = []
        self.frames_v_with_cuts: list[Frame] = []

        self.oriented_polylines_u: list[Polyline] = []
        self.oriented_polylines_v: list[Polyline] = []

    @property
    def transformation(self):
        """
        Compute the transformation needed to align the cutting direction.
        This transformation is required to adjust the mesh and region.
        Cutting planes will be aligned to the x and y axes based on the region's AABB.
        """
        mesh_aabb = self.mesh.aabb()
        origin = self.direction.start
        origin = Point(origin[0], origin[1], origin[2] + mesh_aabb.zmin)
        x_axis = self.direction.direction
        y_axis = x_axis.cross(Vector(0, 0, -1))  # Ensure perpendicular vector in the XY plane
        frame = Frame(origin, x_axis, y_axis)

        return Transformation.from_frame_to_frame(frame, Frame.worldXY())

    def proces_region(self):
        
        points = []
        for vertex in self.mesh.vertices_on_boundary():
            p = self.mesh.vertex_point(vertex)
            points.append(Point(p[0], p[1], 0))
        polygon = Polygon(points)

        result = Polygon(self.region.points[:-1]).boolean_intersection(polygon)
        self.region = Polyline(result.points + [result[0]])     

    def get_cut_planes(self, distance_u: float, distance_v: float):
        """
        From the oriented region bounding-box and division distances construct the cutting frames.
        """
        T = self.transformation
        region_transformed = self.region.transformed(T)

        aabb = Box.from_points(bounding_box(region_transformed))
        origin = aabb.corner(0)

        def generate_planes(distance, divisions, axis):
            return [Plane(origin + axis * i * distance, axis) for i in range(divisions)]

        self.planes_u = generate_planes(distance_u, ceil(aabb.xsize / distance_u), Vector.Xaxis())
        self.planes_v = generate_planes(distance_v, ceil(aabb.ysize / distance_v), Vector.Yaxis())

    def section_region(self, tolerance=0.01):
        """
        Intersections of region and cut planes with the transformed region.
        """



        T = self.transformation

        region_transformed = self.region.transformed(T)

        polygon = Polygon(region_transformed.points[:-1])

        def process_cut_planes(cut_planes, bottom_lines, sort_coordinate):
            for plane in cut_planes:
                points = intersection_polyline_plane(region_transformed, plane)
                points = sorted(points, key=lambda p: p[sort_coordinate])
                lines = []
                for i in range(len(points) - 1):
                    p0 = Point(*points[i])
                    p1 = Point(*points[i + 1])
                    pmid = Point(*midpoint_point_point(p0, p1))
                    if pmid.in_polygon(polygon):
                        # if p0.distance_to_point(p1) > tolerance:
                        lines.append(Line(p0, p1))
                bottom_lines.append(lines)

        process_cut_planes(self.planes_u, self.bottom_lines_u, 1)
        process_cut_planes(self.planes_v, self.bottom_lines_v, 0)

    def section_mesh(self):
        """
        Compute intersections of the mesh and cut planes with the transformed region.
        """
        T = self.transformation
        V, F = self.mesh.transformed(T).to_vertices_and_faces()

        def extract_polylines(coordinates):
            return [Polyline([Point(*point) for point in polyline]) for polyline in coordinates]

        for plane in self.planes_u:
            
            try:
                result = trimesh_slice((V, F), [plane])
                if result:
                    self.top_polylines_u.append(extract_polylines(result))
            except:
                self.top_polylines_u.append([])
                
                print("section_mesh error u-direction")
                pass

        for plane in self.planes_v:
           
            try:
                result = trimesh_slice((V, F), [plane])
                if result:
                    self.top_polylines_v.append(extract_polylines(result))
            except:
                self.top_polylines_v.append([])
                
                print("section_mesh error v-direction")
                pass

    def clip_polyline(self):
        """
        Cut the mesh polylines by the bottom lines' end points in both U and V directions.
        """

        def process_direction(bottom_lines, top_polylines, closed_polylines, tol = 0.01):

            

         
                
            for i in range(len(bottom_lines)):

                lines = bottom_lines[i]
                polylines = top_polylines[i]

                for line in lines:
                    plane0 = Plane(line.start, -line.direction)
                    plane1 = Plane(line.end, line.direction)


                    points = []
                    for polyline in polylines:

                        points0 = []
                        points1 = []

                        # End points of lines as planes are intersected with polyline.
                        # COMPAS bug: when end points of polyline and line have the same position, intersection is not found.
                        # This border cases is handled in if and elif statements below.
                        if(abs(polyline[0][0]-line.start[0]) < tol and abs(polyline[0][1]-line.start[1]) < tol):
                            points0 = [polyline[0]]
                        elif(abs(polyline[-1][0]-line.start[0]) < tol and abs(polyline[-1][1]-line.start[1]) < tol):
                            points0 = [polyline[-1]]
                        else:
                            points0 = intersection_polyline_plane(polyline, plane0)

                        if(abs(polyline[0][0]-line.end[0]) < tol and abs(polyline[0][1]-line.end[1]) < tol):
                            points1 = [polyline[0]]
                        elif(abs(polyline[-1][0]-line.end[0]) < tol and abs(polyline[-1][1]-line.end[1]) < tol):
                            points1 = [polyline[-1]]
                        else:
                            points1 = intersection_polyline_plane(polyline, plane1)

                    

                        if len(points0) > 1 and len(points1) > 1:
                            # print("Waffle.clip_polyline: more than one intersection point per line and polyline pair, skipping this case.")
                            continue
                        elif len(points0) > 0 or len(points1) > 0:
                            # print("Waffle.clip_polyline: two points")

                            p2, p3 = line.end, line.start

                            distances_to_first_plane = []
                            for p in polyline:
                                distance0 = plane0.normal.dot(plane0.point - p)
                                distance1 = plane1.normal.dot(plane1.point - p)
                                if distance0 > 0 and distance1 > 0:
                                    distances_to_first_plane.append(abs(distance0))
                                    points.append(p)

                            if distances_to_first_plane and distances_to_first_plane[0] > distances_to_first_plane[-1]:
                                points.reverse()

                            p0 = Point(*points0[0]) if points0 else points[0]
                            p1 = Point(*points1[0]) if points1 else points[-1]
                            p2, p3 = Point(p1[0], p1[1], p2[2]), Point(p0[0], p0[1], p3[2])

                            if points0:
                                points.insert(0, p0)
                            if points1:
                                points.append(p1)

                            points.extend([p2, p3])
                            closed_polylines.append(Polygon(points))
                            # scene.add(closed_polylines[-1])
                        else:
                            print(points0, points1)
                            scene.add(line)
                            scene.add(polyline)
                            scene.add(plane0)
                            scene.add(plane1)
                            


        # Process both U and V directions using the helper function
        process_direction(self.bottom_lines_u, self.top_polylines_u, self.polygons_u)
        process_direction(self.bottom_lines_v, self.top_polylines_v, self.polygons_v)

    def create_cross_joint(self, gap_joint: float, thickness: float):
        # Process data
        polylines_u_vertical = []
        polylines_u_vertical_planes = []
        polylines_u_vertical_cuts = {}

        polylines_v_vertical = []
        polylines_v_vertical_planes = []
        polylines_v_vertical_cuts = {}

        counter = 0
        for idx, polygon in enumerate(self.polygons_u):
            if len(polygon.points) > 2:
                polylines_u_vertical.append(Polyline(polygon.points))
                polylines_u_vertical_planes.append(polygon.plane)
                polylines_u_vertical_cuts[counter] = []
                counter = counter + 1

        counter = 0
        for idx, polygon in enumerate(self.polygons_v):
            if len(polygon.points) > 2:
                polylines_v_vertical.append(Polyline(polygon.points))
                polylines_v_vertical_planes.append(polygon.plane)
                polylines_v_vertical_cuts[counter] = []
                counter = counter + 1

        # Intersection Polygons
        boolean_offset_vector = Vector(0, 0, max(self.mesh.transformed(self.transformation).aabb().zsize, 1))
        gap_vector = Vector(0, 0, gap_joint * 0.5)

        for i in range(len(polylines_u_vertical)):
            for j in range(len(polylines_v_vertical)):
                result = intersection_polyline_plane(polylines_u_vertical[i], polylines_v_vertical_planes[j])
                if not result:
                    continue
                if len(result) != 2:
                    continue

                if result[0][2] > result[1][2]:
                    result[0], result[1] = result[1], result[0]

                p0 = Point(*result[0]) - boolean_offset_vector
                p1 = Point(*result[1]) + boolean_offset_vector

                pmid = Point((result[0][0] + result[1][0]) * 0.5, (result[0][1] + result[1][1]) * 0.5, (result[0][2] + result[1][2]) * 0.5)

                offset_dir = (p0 - pmid).cross(polylines_u_vertical_planes[i].normal).unitized()

                polyline_u = Polyline(
                    [
                        p0 + offset_dir * thickness * 0.5,
                        pmid + offset_dir * thickness * 0.5 + gap_vector * 0.5,
                        pmid - offset_dir * thickness * 0.5 + gap_vector * 0.5,
                        p0 - offset_dir * thickness * 0.5,
                    ]
                )

                offset_dir = (p1 - pmid).cross(polylines_v_vertical_planes[j].normal).unitized()
                polyline_v = Polyline(
                    [
                        p1 + offset_dir * thickness * 0.5,
                        pmid + offset_dir * thickness * 0.5 - gap_vector * 0.5,
                        pmid - offset_dir * thickness * 0.5 - gap_vector * 0.5,
                        p1 - offset_dir * thickness * 0.5,
                    ]
                )
                polylines_u_vertical_cuts[i].append(polyline_u)
                polylines_v_vertical_cuts[j].append(polyline_v)

        # =============================================================================
        # Boolean Difference the Cuts
        # =============================================================================

        X = self.transformation.inverse()

        for key, value in polylines_u_vertical_cuts.items():
            if len(value) == 0:
                continue

            a = Polygon(polylines_u_vertical[key])
            frame = a.frame
            T = Transformation.from_frame_to_frame(frame, Frame.worldXY())
            T_I = Transformation.from_frame_to_frame(Frame.worldXY(), frame)
            a.transform(T)

            for o in value:
                b = Polygon(o.points)
                c = a.boolean_difference(b.transformed(T))
                a = c

            a.transform(T_I)
            self.polylines_u_with_cuts.append(Polyline(a.points + [a.points[0]]))
            self.polylines_u_with_cuts[-1].transform(X)
            self.frames_u_with_cuts.append(frame.transformed(X))

        for key, value in polylines_v_vertical_cuts.items():
            if len(value) == 0:
                continue

            a = Polygon(polylines_v_vertical[key])
            frame = a.frame

            T = Transformation.from_frame_to_frame(frame, Frame.worldXY())
            T_I = Transformation.from_frame_to_frame(Frame.worldXY(), frame)
            a.transform(T)

            for o in value:
                b = Polygon(o.points)
                a = a.boolean_difference(b.transformed(T))

            a.transform(T_I)
            self.polylines_v_with_cuts.append(Polyline(a.points + [a.points[0]]))
            self.polylines_v_with_cuts[-1].transform(X)
            self.frames_v_with_cuts.append(frame.transformed(X))

        # for polyline in self.polygons_u:
        #     scene.add(polyline)

        # for polyline in self.polygons_v:
        #     scene.add(polyline)

    def low_res_font(self):
        """
        Returns a dictionary of polylines representing low-resolution characters (A-Z, 0-9).
        """
        font = {
            "A": [Polyline([Point(0, 0, 0), Point(0.5, 2, 0), Point(1, 0, 0), Point(0.75, 1, 0), Point(0.25, 1, 0), Point(0, 0, 0)])],
            "B": [Polyline([Point(0, 2, 0), Point(0.5, 2, 0), Point(1, 1.5, 0), Point(0.5, 1, 0), Point(1, 0.5, 0), Point(0.5, 0, 0), Point(0, 0, 0), Point(0, 2, 0)])],
            "0": [Polyline([Point(0, 0, 0), Point(0, 2, 0), Point(1, 2, 0), Point(1, 0, 0), Point(0, 0, 0)])],
            "1": [Polyline([Point(0.5, 0, 0), Point(0.5, 2, 0)])],
            "2": [Polyline([Point(0, 2, 0), Point(1, 2, 0), Point(1, 1, 0), Point(0, 0, 0), Point(1, 0, 0)])],
            "3": [Polyline([Point(0, 2, 0), Point(1, 2, 0), Point(1, 1, 0), Point(0.5, 1, 0), Point(1, 1, 0), Point(1, 0, 0), Point(0, 0, 0)])],
            "4": [Polyline([Point(0, 2, 0), Point(0, 1, 0), Point(1, 1, 0), Point(1, 2, 0), Point(1, 0, 0)])],
            "5": [Polyline([Point(1, 2, 0), Point(0, 2, 0), Point(0, 1, 0), Point(1, 1, 0), Point(1, 0, 0), Point(0, 0, 0)])],
            "6": [Polyline([Point(1, 2, 0), Point(0, 2, 0), Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)])],
            "7": [Polyline([Point(0, 2, 0), Point(1, 2, 0), Point(0.5, 0, 0)])],
            "8": [Polyline([Point(0, 0, 0), Point(0, 2, 0), Point(1, 2, 0), Point(1, 0, 0), Point(0, 0, 0), Point(0, 1, 0), Point(1, 1, 0)])],
            "9": [Polyline([Point(1, 0, 0), Point(1, 2, 0), Point(0, 2, 0), Point(0, 1, 0), Point(1, 1, 0)])],
        }
        return font

    def string_to_geometry(self, text, frame, size, offset):
        """
        Converts a string into a list of polylines representing characters.
        """
        font = self.low_res_font()
        geometry = []
        x_offset = 0

        for char in text.upper():
            if char in font:
                for polyline in font[char]:
                    moved_polyline = Polyline([Point(p.x + x_offset, p.y, p.z) for p in polyline.points])
                    geometry.append(moved_polyline)
                x_offset += 2  # Spacing between characters

        T = Translation.from_vector(offset)
        X = Transformation.from_frame_to_frame(Frame.worldXY(), frame)
        for g in geometry:
            g.scale(size * 0.5)
            g.transform(X)
            g.transform(T)

        return geometry

    def add_numbers_and_orient_to_grid(self, gap: float = 10):
        width = 0
        max_height = 0
        for idx, polyline in enumerate(self.polylines_u_with_cuts):
            box = Box.from_points(bounding_box(polyline.points))
            frame = self.frames_u_with_cuts[idx]
            frame.point = Point(frame.point[0], frame.point[1], box.zmin)
            T = Transformation.from_frame_to_frame(frame, Frame.worldXY())
            T_I = Transformation.from_frame_to_frame(Frame.worldXY(), frame)
            xy_polyline = polyline.transformed(T)
            xy_frame = Frame.worldXY()

            box = Box.from_points(bounding_box(xy_polyline.points))
            T = Translation.from_vector([-box.xmin + width, 0, 0])
            xy_polyline = xy_polyline.transformed(T)
            T = Translation.from_vector([width, 0, 0])
            xy_frame.transform(T)
            width = width + box.xsize + gap

            if box.ysize > max_height:
                max_height = box.ysize

            text_xy = self.string_to_geometry("A" + str(idx), xy_frame, 10, Vector(5, 5, 0))
            for t in text_xy:
                self.oriented_polylines_u.append(t)
                self.oriented_polylines_u.append(t.transformed(T_I * T.inverse() * Translation.from_vector([box.xmin, 0, 0])))

            self.oriented_polylines_u.append(xy_polyline)

        width = 0
        for idx, polyline in enumerate(self.polylines_v_with_cuts):
            box = Box.from_points(bounding_box(polyline.points))
            frame = self.frames_v_with_cuts[idx]
            frame.point = Point(frame.point[0], frame.point[1], box.zmin)
            T = Transformation.from_frame_to_frame(frame, Frame.worldXY())
            T_I = Transformation.from_frame_to_frame(Frame.worldXY(), frame)
            xy_polyline = polyline.transformed(T)
            xy_frame = Frame.worldXY()

            box = Box.from_points(bounding_box(xy_polyline.points))
            T = Translation.from_vector([-box.xmin + width, max_height + gap, 0])
            xy_polyline = xy_polyline.transformed(T)
            T = Translation.from_vector([width, max_height + gap, 0])
            xy_frame.transform(T)
            width = width + box.xsize + gap

            if box.ysize > max_height:
                max_height = box.ysize

            text_xy = self.string_to_geometry("B" + str(idx), xy_frame, 10, Vector(5, 5, 0))
            for t in text_xy:
                self.oriented_polylines_v.append(t)
                self.oriented_polylines_v.append(t.transformed(T_I * T.inverse() * Translation.from_vector([box.xmin, 0, 0])))

            self.oriented_polylines_v.append(xy_polyline)

scene = Scene()

waffle = Waffle(mesh, polyline, line, Z_OFFSET)
waffle.get_cut_planes(DIVISION_DISTANCE_U, DIVISION_DISTANCE_V)
waffle.section_region()
waffle.section_mesh()
waffle.clip_polyline()
waffle.create_cross_joint(GAP_JOINT, THICKNESS)
waffle.add_numbers_and_orient_to_grid()

for polyline in waffle.polylines_u_with_cuts:
    scene.add(polyline)

for polyline in waffle.polylines_v_with_cuts:
    scene.add(polyline)

for polyline in waffle.oriented_polylines_u:
    scene.add(polyline)

for polyline in waffle.oriented_polylines_v:
    scene.add(polyline)

scene.clear_context()
scene.draw()
