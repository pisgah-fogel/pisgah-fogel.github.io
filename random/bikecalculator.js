/**
 * Bike Calculator Javascript Code
 * 
 *
 * Copyright (c) 2012, 2015, Curt Austin
 * All rights reserved
 * 
 */

/*
Power (watts):
Velocity (km/h):
Units:
Rider weight: rweight.value
Bicycle weight: bweight.value
Tires: theTire, rollingRes
Position: theAero, frontalArea
Grade: gradev
Head wind: headwindv
Distance: distancev
Temperature: temperaturev
Elevation: elevationv
Transmission efficiency: transv
Time:
Calories:
Weight loss:
*/

theTire = tire.selectedIndex;
rollingRes = tireValues[theTire];
theAero = aero.selectedIndex;
frontalArea = aeroValues[theAero];

gradev = eval(grade.value) * 0.01;
headwindv = eval(headwind.value)  * (units ? 1.609 : 1.0) / 3.6;  // converted to m/s
distancev = eval(distance.value)  * (units ? 1.609 : 1.0);
temperaturev = ( eval(temperature.value) - (units ? 32.0 : 0.0) )  * (units ? 0.5555 : 1.0);
elevationv = eval(elevation.value)  * (units ? 0.3048 : 1.0);
transv = 0.95; // no one knows what this is, so why bother presenting a choice?
 
units = 0; // default is metric
calcMode = 0; // zero means we calculate velocity, 1 means power
tireValues = [0.005, 0.004, 0.012];
aeroValues = [0.388, 0.445, 0.420, 0.300, 0.233, 0.200];

function makeDecimal2 (value) {
	if (value != null && value != 0) {
		var x = Math.round(parseFloat(value) * 100);
		var d;
		if (x < 100) d=0;
		else d = parseInt(x / 100);
		var c = x % 100;
		var g = (c >= 10)?"":"0";
		value = "" + d + "." + g + c;
	}
	return value
}

function makeDecimal0 (value) {
	if (value != null && value != 0) {
		value = "" + Math.round(parseFloat(value));
	}
	return value
}

function valDecNumber(str) {  /* returns true if a valid number */
	if(str.length == 0) return false;
	var noNegSignYet = true;
	var noPointYet = true;
	for (i=0; i < str.length; i++) {
		var chr = str.substring(i, i+1)
		if (noPointYet && chr == ".") noPointYet = false;
		else if (noNegSignYet && chr == "-") noNegSignYet = false;
		else if (chr< "0" || chr > "9") {
			alert ("I don't think you want to do that, Dave.");
			return false
		}
	}
	return true
}

function empty(inputStr) {
	if (inputStr == "" || inputStr == null) return true;
	return false
}

function newton(aero, hw, tr, tran, p) {        /* Newton's method */

		var vel = 20;       // Initial guess
		var MAX = 10;       // maximum iterations
		var TOL = 0.05;     // tolerance
		for (i=1; i < MAX; i++) {
			var tv = vel + hw;
			var aeroEff = (tv > 0.0) ? aero : -aero; // wind in face, must reverse effect
			var f = vel * (aeroEff * tv * tv + tr) - tran * p; // the function
			var fp = aeroEff * (3.0 * vel + hw) * tv + tr;     // the derivative
			var vNew = vel - f / fp;
			if (Math.abs(vNew - vel) < TOL) return vNew;  // success
			vel = vNew;
		}
		return 0.0;  // failed to converge
}

function setMode(mode) { // called when velocity is entered
	calcMode = mode;
}

function changeUnits(form) {  // units = 1 means US units
	// called when units menu triggers an onChange event
	with (form) {
		units = unitsMenu.selectedIndex;
		if(units==0) { // change displays to metric
			rweight.value = makeDecimal0(rweightv);
			bweight.value = makeDecimal0(bweightv);
			headwind.value =  makeDecimal0(headwindv * 3.6);  // convert to kph from m/s
			distance.value = makeDecimal2(distancev);
			temperature.value = makeDecimal0(temperaturev);
			elevation.value = makeDecimal0(elevationv);
			// calories and weight loss will be be updated without having to do it here.
		} else {  // change displays to US
			rweight.value = makeDecimal0(rweightv * 2.205);
			bweight.value = makeDecimal0(bweightv * 2.205);
			headwind.value =  makeDecimal0(headwindv * 3.6 * 0.6215);
			distance.value = makeDecimal2(distancev * 0.6215);
			temperature.value = makeDecimal0(temperaturev * 1.8 + 32.0);
			elevation.value = makeDecimal0(elevationv * 3.281);
		}
			calcMode = 0;  // force into "standard" mode to avoid complications
			update(form);  // velocity, calories and wt loss will be re-calculated here
	}
}

