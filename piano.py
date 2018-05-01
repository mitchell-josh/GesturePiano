import logging

import pygame
from samplerate import resample

MAX_OCTAVE = 7
WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
BLACK_KEYS = ['C#', 'D#', 'F#', 'G#', 'A#']
playing_keys = []


def generate_octaves(octave_count):
    pygame.mixer.init()

    # Create a new Sound object
    sound = pygame.mixer.Sound("res/c.wav")

    # Create an array and copy sample sound
    sound_array = pygame.sndarray.array(sound)

    ratio_dict = {'C': 1, 'C#': .944, 'D': .891, 'D#': .841, 'E': .794,
                  'F': .749, 'F#': .707, 'G': .667, 'G#': .63, 'A': .594,
                  'A#': .561, 'B': .53}

    scale_dict = {}
    for octave in range(1, octave_count + 1):
        for key, value in ratio_dict.items():
            key = key + '-' + str(octave)
            scale_dict[key] = pygame.sndarray.make_sound(resample(sound_array, value * octave, "sinc_fastest").astype(sound_array.dtype))

    return scale_dict


class Piano:
    def __init__(self, octave_count):
        if octave_count > MAX_OCTAVE:
            logging.error("Cannot generate more then " + MAX_OCTAVE + " octaves!")

        else:
            self.octave_count = octave_count
            self.note_dict = generate_octaves(octave_count)
            self.channel = pygame.mixer.Channel(5)

    def is_valid_note(self, note):
        if not note or note[0] not in WHITE_KEYS and note not in BLACK_KEYS or int(note[-1]) not in range(1, self.octave_count + 1):
            return False

        return True

    def play(self, note):
            self.channel.play(self.note_dict[note])

    def is_note_playing(self):
        return self.channel.get_busy()

    def stop(self):
        self.channel.stop()
