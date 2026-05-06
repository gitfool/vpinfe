from __future__ import annotations

import importlib
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


sys.modules.setdefault(
    "nicegui",
    types.SimpleNamespace(ui=types.SimpleNamespace(input=object)),
)
sys.modules.setdefault(
    "platformdirs",
    types.SimpleNamespace(user_config_dir=lambda *args, **kwargs: "/tmp/vpinfe-test"),
)

vpx_config = importlib.import_module("managerui.pages.vpx_config")


class VpxConfigPageTests(unittest.TestCase):
    def test_displays_standalone_and_all_editor_keys(self):
        with TemporaryDirectory() as temp_dir:
            ini_path = Path(temp_dir) / "VPinballX.ini"
            ini_path.write_text(
                "[Editor]\n"
                "EnableLog = \n"
                "DisableHash = 1\n"
                "\n"
                "[Standalone]\n"
                "RenderingModeOverride = 1\n"
                "Haptics = \n"
                "\n"
                "[Version]\n"
                "VPinball = 10819999\n",
                encoding="utf-8",
            )

            parsed = vpx_config._parse_ini(ini_path)
            sections = vpx_config._build_display_sections(parsed)

        by_section = {
            section["name"]: {field.key for field in section["fields"]}
            for section in sections
        }
        self.assertIn("DisableHash", by_section["Editor"])
        self.assertIn("RenderingModeOverride", by_section["Standalone"])
        self.assertNotIn("Version", by_section)


if __name__ == "__main__":
    unittest.main()
