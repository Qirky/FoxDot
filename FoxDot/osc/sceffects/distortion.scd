SynthDef.new(\distortion,
{|bus, dist, tmp|
var osc;
osc = In.ar(bus, 2);
tmp = osc;
osc = CrossoverDistortion.ar(osc, amp:0.2, smooth:0.01);
osc = osc + (0.1 * dist * DynKlank.ar(`[[60,61,240,3000 + SinOsc.ar(62,mul:100)],nil,[0.1, 0.1, 0.05, 0.01]], osc));
osc = (osc.cubed * 8).softclip * 0.5;
osc = SelectX.ar(dist, [tmp, osc]);
ReplaceOut.ar(bus, osc)}).add;