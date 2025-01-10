import AttachFileIcon from '@mui/icons-material/AttachFile';
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";
import SendIcon from "@mui/icons-material/Send";
import OutlinedInput from '@mui/material/OutlinedInput';

export function render({model}) {
  const [autogrow] = model.useState("auto_grow")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [max_rows] = model.useState("max_rows")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [rows] = model.useState("rows")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  let props = {}
  if (autogrow) {
    props = {minRows: rows}
  } else {
    props = {rows}
  }

  return (
    <OutlinedInput
      multiline
      color={color}
      error={error_state}
      label={label}
      placeholder={placeholder}
      variant={variant}
      value={value}
      disabled={disabled}
      onChange={(event) => setValue(event.target.value)}
      maxRows={max_rows}
      startAdornment={
	<InputAdornment position="start">
	  <IconButton
	    color="gray"
	    aria-label="upload picture"
	    component="label"
	  >
	    <input
              hidden
              accept="image/*"
              type="file"
	    />
	    <AttachFileIcon />
	  </IconButton>
	</InputAdornment>
      }
      endAdornment={
	<InputAdornment position="end">
	  <IconButton
	    color="primary"
	  >
	    <SendIcon />
	  </IconButton>
	</InputAdornment>
      }
      fullWidth
      {...props}
    />
  )
}
