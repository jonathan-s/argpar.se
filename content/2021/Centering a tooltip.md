Title: Centering a tooltip
date: 2021-07-10 00:06
Category: [[51.04 Javascript | Javascript]]
Tags: #frontend, #stimulusjs, #javascript
Slug: centering-tooltip
Authors: Jonathan Sundqvist
Metadescription: Centering a tooltip is a tricky business to get right. This tutorial describes the pitfalls and the final solution for a perfectly working tooltip.
Status: published
image: images/tooltip.webp
internal: [[51.05 Frontend]]

To center a tooltip you'll have to reach for some javascript as you need the coordinates for the element that you either hover over or click on. 

Below I have an implementation for a tooltip using [[Stimulusjs]]. If you're keen on seeing it in action, you can check out the [codepen](https://codepen.io/jonathan-s/pen/zYwONGv) 

```js

class TooltipController extends Stimulus.Controller {
  // This tooltip assumes that the tooltip element isn't
  // contained by an element that is position: relative
  static targets = [ "tooltip" ]
  
  show(event) {
	const aboveTooltip = Number(event.target.dataset.tooltipAbove) 
    const above = aboveTooltip ? aboveTooltip : 30
    let tooltip = this.tooltipTarget
    tooltip.innerHTML = event.target.dataset.tooltipMsg
    // re-paint before getting coordinates from tooltip
	// otherwise we could end with the width of tooltip as 0px
    tooltip.style = 'display: block;'
    
    const ttLoc = tooltip.getBoundingClientRect()
    // getBoundingClientRect is only viewport coordinates 
	// we need height of what we've scrolled. 
    const scroll = document.documentElement.scrollTop
    
    let targetPos = event.target.getBoundingClientRect()
    let yLoc = targetPos.y + scroll - above
    let xLoc = targetPos.x + targetPos.width / 2 - ttLoc.width / 2
    xLoc = xLoc < 0 ? 0 : xLoc
    
    tooltip.style = `position: absolute; top: ${yLoc}px; left: ${xLoc}px;`
  }
  
  hide(event) {
    let tooltip = this.tooltipTarget
    tooltip.style = 'display: none;'
  }
  
}

const application = Stimulus.Application.start();
application.register("tooltip", TooltipController);
```

That's the javascript controller. This is then triggered by an event that you define in html. 

```html
<body data-controller="tooltip">
	<div id="tooltip" style="display: none;" data-target="tooltip.tooltip" class="tooltip">
  	</div>
	<span data-action="mouseover->tooltip#show mouseout->tooltip#hide" data-tooltip-above="30">Hello world</span>
</body>
```

There are a number of edge cases that you need to keep in mind for a robust tooltip. 
- You want to keep the tooltip centered above the element, it's the most natural position. 
- If the element is close to the left or right edge, there is a risk that the tooltip text will be clipped. We want to avoid that. 
- If it's close to the bottom or the top, it could similarly be clipped. 

To get the position of the target element, the element you clicked on, you can use the function `getBoundingClientRect()`. That method returns the coordinates in the viewport, so it does not account for any scrolling the user has done.

To avoid clipping the tooltip at either the bottom or the top we've defined an attribute `data-tooltip-above` where the developer can set how much above or below the tooltip should show up. 

So the position ends up being

```js
// y axis of target element + how much you've scrolled - pixels above target element 
yLoc = targetPos.y + scroll - above
```

For the x coordinate, to be able to center the tooltip, we want to place the element in the middle of the target element. So we add half of the width of target element. Doing so will center the starting point of the tooltip. But as we want to center the middle of the tooltip, we need to also substract half of the width of the tooltip.

In other words 

```js
let xLoc = targetPos.x + targetPos.width / 2 - ttLoc.width / 2
```

Finally if `xLoc` is smaller than 0 we know that the tooltip is placed outside of the viewport so we correct for that by setting it to 0 to avoid clipping the message in the tooltip. 

So that's how you center a tooltip!