import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'
import FormControlLabel from '@mui/material/FormControlLabel'
import FormControl from '@mui/material/FormControl'
import FormLabel from '@mui/material/FormLabel'

export function render({ model }) {
  const [disabled] = model.useState("disabled");
  const [color] = model.useState("color");
  const [value, setValue] = model.useState("value");
  const [options] = model.useState("options");
  const [label] = model.useState("label");
  const [orientation] = model.useState("orientation");
  return (
    <FormControl component="fieldset" disabled={disabled}>
      {label && <FormLabel id="demo-radio-buttons-group-label">{label}</FormLabel>}
      <RadioGroup
	aria-labelledby="demo-radio-buttons-group-label"
	value={value}
	onChange={(e) => setValue(e.target.value)}
        row={ orientation === "horizontal" ? true : false }
      >
        {options.map((option, index) => {
	  return (
	    <FormControlLabel
              key={option}
              value={option}
	      label={option}
              control={<Radio color={color}/>}
	    />
	  )
        })}
      </RadioGroup>
    </FormControl>
  );
}
