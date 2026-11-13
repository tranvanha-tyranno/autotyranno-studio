"""Offline claims/timing/media guards for the China explainer compiler."""
import copy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import china

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'videos/2026-11-13-kinh-te-trung-quoc'


def content():
    return china.load(BATCH / 'content.json')


def test_pinned_claims_keep_source_periods_and_age_threshold():
    value = content()
    assert china.validate(value)['beats'] == 51
    assert value['facts']['gdpQuarters2026'] == [5.0, 4.3, 4.5]
    assert value['facts']['gdpYTD2026'] == 4.6
    assert value['facts']['age60PlusShareEnd2025'] == 23.0


@pytest.mark.parametrize('key,new', [('gdpQuarters2026', [5, 5, 5]), ('gdpYTD2026', 5), ('age60PlusShareEnd2025', 23.1)])
def test_changed_claims_require_research_and_graphic_review(key, new):
    value = content()
    value['facts'][key] = new
    with pytest.raises(ValueError, match='GDP|Age'):
        china.validate(value)


def test_four_parts_and_complete_chapter_words_cannot_change_silently():
    value = content()
    value['chapters'][0]['text'] += ' extra'
    with pytest.raises(ValueError, match='coverage'):
        china.validate(value)
    value = content()
    value['chapters'][0]['beats'][0]['phase'] = 'cta'
    with pytest.raises(ValueError, match='Four-part'):
        china.validate(value)


def test_voice_requests_keep_exact_script_native_speed_and_pinned_voice(tmp_path, monkeypatch):
    value = content()
    (tmp_path / 'content.json').write_text(json.dumps(value), encoding='utf-8')
    calls = []
    monkeypatch.setattr(china, 'speech', lambda target, text, voice: calls.append((target.name, text, voice)))
    china.voice(tmp_path)
    plan = china.load(tmp_path / 'audio/voice-plan.json')
    assert len(calls) == len(value['chapters'])
    assert [row[1] for row in calls] == [chapter['text'] for chapter in value['chapters']]
    assert all(row[2] == '6adFm46eyy74snVn6YrT' for row in calls)
    assert all(row['speed'] == 1.0 and row['language'] == 'vi' and row['model'] == 'eleven_v3' for row in plan['chapterTakes'])


def media_data():
    return {'fps': 30, 'shots': [{'id': 'a', 'start': 0, 'end': 60, 'layout': 'c-photo', 'design': {},
        'images': [{'file': 'china/alias-one.mp4', 'mediaType': 'video', 'sourceHash': 'same-source', 'trimBeforeFrames': 0, 'availableFrames': 120}]},
        {'id': 'b', 'start': 60, 'end': 120, 'layout': 'c-photo', 'design': {},
        'images': [{'file': 'china/alias-two.mp4', 'mediaType': 'video', 'sourceHash': 'same-source', 'trimBeforeFrames': 60, 'availableFrames': 120}]}]}


def test_source_aliases_share_one_nonoverlapping_source_clock():
    value = media_data()
    assert china.validate_media_intervals(value)['movingMediaSeconds'] == 4
    value['shots'][1]['images'][0]['trimBeforeFrames'] = 30
    with pytest.raises(ValueError, match='Repeated source'):
        china.validate_media_intervals(value)


def test_native_clip_cannot_freeze_or_loop_to_fill_a_beat():
    value = media_data()
    value['shots'][0]['images'][0]['availableFrames'] = 59
    with pytest.raises(ValueError, match='freeze/loop'):
        china.validate_media_intervals(value)


def test_contextual_photo_assignments_use_new_batch_without_old_coffee_sources():
    value = china.load(BATCH / 'data.json')
    images = [image for shot in value['shots'] for image in shot['images']]
    assert all(image['file'].startswith('china/') for image in images)
    assert not any('coffee' in image['file'].casefold() or 'cafe' in image['file'].casefold() for image in images)
    assert sum(shot['end'] - shot['start'] for shot in value['shots'] if shot['layout'] not in {'c-photo', 'c-closing'}) / value['frames'] >= .70


def test_no_forbidden_added_brand_in_authored_visible_or_spoken_fields():
    value = content()
    value['chapters'][0]['beats'][0]['headline'] += ' Tyranno'
    with pytest.raises(ValueError, match='branding'):
        china.validate(value)
