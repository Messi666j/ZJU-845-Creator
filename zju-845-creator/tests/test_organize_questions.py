"""Classification and archiving regression tests."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"organize_questions.py"
spec=importlib.util.spec_from_file_location("organizer",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OrganizerTests(unittest.TestCase):
    def test_seven_categories(self):
        cases={"梅森公式与信号流图":0,"阶跃响应的超调量":1,"根轨迹分离点":2,
               "Nyquist 稳定判据":3,"Jury 判据":4,"描述函数极限环":5,"状态空间能控性":6}
        for q,index in cases.items():
            with self.subTest(q=q):
                self.assertEqual(m.classify_question({"original":q})["category"],m.CATEGORIES[index])

    def test_unknown_and_multi_topic(self):
        self.assertEqual(m.classify_question({"original":"求 k"})["category"],m.CATEGORIES[8])
        cross=m.classify_question({"original":"根轨迹与 Nyquist 曲线比较"})
        self.assertEqual(cross["category"],m.CATEGORIES[7])
        self.assertTrue(cross["review_required"])

    def test_explicit_and_invalid(self):
        x=m.classify_question({"original":"Bode","category":"根轨迹"})
        self.assertEqual(x["category"],m.CATEGORIES[2])
        self.assertEqual(x["method"],"explicit")
        with self.assertRaises(ValueError):
            m.normalize_category("../../home")

    def test_directory_creation_and_private_solution(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp)/"bank"
            m.init_bank(root)
            self.assertTrue(all((root/c/".gitkeep").is_file() for c in m.CATEGORIES))
            item={"id":"../../lesson","original":"根轨迹","variant":"求分离点",
                  "category":"根轨迹","tags":["分离点"],"solution":"PRIVATE_ANSWER"}
            saved=m.save_item(item,root)
            folder=Path(saved["folder"])
            self.assertTrue(folder.resolve().is_relative_to(root.resolve()))
            self.assertTrue((folder/"original.md").exists())
            self.assertTrue((folder/"variant.md").exists())
            self.assertFalse((folder/"solution.md").exists())
            self.assertNotIn("PRIVATE_ANSWER","".join(p.read_text() for p in folder.glob("*") if p.is_file()))
            repeated=m.save_item(item,root,include_solution=True)
            self.assertNotEqual(saved["folder"],repeated["folder"])
            self.assertIn("PRIVATE_ANSWER",(Path(repeated["folder"])/"solution.md").read_text())

    def test_attachment_dry_run_and_batch(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp)/"bank"
            attachment=Path(tmp)/"figure.png"
            attachment.write_bytes(b"PNG")
            obj={"original":"数学模型 梅森公式","attachment_paths":[str(attachment)]}
            result=m.save_item(obj,root,dry_run=True)
            self.assertFalse(Path(result["folder"]).exists())
            result=m.save_item(obj,root)
            self.assertTrue((Path(result["folder"])/"attachments"/"figure.png").exists())
            data=Path(tmp)/"batch.json"
            data.write_text(json.dumps([{"original":"Nyquist"},{"variant":"阶跃响应超调量"}],ensure_ascii=False))
            proc=subprocess.run([sys.executable,str(SCRIPT),"save","--input",str(data),
                                 "--root",str(root)],capture_output=True,text=True,check=True)
            out=json.loads(proc.stdout)
            self.assertEqual(len(out),2)
            self.assertTrue(all(Path(x["folder"]).is_dir() for x in out))

if __name__=="__main__":
    unittest.main()
