import itertools
from typing import List

import json

DEFINITIONS_FILE_NAME = "definitions.json"


def _set_definition_values(definition: dict, name: str, source: dict, trim_len: int,
                           split_type: str, remove_noise: bool, discard: int):
    definition["Name"] = name
    definition["RawSource"] = source["RawSource"]

    if trim_len == 0:
        definition["TrimSource"] = False
    else:
        definition["TrimSource"] = False
        definition["TrimSourceLengthMs"] = trim_len * 60 * 1000

    definition["ModelPath"] = source["ModelPath"]
    definition["Language"] = source["Language"]
    definition["SilenceSplitType"] = split_type
    definition["RemoveNoise"] = remove_noise
    if discard == 0:
        definition["DiscardTranscripts"] = False
    else:
        definition["DiscardTranscripts"] = True
        definition["DiscardWordCount"] = discard


def generate_definitions(name_idx_start: int = 0, sources: List[dict] = None,
                         trim_source_lengths_mins: List[int] = None,
                         silence_split_types: List[str] = None, split_lengths: List[int] = None,
                         split_min_silence_lens: List[int] = None, split_silence_threshs: List[int] = None,
                         remove_noises: List[bool] = None, discard_word_counts: List[int] = None,
                         whisper_vram: int = 10, gpu: int = 2):
    """
    :param name_idx_start: Start index for experiment names
    :param sources: List of dicts - elements should be given in format
        {"RawSource": str, "ModelPath": str, "Language": str}
    :param trim_source_lengths_mins: List of lengths to which input audios will be trimmed
    :param silence_split_types: List of silence split types - elements can be either 'equal' or 'silence'
    :param split_lengths: List of split lengths for split_equal
    :param split_min_silence_lens: List of min silence lengths for split_silence
    :param split_silence_threshs: List of silence threshs for split_silence
    :param remove_noises: List - elements can be either true or false
    :param discard_word_counts: List of ints - 0 means no transcripts are discarded
    :return: None
    """
    assert len(split_min_silence_lens) == len(split_silence_threshs)
    defs = []
    args = itertools.product(sources, trim_source_lengths_mins, silence_split_types, remove_noises, discard_word_counts)

    name_idx_count = name_idx_start
    name_base = "experiment_"
    for source, trim_len, split_type, remove_noise, discard in args:
        if split_type == 'equal':
            for length in split_lengths:
                definition = {}
                _set_definition_values(definition, name_base + str(name_idx_count), source,
                                       trim_len, split_type, remove_noise, discard)
                definition["SplitSilenceLength"] = length
                defs.append(definition)
                name_idx_count += 1

        elif split_type == 'silence':
            for silence_len, thresh in zip(split_min_silence_lens, split_silence_threshs):
                definition = {}
                _set_definition_values(definition, name_base + str(name_idx_count), source,
                                       trim_len, split_type, remove_noise, discard)
                definition["SplitSilenceMinLength"] = silence_len
                definition["SplitSilenceThresh"] = thresh
                defs.append(definition)
                name_idx_count += 1

    output = {
        "Definitions": defs,
        "Gpu": gpu,
        "WhisperVram": whisper_vram
    }

    with open(DEFINITIONS_FILE_NAME, 'w') as file:
        file.write(json.dumps(output))


if __name__ == '__main__':
    sources = [
        {
            "RawSource": "../audiofiles/raw",
            "ModelPath": "",
            "Language": "en"
        }
    ]
    trim_source_lengths_mins = [0, 10]
    silence_split_types = ['equal', 'silence']
    split_lengths = [8, 10]
    split_min_silence_lens = [300]
    split_silence_threshs = [-45]
    remove_noises = [True, False]
    discard_word_counts = [0, 3]
    generate_definitions(sources=sources, trim_source_lengths_mins=trim_source_lengths_mins,
                         silence_split_types=silence_split_types, split_lengths=split_lengths,
                         split_min_silence_lens=split_min_silence_lens, split_silence_threshs=split_silence_threshs,
                         remove_noises=remove_noises, discard_word_counts=discard_word_counts)
