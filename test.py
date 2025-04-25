import os
os.environ["FLET_SECRET_KEY"] = "mysecret123"  # This must be before importing flet

from flet import *
from time import sleep

def main(page: Page):
    listfile = Ref[Column]()
    progressbar = ProgressBar(width=page.window.width, value=0, visible=False)

    def res_picker(e: FilePickerResultEvent):
        print(e.files[0].path)
        listfile.current.controls.append(
            Row([Text(e.files[0].name)])
        )
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        progressbar.visible = True
        progressbar.value = e.progress
        sleep(0.1)
        if e.progress == 1:
            progressbar.visible = False
        page.update()

    def btn_upload(e):
        files = []
        for f in filepicker.result.files:
            files.append(
                FilePickerUploadFile(
                    name=f.name,
                    upload_url=page.get_upload_url(f.name, 60)
                )
            )
        filepicker.upload(files)

    filepicker = FilePicker(on_result=res_picker, on_upload=on_upload_progress)
    page.overlay.append(filepicker)

    page.add(
        Column([
            Text("Hello, Flet!"),
            ElevatedButton("Select your files", on_click=lambda _: filepicker.pick_files()),
            Column(ref=listfile),
            progressbar,
            ElevatedButton("Upload", on_click=btn_upload)
        ])
    )

app(
    target=main,
    view=AppView.WEB_BROWSER,
    port=5050,
    upload_dir="assets/images"
)
