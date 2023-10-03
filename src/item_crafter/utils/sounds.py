import os

from playsound import playsound


def play_sound_meaning_that_system_has_failed() -> None:
    playsound(_file_name_of_sound_meaning_that_system_has_failed())

def play_sound_meaning_that_property_has_been_found() -> None:
    playsound(_file_name_of_sound_meaning_that_property_has_been_found())


def _file_name_of_sound_meaning_that_system_has_failed() -> str:
    return f"..\\..\\sounds\\SystemFailure.mp3"

def _file_name_of_sound_meaning_that_property_has_been_found() -> str:
    return f"..\\..\\sounds\\ScanCompleted.mp3"


if __name__ == '__main__':
    play_sound_meaning_that_system_has_failed()
    play_sound_meaning_that_property_has_been_found()
