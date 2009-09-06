import mutagen.mp3

def validate_mp3(file_path):
    file = mutagen.mp3.MP3(file_path)
    result_list = []
    result_list.append( verify_attribute('Bitrate', file.info.bitrate, 128000) )
    result_list.append( verify_attribute('Sample Rate', file.info.sample_rate, 44100) )
    result_list.append( verify_attribute('Channel Mode', file.info.mode, mutagen.mp3.JOINTSTEREO, mp3_mode_label(file.info.mode), mp3_mode_label(mutagen.mp3.JOINTSTEREO)) )
    
    return result_list

def verify_attribute(label, data, expected_value, data_label = None, expected_value_label=None):
    status = "PASS"
    if data != expected_value:
        status="FAIL"

    if data_label == None:
        data_label = data
    if expected_value_label == None:
        expected_value_label = expected_value
            
    return label + " " + status + ": " + "Expected: " + str(expected_value_label) + " Actual: " + str(data_label)

_mp3_mode_labels = dict({
    mutagen.mp3.STEREO : "Stereo",
    mutagen.mp3.JOINTSTEREO : "Joint Stereo",
    mutagen.mp3.DUALCHANNEL : "Dual Channel",
    mutagen.mp3.MONO : "Mono"
    })

def mp3_mode_label(value):
    return _mp3_mode_labels.setdefault(value,'Unknown')

_mp3_bitrate_mode_labels = dict({
    0 : 'Constant Bitrate (CBR)',
    1 : 'Variable Bitrate (VBR)'
    })

def mp3_bitrate_mode_label(value):
    return _mp3_bitrate_mode_labels.setdefault(value,'Unknown')

"""
if(sys.argv.count < 2):
    print "missing argument"
    exit(255)
else:
    test = mutagen.mp3.MP3(sys.argv[1])
    test1 = eyeD3.Mp3AudioFile(sys.argv[1])

    br_mode =  test1.getBitRate()[0]

    
    fail_count = 0
    fail_count += verify_attribute('Bitrate', test.info.bitrate, 128000)
    fail_count += verify_attribute('Bitrate Mode', br_mode, 0, mp3_bitrate_mode_label(br_mode),mp3_bitrate_mode_label(0))

    fail_count += verify_attribute('Sample Rate', test.info.sample_rate, 44100)
    fail_count += verify_attribute('Channel Mode', test.info.mode, mutagen.mp3.JOINTSTEREO, mp3_mode_label(test.info.mode), mp3_mode_label(mutagen.mp3.JOINTSTEREO))
    
    exit(fail_count)
"""