import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";

export function render({model, view}) {
  const [full_screen] = model.useState("full_screen");
  const [open] = model.useState("open");
  const [title] = model.useState("title");
  const objects = model.get_child("objects");

  model.on("after_render", () => {
    document.head.append(...view.style_cache.children)
  })

  return (
    <Dialog open={open} fullScreen={full_screen}>
      <DialogTitle>
        {title}
      </DialogTitle>
      <DialogContent>
	{objects}
      </DialogContent>
    </Dialog>
  );
}
