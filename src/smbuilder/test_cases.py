import base
import builder
import parser

import os
import unittest


def test_package():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(dirpath, 'testpackages', 'test_package')
    return target


class BuilderTests(unittest.TestCase):
    def test_find_plugin_deps(self):
        def fake_package(name, plugins):
            # TODO: this is downright idiotic
            return base.PackageContainer(name, plugins, {}, [], [], [], [], [], [], '', [], {})

        # TODO: this should really test package inheritance too
        p1 = fake_package('p1', ['plugin1', 'plugin2', 'plugin3'])
        p2 = fake_package('p2', ['plugin1', 'plugin4', 'plugin3'])
        packages = {
            'p1': p1,
            'p2': p2,
        }

        expected = set(['plugin1', 'plugin2', 'plugin3'])
        self.assertEqual(expected, base.find_plugin_deps(p1, packages))


class ParserTests(unittest.TestCase):
    def test_examples(self):
        target = test_package()
        parser.parse_configs(target)

        packages = sorted(['test_package'])
        plugins = sorted(['test_plugin', 'test_plugin2'])

        self.assertEqual(packages, sorted(parser.Packages.keys()))
        self.assertEqual(plugins, sorted(parser.Plugins.keys()))


class BaseTests(unittest.TestCase):
    def test_templatize(self):
        text = """
        sv_tags {{myarg}}
        sv_deadtalk {{deadtalk}}
        """
        args = {
            'myarg': 'myinput',
            'deadtalk': '1',
        }
        actual = base.templatize(text, args)
        expected = """
        sv_tags myinput
        sv_deadtalk 1
        """
        self.assertEqual(expected, actual)


class OverallTest(unittest.TestCase):
    def test_overall(self):
        target = test_package()
        builder.perform_builds(target, compiler='spcomp')


if __name__ == "__main__":
    unittest.main()
