require 'json'
require ARGV[0]
include SonicPi::Synths

all_synths = {}
BaseInfo.get_all.each do |name, synth|
  is_synth = synth.is_a? SynthInfo
  data = {
    :name => synth.name,
    :synth_name => synth.synth_name,
    :prefix => synth.prefix,
    :doc => synth.doc,
    :arg_defaults => synth.arg_defaults,
    :user_facing => synth.user_facing?,
    :is_synth => is_synth,
  }
  if is_synth
    data[:category] = synth.category
  end
  all_synths[name] = data
end

if ARGV.length > 1
  File.write(ARGV[1], JSON.generate(all_synths))
else
  puts JSON.generate(all_synths)
end
