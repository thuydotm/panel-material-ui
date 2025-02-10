import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"
import Tooltip from "@mui/material/Tooltip";

export function render({model, el}) {
  const [color] = model.useState("button_type")
  const [description] = model.useState("description")
  const [description_delay] = model.useState("description_delay")
  const [size] = model.useState("size")
  const [orientation] = model.useState("orientation")
  const [disabled] = model.useState("disabled")
  const [disableElevation] = model.useState("disableElevation")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")
  const exclusive = model.esm_constants.exclusive
  const button_group = (
    <ToggleButtonGroup
      disabled={disabled}
      orientation={orientation}
      value={value}
    >
      {options.map((option, index) => {
        return (
          <ToggleButton
            color={color}
            size={size}
            aria-label={option}
            key={option}
            value={option}
            selected={exclusive ? (value==option) : value.includes(option)}
            onClick={(e) => {
              let newValue
              if (exclusive) {
                newValue = option
              } else if (value.includes(option)) {
                newValue = value.filter((v) => v !== option)
              } else {
                newValue = [...value]
                newValue.push(option)
              }
              setValue(newValue)
            }}
          >
            {option}
          </ToggleButton>
        )
      })}
    </ToggleButtonGroup>
  )
  return (description ? (
    <Tooltip
      title={description}
      enterDelay={description_delay}
      arrow
      placement="right"
      PopperProps={{
        container: el
      }}
    >
      {button_group}
    </Tooltip>) : button_group
  )
}
