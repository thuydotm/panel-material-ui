import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';

export function render({ model} ) {
  const objects = model.get_child("objects");
  const [active] = model.useState("active");
  const [names] = model.useState("_names");
  const [toggle] = model.useState("toggle");

  const handle_expand = (index) => (event, newExpanded) => {
    console.log(index, newExpanded)
  };

  return (
    <>
      { objects.map((obj, index) => {
	return (
	  <Accordion
	    defaultExpanded={active.includes(index)}
	    key={"accordion-"+index}
	    onChange={handle_expand(index)}
	  >
	    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{names[index]}</AccordionSummary>
	    <AccordionDetails>{obj}</AccordionDetails>
	  </Accordion>
	)
      }) }
    </>
  );
}
