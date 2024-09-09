#! python3

try:
    import compas
except ModuleNotFoundError:
    compas = False

try:
    import compas_ags
except ModuleNotFoundError:
    compas_ags = False

try:
    import compas_fd
except ModuleNotFoundError:
    compas_fd = False

try:
    import compas_rui
except ModuleNotFoundError:
    compas_rui = False
    InfoForm = False
else:
    from compas_rui.forms import InfoForm

try:
    import compas_session
except ModuleNotFoundError:
    compas_session = False

try:
    import compas_tna
except ModuleNotFoundError:
    compas_tna = False

if not InfoForm:
    import Eto.Drawing  # type: ignore
    import Eto.Forms  # type: ignore
    import Rhino  # type: ignore
    import Rhino.UI  # type: ignore

    class InfoForm(Eto.Forms.Dialog[bool]):
        def __init__(self, text, title="Info", width=800, height=500):

            super().__init__()

            self.Title = title
            self.Padding = Eto.Drawing.Padding(0)
            self.Resizable = True
            self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
            self.ClientSize = Eto.Drawing.Size(width, height)
            textarea = Eto.Forms.TextArea()
            textarea.Text = text
            textarea.ReadOnly = True
            layout = Eto.Forms.DynamicLayout()
            layout.BeginVertical(Eto.Drawing.Padding(12, 12, 12, 0), Eto.Drawing.Size(0, 0), True, True)
            layout.AddRow(textarea)
            layout.EndVertical()
            layout.BeginVertical(Eto.Drawing.Padding(12, 12, 12, 18), Eto.Drawing.Size(6, 0), False, False)
            layout.AddRow(None, self.ok)
            layout.EndVertical()
            self.Content = layout

        @property
        def ok(self):
            self.DefaultButton = Eto.Forms.Button(Text="OK")
            self.DefaultButton.Click += self.on_ok
            return self.DefaultButton

        def on_ok(self, sender, event):
            self.Close(True)

        def show(self):
            return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


def RunCommand(interactive):

    width = len("compas_session") + 1

    lines = [
        "compas is not installed" if not compas else f"{compas.__name__:<{width}}: {compas.__version__}",
        "compas_ags is not installed" if not compas_ags else f"{compas_ags.__name__:<{width}}: {compas_ags.__version__}",
        "compas_fd is not installed" if not compas_fd else f"{compas_fd.__name__:<{width}}: {compas_fd.__version__}",
        "compas_rui is not installed" if not compas_rui else f"{compas_rui.__name__:<{width}}: {compas_rui.__version__}",
        "compas_session is not installed" if not compas_session else f"{compas_session.__name__:<{width}}: {compas_session.__version__}",
        "compas_tna is not installed" if not compas_tna else f"{compas_tna.__name__:<{width}}: {compas_tna.__version__}",
    ]

    form = InfoForm(text="\n".join(lines), title="Verify Installation")
    form.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
