import ToggleButtonGroup from '@mui/material/ToggleButtonGroup'
import ToggleButton from '@mui/material/ToggleButton'

function __Button({ value, ...otherProps }) {
  return (
    <ToggleButton
      variant="outlined"
      value={value}
      {...otherProps}
    />
  );
}


export function render({ model }) {
  const [variant] = model.useState("variant")
  const [color] = model.useState("color")
  const [size] = model.useState("size")
  const [orientation] = model.useState("orientation")
  const [disabled] = model.useState("disabled")
  const [disableElevation] = model.useState("disableElevation")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")

  return (
    <ToggleButtonGroup
      value={value}
      exclusive={model.esm_constants.exclusive}
      onChange={(event, newValue) => { setValue(newValue)}}
      orientation={orientation}
      size={size}
      color={color}
      disabled={disabled}
      fullWidth={true}
      variant={variant}
    >
      {...options.map((btn, index) => {
	return (
	  <__Button
	    aria-label={btn}
	    color={color}
	    value={btn}
	    selected={btn === value}
	    variant={variant}
	  >
	    {btn}
	  </__Button>
	)
      })}
    </ToggleButtonGroup>
  )
}
