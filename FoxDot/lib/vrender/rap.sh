notes=$1
durations=$2
lyrics=$3
tempo=$4
scale=$5
outputName=$6

python3 lib/vrender/compose/compose.py "$notes" "$durations" "$scale"

midi=lib/vrender/compose/last_midi_generated_by_vrender.mid

musescore $midi -o lib/vrender/midi2voice/musicXMLs/voice.musicxml
python2 lib/vrender/midi2voice/voiceConverter.py "$lyrics" lib/vrender/midi2voice/musicXMLs/voice.musicxml $tempo

OUTPUT=$(curl -X POST -F 'SPKR_LANG=english' -F 'SPKR=4' -F 'SYNALPHA=0.55' -F 'VIBPOWER=1' -F 'F0SHIFT=0' -F  'SYNSRC=@lib/vrender/midi2voice/musicXMLs/voice.xml' http://sinsy.sp.nitech.ac.jp/index.php | grep "lf0")
python2 lib/vrender/midi2voice/sinsy.py $OUTPUT

cp snd/_loop_/voice_last_recording.wav snd/_loop_/$outputName.wav