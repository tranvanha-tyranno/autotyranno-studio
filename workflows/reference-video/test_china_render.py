"""Three narrow render invariants, including a six-frame real stream-copy join."""
from pathlib import Path
import subprocess
import sys
import wave

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import china_render as r


def test_copy_gate_rejects_different_geometry_rate_sar_color_and_codec():
    base = {'codec': 'h264', 'profile': 'High', 'width': 1920, 'height': 1080, 'fps': 30.,
            'pixelFormat': 'yuv420p', 'sar': '1:1', 'color': 'tv, bt709, progressive)'}
    assert r.copy_compatible([base, dict(base)])
    for key, value in [('codec', 'hevc'), ('width', 1280), ('fps', 25), ('sar', '4:3'), ('color', None), ('profile', 'Main')]:
        assert not r.copy_compatible([base, {**base, key: value}])


def test_concat_audio_comes_from_exact_mix_and_copy_mode_has_no_video_encode():
    command = list(map(str, r.concat_command('parts.txt', 'exact-mix.wav', 17913, 'out.mp4', stream_copy=True)))
    assert command[command.index('-c:v') + 1] == 'copy'
    assert command[command.index('-c:a') + 1] == 'aac'
    assert command[command.index('-frames:v') + 1] == '17913'
    assert command[command.index('-t') + 1] == '597.100000000'
    assert '-vf' not in command and '1:a:0' in command and 'exact-mix.wav' in command
    fallback = list(map(str, r.concat_command('parts.txt', 'exact-mix.wav', 17913, 'out.mp4', stream_copy=False)))
    assert fallback[fallback.index('-c:v') + 1] == 'libx264' and '-vf' in fallback
    assert r.CACHE_BYTES == 268435456


def test_tiny_actual_packet_normalization_copy_join_and_full_video_audio_decode(tmp_path):
    normalized = []
    for index, color in enumerate(['red', 'blue']):
        source, target = tmp_path / f'part-{index}.mp4', tmp_path / f'norm-{index}.mp4'
        subprocess.run([r.FF, '-y', '-v', 'error', '-f', 'lavfi', '-i', f'color=c={color}:s=1920x1080:r=30',
            '-frames:v', '3', '-vf', 'setsar=1', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
            '-color_range', 'tv', str(source)], check=True, capture_output=True)
        subprocess.run(list(map(str, r.normalize_packet_command(source, target))), check=True, capture_output=True)
        normalized.append(target)
    assert r.copy_compatible([r.probe_video(path) for path in normalized])
    listing = tmp_path / 'parts.txt'
    listing.write_text('\n'.join("file '" + path.as_posix() + "'" for path in normalized), encoding='utf-8')
    mix = tmp_path / 'mix.wav'
    with wave.open(str(mix), 'wb') as audio:
        audio.setnchannels(2)
        audio.setsampwidth(2)
        audio.setframerate(48000)
        audio.writeframes(bytes(9600 * 4))
    output = tmp_path / 'joined.mp4'
    subprocess.run(list(map(str, r.concat_command(listing, mix, 6, output, stream_copy=True))), check=True, capture_output=True)
    assert r.decoded(output, 6)['frames'] == 6
    assert r.audio_decoded(output, .2, .18)['seconds'] >= .2
