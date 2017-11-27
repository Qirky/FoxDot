require 'json'
require ARGV[0]
include SonicPi::Synths

all_synths = {}
BaseInfo.get_all.each do |name, synth|
  next unless synth.is_a? SynthInfo
  data = {
    :name => synth.name,
    :synth_name => synth.synth_name,
    :prefix => synth.prefix,
    :category => synth.category,
    :doc => synth.doc,
    :arg_defaults => synth.arg_defaults,
    :info => synth.info,
  }
  all_synths[name] = data
end

if ARGV.length > 1
  File.write(ARGV[1], JSON.generate(all_synths))
else
  puts JSON.generate(all_synths)
end
