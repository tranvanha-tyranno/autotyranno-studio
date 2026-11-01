"""Measured exposure QA and bounded, smooth luma correction for review footage."""
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageStat


def luma(image, roi=(.1, .1, .9, .9)):
    image = image.convert('L')
    w, h = image.size
    region = image.crop(tuple(round(value*size) for value, size in zip(roi, (w, h, w, h))))
    return ImageStat.Stat(region).mean[0]


def sample_frame(ffmpeg, source, seconds, size=(144, 256)):
    width, height = size
    result = subprocess.run([
        ffmpeg, '-v', 'error', '-ss', f'{seconds:.8f}', '-i', str(source),
        '-frames:v', '1', '-vf', f'scale={width}:{height}', '-pix_fmt', 'rgb24',
        '-f', 'rawvideo', 'pipe:1',
    ], capture_output=True, check=True)
    if len(result.stdout) != width*height*3:
        raise ValueError('No complete frame at '+str(seconds)+'s: '+str(source))
    return Image.frombytes('RGB', size, result.stdout)


def interpolate(points, field):
    """FFmpeg expression interpolated between measured points, held at ends."""
    expression = f'{points[-1][field]:.9f}'
    for first, last in reversed(list(zip(points, points[1:]))):
        begin, end = first['output_seconds'], last['output_seconds']
        a, b = first[field], last[field]
        ramp = f'({a:.9f}+({b-a:.9f})*(t-{begin:.9f})/{end-begin:.9f})'
        expression = f'if(lt(t,{end:.9f}),{ramp},{expression})'
    return expression


def exposure_plan(ffmpeg, source, opening, scene, settings):
    """Changes in composition can affect luma; all corrections require visual QA."""
    roi = settings.get('roi', [.1, .1, .9, .9])
    if len(roi) != 4 or not (0 <= roi[0] < roi[2] <= 1 and 0 <= roi[1] < roi[3] <= 1):
        raise ValueError('exposure_lock roi must be normalized bounds')
    maximum = settings.get('max_brightness', .07)
    if not isinstance(maximum, (float, int)) or not math.isfinite(maximum) or not 0 <= maximum <= .12:
        raise ValueError('max_brightness must be between zero and .12')
    black_floor = settings.get('black_floor', .12)
    black_transition = settings.get('black_transition', .32)
    if (not isinstance(black_floor, (int, float))
            or not isinstance(black_transition, (int, float))
            or not 0 <= black_floor < black_transition <= 1):
        raise ValueError('black_floor and black_transition must increase within zero to one')
    speed = scene['visual_speed']
    start, seconds = scene.get('source_start', 0), scene['seconds']
    # Muse returns 24 fps clips: the final presentation timestamp is 9.9583s
    # for a 10s file. Seeking to 9.96s yields no frame despite a valid duration.
    # Sample inside the final 100ms, also covering common 10/15/24/30 fps sources.
    used = seconds*speed
    last = start+used-min(.1, used/2)
    times = sorted(set([start, last] + [start+n for n in range(1, math.ceil(last-start)) if start+n < last]))
    with Image.open(opening) as image:
        target = luma(image.resize((144, 256)), roi)
    measured = [luma(sample_frame(ffmpeg, source, t), roi) for t in times]
    # Three-point smoothing and linear interpolation avoid per-frame auto-exposure
    # pumping. Preserve endpoints so progressive darkening is actually corrected.
    smoothed = [
        value if n in (0, len(measured)-1) else sum(measured[n-1:n+2])/3
        for n, value in enumerate(measured)
    ]
    points = []
    for t, raw, mean in zip(times, measured, smoothed):
        # eq brightness is an additive offset on limited-range video luma.
        desired = (target-mean)/219
        lower = -maximum if settings.get('allow_dimming', False) else 0
        correction = max(lower, min(maximum, desired)) if settings.get('enabled', True) else 0
        points.append({'source_seconds': t, 'output_seconds': (t-start)/speed,
                       'mean_luma': round(raw, 4), 'smoothed_luma': round(mean, 4),
                       'brightness': round(correction, 9),
                       'bounded': abs(desired) > maximum})
    return {
        'roi': roi, 'target_opening_luma': round(target, 4),
        'method': 'Opening-reference ROI mean; three-point smoothing and interpolated bounded Y-luma offsets. Composition affects the metric; visual review is mandatory.',
        'enabled': settings.get('enabled', True), 'allow_dimming': settings.get('allow_dimming', False),
        'preserve_blacks': bool(settings.get('preserve_blacks', False)),
        'black_floor': black_floor, 'black_transition': black_transition,
        'max_brightness': maximum, 'points': points,
        'end_to_opening_ratio': measured[-1]/max(target, 1),
        'end_to_start_ratio': measured[-1]/max(measured[0], 1),
        'needs_attention': measured[-1] < .90*target or any(p['bounded'] for p in points),
        'ffmpeg_filter': f"eq=brightness='{interpolate(points, 'brightness')}':eval=frame",
    }


def exposure_filters(input_label, output_label, plan, prefix):
    """Apply measured luma lift while leaving black display pixels unchanged.

    A luma mask selects the lifted image only above the shadow floor; chroma
    stays from the original. Names are scoped per scene for concat rendering.
    """
    if not plan['enabled']:
        return [f'[{input_label}]null[{output_label}]']
    if not plan.get('preserve_blacks'):
        return [f'[{input_label}]{plan["ffmpeg_filter"]}[{output_label}]']
    low = 16+219*plan['black_floor']
    high = 16+219*plan['black_transition']
    return [
        f'[{input_label}]split=3[{prefix}orig][{prefix}liftin][{prefix}maskin]',
        f'[{prefix}liftin]{plan["ffmpeg_filter"]}[{prefix}lift]',
        f"[{prefix}maskin]lutyuv=y='clip((val-{low:.6f})*255/{high-low:.6f},0,255)':u=128:v=128[{prefix}mask]",
        f'[{prefix}orig][{prefix}lift][{prefix}mask]maskedmerge=planes=1[{output_label}]',
    ]
