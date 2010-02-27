"""Utilities to validate that uploaded mp3 files meet the podiobooks standards"""

import eyeD3

def validate_mp3(file_path):
    """Validates that an mp3 file meets the podiobooks standards at the file level"""
    mp3file = eyeD3.Mp3AudioFile(file_path)
    result_list = []
    result_list.append(verify_attribute('Bitrate', mp3file.getBitRate()[1], 128))
    result_list.append(verify_attribute('Bitrate Mode', mp3_bitrate_mode_label(mp3file.getBitRate()[0]), mp3_bitrate_mode_label(0)))
    result_list.append(verify_attribute('Sample Rate', mp3file.getSampleFreq(), 44100))
    result_list.append(verify_attribute('Channel Mode', mp3file.header.mode.title(), 'Joint Stereo'))
    
    return result_list

def verify_attribute(label, data, expected_value, data_label=None, expected_value_label=None):
    """Creates validation result strings based on the test results"""
    status = "<span class='pass'>PASS</span>"
    if data != expected_value:
        status = "<span class='fail'>FAIL</span>"

    if data_label == None:
        data_label = data
    if expected_value_label == None:
        expected_value_label = expected_value
            
    return label + " " + status + ": " + "Expected: " + str(expected_value_label) + " Actual: " + str(data_label)

def mp3_bitrate_mode_label(value):
    """Returns the friendly name for the bitratemode by doing a table lookup"""
    
    _mp3_bitrate_mode_labels = dict({
        0 : 'Constant Bitrate (CBR)',
        1 : 'Variable Bitrate (VBR)'
    })
    
    return _mp3_bitrate_mode_labels.setdefault(value, 'Unknown')

