"""Measure this take's quiet pauses and retain all speech with boundary guards."""
import argparse
import hashlib
import importlib.util
import re
from pathlib import Path


def silence_ranges(log):
    start, ranges = None, []
    for line in log.splitlines():
        found = re.search(r'silence_start:\s*([\d.]+)', line)
        if found:
            start = float(found[1])
        found = re.search(r'silence_end:\s*([\d.]+)', line)
        if found and start is not None:
            ranges.append((start, float(found[1])))
            start = None
    return ranges


def speech_segments(duration, quiet, guard=.12, minimum_pause=.36):
    """Remove only the middle of measured internal pauses, preserving both ends."""
    cursor, segments, removed = 0., [], []
    for start, end in quiet:
        if start < .1 or end > duration-.1 or end-start < minimum_pause:
            continue
        cut_begin, cut_end = start+guard, end-guard
        if cut_begin >= cut_end:
            continue
        segments.append([round(cursor, 6), round(cut_begin, 6)])
        removed.append([round(cut_begin, 6), round(cut_end, 6)])
        cursor = cut_end
    segments.append([round(cursor, 6), duration])
    return segments, removed


def prepare(batch):
    spec = importlib.util.spec_from_file_location('product_runner', Path(__file__).with_name('run.py'))
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    config = runner.read_json(batch/'batch.json')
    rows = []
    for i, clip in enumerate(config['clips'], 1):
        for n, scene in enumerate(clip['scenes'], 1):
            folder = runner.storyboard_module().folder(runner, batch, i, clip, n)
            voice = runner.storyboard_module().voice_folder(runner, folder)/'voice.mp3'
            duration = runner.duration(voice)
            result = runner.run_ff([runner.FF, '-hide_banner', '-i', str(voice), '-af',
                                    'silencedetect=noise=-40dB:d=0.25', '-f', 'null', '-'])
            quiet = silence_ranges(result.stderr)
            segments, removed = speech_segments(duration, quiet)
            used = sum(end-start for start, end in segments)
            tempo = max(1., used/(scene['seconds']-.06))
            row = {
                'scene': n, 'voice_sha256': hashlib.sha256(voice.read_bytes()).hexdigest(),
                'original_seconds': duration, 'detected_quiet_ranges': quiet,
                'noise_threshold_db': -40, 'retained_boundary_guard_seconds': .12,
                'removed_quiet_interiors': removed, 'speech_preserving_segments': segments,
                'used_seconds': used, 'render_tempo': tempo,
                'scope': 'Derived only from this exact saved take; original voice retained. Never transfer ranges to a new take.',
            }
            runner.save_json(folder/'audio-timing-review.json', row)
            if tempo > 1.25:
                raise ValueError(f'Scene {n}: speech still too long after measured pause cleanup; revise script.')
            scene['audio_segments'] = segments
            rows.append(row)
    runner.save_json(batch/'batch.json', config)
    runner.save_json(batch/'narration-timing-qa.json', rows)
    runner.validate(config)
    print('Measured narration pauses:', len(rows), 'takes; max tempo', round(max(row['render_tempo'] for row in rows), 3))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    prepare(Path(args.batch).resolve())
