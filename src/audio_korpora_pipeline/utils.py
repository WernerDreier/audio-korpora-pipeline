import subprocess

import soundfile as sf


class SoundfileService:
  def downsample(self, filepath):
    audiodata, samplerate = sf.read(file=filepath)
    sf.write(file='outputfile.wav', data=audiodata, samplerate=16000)

  def downsampleAlternative(self, filepath):
    subprocess.call(['sox', filepath, '-e', 'mu-law',
                     '-r', '16k', 'file.wav', 'remix', '1,2'])
