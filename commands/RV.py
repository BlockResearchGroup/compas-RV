#! python3
# venv: brg-csd
# r: compas_rv>=0.9.1

import pathlib

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore
import System  # type: ignore

pluginfile = Rhino.PlugIns.PlugIn.PathFromId(System.Guid("a6dc4669-0e8e-40ea-8d71-b9b0f4764ec1"))
shared = pathlib.Path(str(pluginfile)).parent / "shared"


class SplashForm(Eto.Forms.Dialog[bool]):
    def __init__(self, title, url, width=800, height=450):
        super().__init__()

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(width, height)
        self.WindowStyle = Eto.Forms.WindowStyle.NONE  # type: ignore

        webview = Eto.Forms.WebView()
        webview.Size = Eto.Drawing.Size(width, height)
        webview.Url = System.Uri(url)
        webview.BrowserContextMenuEnabled = False
        webview.DocumentLoading += self.action

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical()
        layout.AddRow(webview)
        layout.EndVertical()
        self.Content = layout

    def action(self, sender, e):
        if e.Uri.Scheme == "action" and e.Uri.Host == "close":
            self.Close()

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


def RunCommand():
    form = SplashForm(title="RhinoVAULT", url=str(shared / "index.html"))
    form.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