function updateDistance(form, field) {
// change distance to suit time 1, calories 2, or wt loss 3
	with (form) {
		if (field==1) { // a time was entered
		//alert("time entered");
			newTime = eval(time.value);  // minutes
			distancev *= newTime/t;
			distance.value = makeDecimal2(distancev * (units ? 0.6214 : 1.0));
		}
		else if (field==2) { // calories were entered
			newCal = eval(calories.value) * (units ? 4.188 : 1.0); 
			distancev *= newCal/c;
			distance.value = makeDecimal2(distancev * (units ? 0.6214 : 1.0));
		}
		else { // wt loss was entered
			newWeightloss = eval(weightloss.value) * (units ? 0.4536 : 1.0);
			distancev *= newWeightloss/wl;
			distance.value = makeDecimal2(distancev * (units ? 0.6214 : 1.0));
		}
		update(form);
	}
}

function update(form) {
	// all done in metric units, JIT conversion to/from

	with (form) {

		// get most form values
		{ 
		rweightv = eval(rweight.value) * (units ? 0.4536 : 1.0);
		bweightv = eval(bweight.value) * (units ? 0.4536 : 1.0);
		theTire = tire.selectedIndex;
		rollingRes = tireValues[theTire];
		theAero = aero.selectedIndex;
		frontalArea = aeroValues[theAero];
		gradev = eval(grade.value) * 0.01;
		headwindv = eval(headwind.value)  * (units ? 1.609 : 1.0) / 3.6;  // converted to m/s
		distancev = eval(distance.value)  * (units ? 1.609 : 1.0);
		temperaturev = ( eval(temperature.value) - (units ? 32.0 : 0.0) )  * (units ? 0.5555 : 1.0);
		elevationv = eval(elevation.value)  * (units ? 0.3048 : 1.0);
		transv = 0.95; // no one knows what this is, so why bother presenting a choice?
		}
		
		/* Common calculations */
		density = (1.293 - 0.00426 * temperaturev) * Math.exp(-elevationv / 7000.0);
		twt = 9.8 * (rweightv + bweightv);  // total weight in newtons
			A2 = 0.5 * frontalArea * density;  // full air resistance parameter
			tres = twt * (gradev + rollingRes); // gravity and rolling resistance
		
		if(!calcMode) {	// we calculate velocity from power when calcMode = 0
			powerv = eval(power.value);
			
			v = newton(A2, headwindv, tres, transv, powerv) * 3.6;      // convert to km/h
			if (v > 0.0) t = 60.0* distancev / v;
				else t = 0.0;  // don't want any div by zero errors
			
			velocity.value = makeDecimal2(v * (units ? 0.6214 : 1.0) );
			
		} else {  // we calculate power from velocity
			v = eval(velocity.value) / 3.6 * (units ? 1.609 : 1.0);  // converted to m/s;
			tv = v + headwindv; 
			var A2Eff = (tv > 0.0) ? A2 : -A2; // wind in face, must reverse effect
			powerv = (v * tres + v * tv * tv * A2Eff) / transv;
			
			if (v > 0.0) t = 16.6667 * distancev / v;  // v is m/s here, t is in minutes
			else t = 0.0;  // don't want any div by zero errors

			power.value = makeDecimal0(powerv);
			dragSlider.setValue(powerv/500.0);
		}
		
		/* Common calculations */
		
		// c = t * 60.0 * powerv / 0.25 / 1000.0; // kilowatt-seconds, aka kilojoules. t is converted to seconds from minutes, 25% conversion efficiency
		c = t * powerv * 0.24;  // simplified
		wl = c / 32318.0; // comes from 1 lb = 3500 Calories

		/* other results */
		
		time.value = makeDecimal2(t);
		calories.value = makeDecimal0(c * (units ? 0.2388 : 1.0));
		weightloss.value = makeDecimal2(wl * (units ? 2.205 : 1.0));
	}
}

// The following incorporates a work-around the adsense js conflict with window.onload in order to get the slider going. But it may not work right in IE8 or less, or in Opera. Ref: http://www.rgraph.net/docs/domcontentloaded.html

function startDragSlider() {
		dragSlider = new Dragdealer('powerCtrl',
		{
		x: 0.3,
		animationCallback: function(x, y)
			{
				// call update with x
				var powerField = document.getElementById('powerID');
				var form = document.getElementById('calcID');
				powerField.value = makeDecimal0(500.0 * x);
				calcMode = 0;
				update(form);
			}
		});
}
