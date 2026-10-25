"""Offline behavioral checks; no real meeting or remote service is accessed."""
import importlib.util
import io
from contextlib import redirect_stdout
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v = load('verbatim', 'scripts/verbatim.py')
i = load('inventory', 'scripts/inventory.py')
t = load('download', 'dependencies/tencent-meeting-extract/scripts/tm_download.py')


class HelpersTest(unittest.TestCase):
    def test_correction_keeps_original_word(self):
        with patch.object(v, 'parse', return_value=[{'sp': 'SPEAKER_04', 'ts': 1, 'text': 'Daau'}]), patch.object(v, 'CONFIG', {'global_fix': [('Daau', 'DAU')]}), patch.object(sys, 'argv', ['verbatim.py', 'fixture']):
            output = io.StringIO()
            with redirect_stdout(output):
                v.main()
            self.assertIn('Daau〔修正：DAU；依据见修正对照表〕', output.getvalue())

    def test_metadata_like_speech_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.txt'
            source.write_text('● SPEAKER_04 | 00:00:01\n生成时间我们再核对。\n', encoding='utf-8')
            self.assertEqual(v.parse(source)[0]['text'], '生成时间我们再核对。')

    def test_all_unknown_speaker_numbers(self):
        for n in (0, 3, 4, 19, 100):
            self.assertIn('归属存疑', v.map_speaker({'sp': f'SPEAKER_{n:02}', 'ts': 0}, {}))

    def test_phase_mapping(self):
        cfg = {'default_speaker_map': {'SPEAKER_04': '甲'}, 'phase_breaks': [(10, {'SPEAKER_04': '乙'})]}
        self.assertEqual(v.map_speaker({'sp': 'SPEAKER_04', 'ts': 9}, cfg), '甲')
        self.assertEqual(v.map_speaker({'sp': 'SPEAKER_04', 'ts': 10}, cfg), '乙')

    def test_real_name_preserved(self):
        self.assertEqual(v.map_speaker({'sp': 'João', 'ts': 0}, {}), 'João')

    def test_repetition_and_order_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.txt'
            source.write_text('● SPEAKER_04 | 00:00:01\n嗯，就是，就是先确认。\n● João | 00:00:02\nYeah, yeah.\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/verbatim.py'), str(source)], capture_output=True, text=True, check=True)
            self.assertIn('嗯，就是，就是先确认。', result.stdout)
            self.assertLess(result.stdout.index('嗯，就是'), result.stdout.index('Yeah, yeah.'))
            self.assertIn('SPEAKER_04（发言人归属存疑）', result.stdout)
            self.assertNotIn('发言人归属已按', result.stdout)

    def test_invalid_transcript_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.txt'
            source.write_text('unsupported format', encoding='utf-8')
            with self.assertRaises(ValueError):
                v.parse(source)

    def test_missing_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                i.collect([str(Path(directory) / 'missing')])

    def test_hidden_material_can_be_included(self):
        with tempfile.TemporaryDirectory() as directory:
            hidden = Path(directory) / '.source.txt'
            hidden.write_text('material', encoding='utf-8')
            self.assertEqual(i.collect([directory], include_hidden=True), [str(hidden)])

    def test_same_basename_not_merged(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ('a', 'b'):
                folder = Path(directory) / name
                folder.mkdir()
                (folder / 'notes.txt').write_text(name, encoding='utf-8')
            self.assertEqual(len(i.collect([directory])), 2)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/inventory.py'), directory], capture_output=True, text=True, check=True)
            self.assertIn(str(Path(directory) / 'a/notes.txt'), result.stdout)
            self.assertIn(str(Path(directory) / 'b/notes.txt'), result.stdout)

    def test_referer_kept_and_http_failure_fails(self):
        with patch.object(t.subprocess, 'run') as run:
            run.return_value.returncode = 22
            with self.assertRaises(SystemExit):
                t.curl_download('https://example.invalid/video.mp4', 'https://meeting.tencent.com/cw/example', 'out.mp4')
            command = run.call_args.args[0]
            self.assertIn('--fail', command)
            self.assertIn('Referer: https://meeting.tencent.com/cw/example', command)

    def test_meeting_url_forms(self):
        self.assertEqual(t.referer_for('https://meeting.tencent.com/crm/abc123'), 'https://meeting.tencent.com/cw/abc123')
        with self.assertRaises(SystemExit):
            t.extract_code('https://example.invalid/')


if __name__ == '__main__':
    unittest.main()
