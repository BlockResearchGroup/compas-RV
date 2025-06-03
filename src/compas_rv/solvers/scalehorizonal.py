import Rhino  # type: ignore
from numpy import array
from numpy import float64

import compas_rhino.conversions
from compas_fd.solvers.fd_numerical_data import FDNumericalData
from compas_rv.conduits import EdgesConduit
from compas_rv.datastructures import ThrustDiagram
from compas_tna.equilibrium.diagrams import update_z
from compas_tna.loads import LoadUpdater


class InteractiveScaleHorizontal:
    def __init__(
        self,
        thrust: ThrustDiagram,
    ):
        self.thrust = thrust
        self.scale = 1.0

        self._numdata = None
        self._loadupdater = None
        self._q0 = None
        self._conduit_edges = None

    def __call__(self):
        try:
            self.start()
            self.stop()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    @property
    def conduit_edges(self) -> EdgesConduit:
        if not self._conduit_edges:
            self._conduit_edges = EdgesConduit(self.numdata.xyz, self.numdata.edges, thickness=1)
        return self._conduit_edges

    @property
    def numdata(self) -> FDNumericalData:
        if self._numdata is None:
            vertex_index = self.thrust.vertex_index()
            vertices = self.thrust.vertices_attributes("xyz")
            loads = [self.thrust.vertex_attributes(vertex, ["px", "py", "pz"]) or [0, 0, 0] for vertex in self.thrust.vertices()]
            fixed = [vertex_index[vertex] for vertex in self.thrust.vertices_where(is_support=True)]
            edges = list(self.thrust.edges_where(_is_edge=True))
            forcedensities = list(self.thrust.edges_attribute(name="q", keys=edges))
            edges = [(vertex_index[u], vertex_index[v]) for u, v in edges]
            self._numdata = FDNumericalData.from_params(vertices, fixed, edges, forcedensities, loads)
        return self._numdata

    # this can be done more elegantly
    @property
    def loadupdater(self) -> LoadUpdater:
        if self._loadupdater is None:
            self._loadupdater = LoadUpdater(
                self.thrust,
                array(self.numdata.p, copy=True),
                array(self.thrust.vertices_attribute("t"), dtype=float64).reshape((-1, 1)),
                1.0,
            )
        return self._loadupdater

    def _update(self) -> None:
        update_z(
            self.numdata.xyz,
            self.scale * self.numdata.Q,
            self.numdata.C,
            self.numdata.p,
            self.numdata.free,
            self.numdata.fixed,
            self.loadupdater,
            kmax=10,
        )

    def start(self):
        def on_dynamic_draw(sender, e):
            self.conduit_edges.disable()
            p2 = compas_rhino.conversions.point_to_compas(e.CurrentPoint)
            v02 = p2 - p0
            self.scale = v02.length / v01.length
            self._update()
            self.conduit_edges.enable()

        get_p0 = Rhino.Input.Custom.GetPoint()
        get_p0.SetCommandPrompt("Select base point")
        get_p0.Get()
        rhino_p0 = get_p0.Point()
        p0 = compas_rhino.conversions.point_to_compas(rhino_p0)

        get_p1 = Rhino.Input.Custom.GetPoint()
        get_p1.DrawLineFromPoint(rhino_p0, True)
        get_p1.SetCommandPrompt("Select reference 1")
        get_p1.Get()
        rhino_p1 = get_p1.Point()
        p1 = compas_rhino.conversions.point_to_compas(rhino_p1)

        v01 = p1 - p0

        get_p2 = Rhino.Input.Custom.GetPoint()
        get_p2.Constrain(rhino_p0, rhino_p1)
        get_p2.DrawLineFromPoint(rhino_p0, True)
        get_p2.SetCommandPrompt("Select reference 2")
        get_p2.DynamicDraw += on_dynamic_draw
        get_p2.Get()
        rhino_p2 = get_p2.Point()
        p2 = compas_rhino.conversions.point_to_compas(rhino_p2)

        v02 = p2 - p0

        self.scale = v02.length / v01.length  # scaling is always positive

    def stop(self):
        update_z(
            self.numdata.xyz,
            self.scale * self.numdata.Q,
            self.numdata.C,
            self.numdata.p,
            self.numdata.free,
            self.numdata.fixed,
            self.loadupdater,
            kmax=100,
        )

        self.conduit_edges.disable()
        del self._conduit_edges
        self._conduit_edges = None
